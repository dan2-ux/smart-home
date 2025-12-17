package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	_ "github.com/mattn/go-sqlite3"
)

func connectDatabase() *sql.DB {
	db, err := sql.Open("sqlite3", "/home/pi/Desktop/golang/go+sqlite/data.db")

	if err != nil {
		panic(err)
	}

	return db
}

func getDatabase() (int, float32, float32, int32, float32) {
	db := connectDatabase()

	rows, err := db.Query("SELECT * FROM sensor WHERE id = 1")

	defer db.Close()

	if err != nil {
		panic(err)
	}

	defer rows.Close()

	var id int
	var temp float32
	var hum float32
	var gas int32
	var voltage float32

	for rows.Next() {
		err := rows.Scan(&id, &temp, &hum, &gas, &voltage)
		if err != nil {
			panic(err)
		}
	}

	return id, temp, hum, gas, voltage
}

func getDatabaseC() (string, string) {
	db := connectDatabase()

	rows, err := db.Query("SELECT * FROM cData WHERE id = 1")

	defer db.Close()

	if err != nil {
		panic(err)
	}

	defer rows.Close()

	var id int
	var ledState string
	var lightState string

	for rows.Next() {
		err := rows.Scan(&id, &ledState, &lightState)
		if err != nil {
			panic(err)
		}
	}

	return ledState, lightState
}

type dataType struct {
	ID      int     `json:"id"`
	TEMP    float32 `json:"temp"`
	HUM     float32 `json:"hum"`
	GAS     int32   `json:"gas"`
	VOLTAGE float32 `json:"voltage"`
}

func getHTTP(c *gin.Context) {

	id, temp, hum, gas, voltage := getDatabase()

	c.IndentedJSON(http.StatusOK, gin.H{
		"id":      id,
		"temp":    temp,
		"hum":     hum,
		"gas":     gas,
		"voltage": voltage,
	})
}

func getHTTPC(c *gin.Context) {

	ledState, lightState := getDatabaseC()

	c.IndentedJSON(http.StatusOK, gin.H{
		"ledState":   ledState,
		"lightState": lightState,
	})
}

type ledType struct {
	LEDSTATE   string `json:"ledState"`
	LIGHTSTATE string `json:"lightState"`
}

func putHTTP(c *gin.Context) {

	var newData ledType

	if err := c.BindJSON(&newData); err != nil {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"message": "error"})
		return
	}

	db := connectDatabase()

	_, err1 := db.Exec(" UPDATE cData SET ledState = ?, lightState = ? WHERE id = 1", newData.LEDSTATE, newData.LIGHTSTATE)

	if err1 != nil {
		panic(err1)
	}
	pubMQTT()

	ledState, lightState := getDatabaseC()

	c.IndentedJSON(http.StatusOK, gin.H{
		"ledState":   ledState,
		"lightState": lightState,
	})
}

func connectMQTT(clientID string) mqtt.Client {
	broker := "tcp://192.168.100.246:1883"

	opt := mqtt.NewClientOptions()
	opt.AddBroker(broker)
	opt.SetClientID(clientID)
	opt.SetCleanSession(true)
	opt.OnConnectionLost = func(client mqtt.Client, err error) {
		print("Lost connection to MQTT")
		go MQTTsub()
	}

	client := mqtt.NewClient(opt)
	token := client.Connect()
	token.Wait()

	if token.Error() != nil {
		panic(token.Error())
	}

	return client
}

func MQTTsub() {
	client := connectMQTT("subMQTT")

	subMQTT := client.Subscribe("topic/test", 0, callback)
	subMQTT.Wait()

	if subMQTT.Error() != nil {
		panic(subMQTT.Error())
	}
}

var callback mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
	var newValue []dataType

	err := json.Unmarshal(msg.Payload(), &newValue)

	if err != nil {
		panic(err)
	}

	db := connectDatabase()
	defer db.Close()

	_, err1 := db.Exec(`
		UPDATE sensor 
		SET temp = ?, hum = ?, gas = ?, voltage = ?
		WHERE id = ?`,
		newValue[0].TEMP, newValue[0].HUM, newValue[0].GAS, newValue[0].VOLTAGE, newValue[0].ID,
	)

	if err1 != nil {
		panic(err1)
	}

	fmt.Printf("\n📩 MQTT message received: %s", string(msg.Payload()))

}

func pubMQTT() {
	client := connectMQTT("pubMQTT")

	ledState, lightState := getDatabaseC()

	newData := []ledType{
		{
			LEDSTATE:   ledState,
			LIGHTSTATE: lightState,
		},
	}

	dataHolder, _ := json.Marshal(newData)

	sendingMess := client.Publish("topic/test", 0, false, dataHolder)

	sendingMess.Wait()

	if sendingMess.Error() != nil {
		panic(sendingMess.Error())
	}

	client.Disconnect(250)
}

func main() {

	go MQTTsub()

	router := gin.Default()

	router.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:3000"},
		AllowMethods:     []string{"GET", "PUT", "POST", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
	}))

	router.GET("/http", getHTTP)
	router.GET("/http/c", getHTTPC)
	router.PUT("/http/c", putHTTP)
	router.Run("192.168.100.246:8000")
}
