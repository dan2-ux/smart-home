import { StatusBar } from 'expo-status-bar';
import { Pressable, StyleSheet, Text, View , Button, Image } from 'react-native';
import Bar from './bar'
import Sensor from './sensorTask'
import Feature from './featureTask'

import { useState } from 'react';

export default function App(){
  const [state, sState] = useState("sensor");
  return (
    <View style={{flex: 1}}>
      {state == "sensor" ? <Sensor/> : <Feature/>}

      <Bar sendBarData={(newState) => {sState(newState)}} />
    </View>
  )
}
