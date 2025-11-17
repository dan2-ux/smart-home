static const BaseType_t pro_cpu = 0;
static const BaseType_t app_cpu = 1;

#include <DHT.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>

WiFiClient esp32Client;
PubSubClient client(esp32Client);

#define warningLed 0
#define DHTPIN 4
#define DHTTYPE DHT22
#define gas 34
#define controlLed 21

DHT dht(DHTPIN, DHTTYPE);

static const char* ssid = "Your ssid";
static const char* pass = "your pass";
static const char* mqtt_server = "your mqtt server";
static const char* topic = "topic/test";

static TimerHandle_t turnoff_warningLed;

static SemaphoreHandle_t mutex1, mutex2;

static QueueHandle_t tempQ, humQ, gasQ;

static String jsonEx = "[{\"id\": \1, \"temp\": \0, \"hum\": 0, \"gas\": 0}]";

void turnOffLed(TimerHandle_t xTimer){
  digitalWrite(warningLed, LOW);
}

void dhtSensor(void *paramter){
  float temp, hum;
  while(1){
    if (xSemaphoreTake(mutex1, portMAX_DELAY)){
      temp = dht.readTemperature();
      hum = dht.readHumidity();

      xQueueSend(tempQ, &temp, 10);
      xQueueSend(humQ, &hum, 10);
      //Serial.printf("\nTemp: %f || Hum: %f", temp, hum);
      if (temp > 50 || hum < 20 ){
        xSemaphoreTake(mutex2, portMAX_DELAY);
        digitalWrite(warningLed, HIGH);
        xTimerStart(turnoff_warningLed, portMAX_DELAY);
        xSemaphoreGive(mutex2);
      }
      xSemaphoreGive(mutex1);
    }
    vTaskDelay(1000 / portTICK_PERIOD_MS);
  }
}

void mq2Sensor(void *parameter){
  int gasValue;
  while(1){
    if (xSemaphoreTake(mutex1, portMAX_DELAY)){
      gasValue = analogRead(gas);

      xQueueSend(gasQ, &gasValue, 10);
      //Serial.printf("\nGas: %d", gasValue);
      if (gasValue > 1000){
        xSemaphoreTake(mutex2, portMAX_DELAY);
        digitalWrite(warningLed, HIGH);
        
        xTimerStart(turnoff_warningLed, portMAX_DELAY);
        xSemaphoreGive(mutex2);
      }
      xSemaphoreGive(mutex1);
    }
    vTaskDelay(1000 / portTICK_PERIOD_MS);
  }
}

void check_connection(){
  while(WiFi.status() != WL_CONNECTED){
      Serial.println("\nReconnecting to WiFi");
      WiFi.begin(ssid, pass);
      delay(1000);
  }
  
  while(!client.connected()){
    Serial.println("\nReconnecting to Server");
    if (client.connect("ESP32Client")){
      client.subscribe(topic);
      delay(1000);
    }
  }
}

void pubMQTT(void *parameter){
  float temp, hum;
  int gasValue;
  while(1){
    xQueueReceive(tempQ, &temp, 10);
    xQueueReceive(humQ, &hum, 10);
    xQueueReceive(gasQ, &gasValue, 10);

    StaticJsonDocument <200> json;
    deserializeJson(json, jsonEx);

    json[0]["id"] = 1;
    json[0]["temp"] = temp;
    json[0]["hum"] = hum;
    json[0]["gas"] = gasValue;

    serializeJson(json, jsonEx);

    vTaskDelay(500 / portTICK_PERIOD_MS);

    client.publish(topic, jsonEx.c_str());

    Serial.printf("\nTemp: %f C|| Hum: %f %%|| Gas: %d ", temp, hum, gasValue);
  }
}

void callback(char* topic, byte* payLoad, int length){
  String message = "";
  for (int i = 0 ; i < length; i ++){
    message += (char)payLoad[i];
  }
  StaticJsonDocument <200> json;
  deserializeJson(json, message);

  if (json[0]["ledState"] == "on" && digitalRead(controlLed) == LOW){
    digitalWrite(controlLed, HIGH);
  }
  else if (json[0]["ledState"] == "off" && digitalRead(controlLed) == HIGH){
    digitalWrite(controlLed, LOW);
  }
}

void setup(){
  Serial.begin(9600);

  pinMode(warningLed, OUTPUT);
  pinMode(controlLed, OUTPUT);
  dht.begin();

  WiFi.begin(ssid, pass);
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  mutex1 = xSemaphoreCreateMutex();
  mutex2 = xSemaphoreCreateMutex();

  tempQ = xQueueCreate(5, sizeof(float));
  humQ = xQueueCreate(5, sizeof(float));
  gasQ = xQueueCreate(5, sizeof(int));

  turnoff_warningLed = xTimerCreate(
    "Turn off led after 5 seconds",
    5000 / portTICK_PERIOD_MS,
    pdFALSE,
    (void *)0,
    turnOffLed
  );

  xTaskCreatePinnedToCore(
    dhtSensor, "dht sensor reader", 2048, NULL, 5, NULL, app_cpu
  );

  xTaskCreatePinnedToCore(
    mq2Sensor, "gas sensor reader", 2048, NULL, 5, NULL, app_cpu
  );

  xTaskCreatePinnedToCore(
    pubMQTT, "publish MQTT data", 5000, NULL, 4, NULL, pro_cpu
  );
}

void loop(){
  check_connection();
  client.loop();
}
