import { StatusBar } from 'expo-status-bar';
import { Pressable, StyleSheet, Text, View , Button, Image } from 'react-native';
import { useState, useEffect } from 'react';

export default function Feature(){
    const [ledState, sLedState] = useState(null);

    const ledImage = ledState === "on" 
        ? require("./assets/ledOn.png") 
        : require("./assets/ledOff.png");

    const ledText = ledState === "on"
        ? 'TURN OFF'
        : 'TURN ON'

    const URL = "http://192.168.100.246:8000"
    const getLed = async () =>{
        try{
            const data = await fetch(`${URL}/http/c`)
            const newData = await data.json();
            sLedState(newData.ledState);
        }
        catch(err){
            sLedState("off")
        }
    }

    useEffect(() => {
        const initiate = async () =>{
            await getLed()
        }
        initiate();
        const interval = setInterval(() => {
            getLed();
        }, 1000);
        return () => clearInterval(interval)
    })

    const changeLed = async () =>{
        const newData = ledState === "on" ? "off" : "on"
        try{
            const send = await fetch(`${URL}/http/c`, {
                method : "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ledState: newData})
            })
            const data = await send.json();
            sLedState(data);
        }
        catch(err){
            alert("Can't change led state: " + err);
        }
        
    }

    return (
        <View 
            style={{
            backgroundColor: "#fff",
            flex: 1,
            justifyContent: 'space-evenly',
            alignItems: 'center',
            width: "100%"
            }}>

                <View style={styles.container}>
                    <View style={styles.infoCon}>
                        <Text style={styles.name}>1</Text>
                    </View>
                </View>
                <View style={styles.container}>
                    <View style={styles.infoCon}>
                        <Text style={styles.name}>Light</Text>
                        <Image source={ledImage} style={styles.img} />
                        <Button title={ledText} color={ledState == "on" ? "#0096FF" : "#000"} onPress={changeLed}/>
                    </View>
                </View>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 0.35, width: '100%', flexDirection: 'row', justifyContent: 'space-evenly',
    },
    infoCon:{
        flex: 0.6, borderWidth: 3, borderColor: "#ddd", borderRadius: 45, justifyContent: 'space-evenly', alignItems: 'center', 
        width: "100%", backgroundColor: "#eee"
    },
    img: {
        width: 100, height: 100,
    },
    name: {
        fontWeight: 'bold', fontFamily: 'Times New Roman', fontSize: 30
    },
})