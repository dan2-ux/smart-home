# This repository showcases how smart home architecture can be integrated with an AI agent.

This project presents an AI-driven approach to smart home automation. The system empowers an AI agent to configure and control household devices, adapt to user preferences, and optimize home operations. In addition, it provides real-time data and insights to users, enabling smarter decisions and a more responsive home environment.

## Futuristic Smart Home

Everyone has a vision of living in a home full of technology—where everything is connected and, more importantly, the system can understand and communicate with the user effectively. By implementing AI in the central hub and equipping it with the tools to interact with servers, this vision becomes a reality.

## Workflow
The system is structured into three main layers:

### 1. Embedded Layer

- Consists of ESP32 MCUs interfacing with sensors and actuators.

- Publishes sensor data to the central layer via MQTT.

- Subscribes to the central layer to receive commands or updated API values, allowing devices to adapt automatically.

### 2. Central Layer

- Contains two main components: a Go-based server and an AI agent.

- The server, running on a Raspberry Pi 5 with SQLite, handles API storage, distribution, and communication with both embedded devices and the mobile app.

- The AI agent runs natively on the Pi 5 and can read and modify database values, enabling intelligent automation and decision-making.

### 3. Mobile Application Layer

- Connects to the Go server via HTTP/REST APIs.

- Displays real-time sensor data and allows users to monitor and control their smart home remotely.

## Simplified Architecture Diagram
        ┌─────────────────────────┐
        │  Mobile Application     │
        │  (react native)         │
        └─────────▲───────────────┘
                  │
             REST / HTTP
                  │
        ┌─────────▼───────────────┐
        │       Central Layer     |
        │         (Pi 5)          |
        │ ┌───────┐   ┌─────────┐ │
        │ │Server │   │ AI Agent│ │
        │ └───────┘   └─────────┘ │
        └─────────▲───────────────┘
                  │
                 MQTT
                  │
        ┌─────────▼───────────────┐
        │     Embedded Layer      │
        │         ESP32           │
        │ (Sensors & Actuators)   │
        └─────────────────────────┘

## Hardware requirements
- Raspberry pi 5
- ESP32
- DHT22
- MQ2
- LEDs
- Fan
- Relay
- Speakers

# Software requirements
- FREERTOS
- Ollama

# Communication protocols
- HTTP
- MQTT

## Running Guidance
### For Application layer
Import npm and run the following:
<pre>
  sudo npm i -g expo-cli
  expo init INITtest # choose blank as this is written is Javascript
  cd INITtest
  npm start
</pre>

Then copy all the js files in this repository into your newly created react native enviroment.

#### For embedded and cental layers consider read README files in other folders.


