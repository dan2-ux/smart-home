import { StatusBar } from 'expo-status-bar';
import { Pressable, StyleSheet, Text, View , Button, Image } from 'react-native';
import { useState, useEffect } from 'react';

export default function Sensor(){
    const URL = "http://192.168.100.246:8000"
    const [temp, sTemp] = useState(null);
    const [hum, sHum] = useState(null);
    const [gas, sGas] = useState(null);

    const getData = async () => {
        try{
            const data = await fetch(`${URL}/http`)
            const newData = await data.json();
            sTemp(newData.temp)
            sHum(newData.hum)
            sGas(newData.gas)
        }
        catch(err){
            sTemp("NOT FOUND")
            sHum("NOT FOUND")
            sGas("NOT FOUND")
        }
    }

    useEffect(() => {
        const initiate = async () => {
            await getData();
        };
    
        initiate();
    
        const interval = setInterval(() => {
            getData();
        }, 1000);
    
        return () => clearInterval(interval);
    }, []);
    

    return (
        <View 
            style={{
            backgroundColor: "#fff",
            flex: 1,
            flexDirection: 'column',
            justifyContent: 'space-evenly',
            alignItems: 'center'
            }}>
                <View style={{flex: 0.2 , width: '100%', flexDirection: 'row', justifyContent: 'space-evenly' }}>
                    <View style={styles.infoCon}>
                        <Text style={styles.name}>TEMPERATURE</Text>
                        <Image source={require('./assets/tempIcon.png')} style={styles.img} />
                        <Text style={{color: temp > 30 || temp < 10 ? "red" : "green", fontWeight: "bold"}}>{temp}°C</Text>
                    </View>
                    <View style={styles.infoCon}>
                        <Text style={styles.name}>HUMIDITY</Text>
                        <Image source={require('./assets/humIcon.png')} style={styles.img} />
                        <Text style={{color: hum > 80 || hum < 20 ? "red" : "green", fontWeight: "bold"}}>{hum}%</Text>
                    </View>
                </View>

                <View style={{flex: 0.2 , width: '100%', flexDirection: 'row', justifyContent: 'space-evenly' }}>
                    <View style={styles.infoCon}>
                        <Text style={styles.name}>GAS</Text>
                        <Image source={require('./assets/gasIcon.png')} style={styles.img} />
                        <Text style={{color: gas > 1000 ? "red" : "green", fontWeight: "bold"}}>{gas}</Text>
                    </View>
                    <View style={styles.infoCon}>
                        {/* <Text style={styles.name}>Unknow</Text>
                        <Text >3</Text>
                        <Text >3</Text> */}
                    </View>
                </View>
        </View>
    )
}

const styles = StyleSheet.create({
    name: {
        fontWeight: 'bold', fontFamily: 'Times New Roman'
    },
    img: {
        width: 50, height: 50,
    },
    infoCon:{
        flex: 0.35, borderWidth: 3, borderColor: "#ddd", borderRadius: 45, justifyContent: 'center', alignItems: 'center', 
        backgroundColor: "#eee"
    }
})