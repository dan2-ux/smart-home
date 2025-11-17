import { StatusBar } from 'expo-status-bar';
import { Pressable, StyleSheet, Text, View , Button, Image } from 'react-native';
import { useState } from 'react';

export default function Bar({sendBarData}){
    const [state, sState] = useState("sensor")
    const stateChange = (newState) => {
        sState(newState);
        sendBarData(newState);
    }
    return (
        <View 
        style={{
            backgroundColor: "#eee",
            flex: 0.1, 
            flexDirection: "row",
            justifyContent: 'space-evenly',
            alignItems: 'center'
          }}>
        <Pressable style={ ({pressed}) => ({
          flex: 0.3,
          height: 50,
          justifyContent: 'center',
          alignItems: 'center',
          transform: [{scale: pressed ? 1.3 : 1}],
          
        })} onPress={() => stateChange('sensor')} >
          <View style={{flex: 1, justifyContent: 'center', alignItems: 'center'}}>
            <Image source={require('./assets/sensorIcon.png')}
              style={{width: 25, height: 25}}
            />
            <Text style={{color: "#000"}}>Sensor</Text>
          </View>
        </Pressable>
        <Pressable style={ ({pressed}) => ({
          flex: 0.3,
          height: 50,
          justifyContent: 'center',
          alignItems: 'center', 
          transform: [{scale: pressed ? 1.3 : 1}]
        })} onPress={() => stateChange('feature')}>
          <View style={{flex: 1, justifyContent: 'center', alignItems: 'center'}}>
            <Image source={require('./assets/featureIcon.png')}
              style={{width: 25, height: 25}}
            />
            <Text style={{color: "#000"}}>Feature</Text>
          </View>
        </Pressable>
      </View>
    )
}