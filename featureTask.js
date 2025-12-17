import { StatusBar } from 'expo-status-bar';
import { Pressable, StyleSheet, Text, View, Button, Image } from 'react-native';
import { useState, useEffect } from 'react';

export default function Feature() {
    const [ledState, sLedState] = useState("off");
    const [lightState, sLightState] = useState("off");

    const ledImage = ledState === "on" 
        ? require("./assets/ledOn.png") 
        : require("./assets/ledOff.png");

    const ledText = ledState === "on" ? 'TURN OFF' : 'TURN ON';

    const lightImage = lightState === "on"  // fixed
        ? require("./assets/ledOn.png") 
        : require("./assets/ledOff.png");

    const lightText = lightState === "on" ? 'TURN OFF' : 'TURN ON'; // fixed

    const URL = "http://192.168.100.246:8000";

    const getLed = async () => {
        try {
            const data = await fetch(`${URL}/http/c`);
            const newData = await data.json();
            sLedState(newData.ledState);
            sLightState(newData.lightState);
        } catch(err) {
            sLedState("off");
            sLightState("off");
        }
    }

    useEffect(() => {
        getLed();
        const interval = setInterval(getLed, 1000);
        return () => clearInterval(interval);
    }, []);

    const changeLed = async () => {
        const newLedState = ledState === "on" ? "off" : "on";
    
        try {
            const send = await fetch(`${URL}/http/c`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ledState: newLedState, lightState: lightState })
            });
            const data = await send.json();
            sLedState(data.ledState);
            sLightState(data.lightState);
        } catch (err) {
            alert("Can't change states: " + err);
        }
    }
    
    const changeLight = async () => {
        const newLightState = lightState === "on" ? "off" : "on";
    
        try {
            const send = await fetch(`${URL}/http/c`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ledState: ledState, lightState: newLightState })
            });
            const data = await send.json();
            sLedState(data.ledState);
            sLightState(data.lightState);
        } catch (err) {
            alert("Can't change states: " + err);
        }
    }
    
    
    return (
        <View style={styles.main}>
            <View style={styles.container}>
                <View style={styles.infoCon}>
                    <Text style={styles.name}>LIGHT</Text>
                    <Image source={lightImage} style={styles.img} />
                    <Button title={lightText} color={lightState === "on" ? "#0096FF" : "#000"} onPress={changeLight}/>
                </View>
            </View>
            <View style={styles.container}>
                <View style={styles.infoCon}>
                    <Text style={styles.name}>LED</Text>
                    <Image source={ledImage} style={styles.img} />
                    <Button title={ledText} color={ledState === "on" ? "#0096FF" : "#000"} onPress={changeLed}/>
                </View>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    main: {
        backgroundColor: "#fff",
        flex: 1,
        justifyContent: 'space-evenly',
        alignItems: 'center',
        width: "100%"
    },
    container: {
        flex: 0.35,
        width: '100%',
        flexDirection: 'row',
        justifyContent: 'space-evenly',
    },
    infoCon: {
        flex: 0.6,
        borderWidth: 3,
        borderColor: "#ddd",
        borderRadius: 45,
        justifyContent: 'space-evenly',
        alignItems: 'center', 
        width: "100%",
        backgroundColor: "#eee"
    },
    img: {
        width: 100,
        height: 100,
    },
    name: {
        fontWeight: 'bold',
        fontFamily: 'Times New Roman',
        fontSize: 30
    },
});
