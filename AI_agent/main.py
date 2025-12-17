from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from dotenv import load_dotenv

import json
from datetime import datetime
import requests
import time
import os

# ================= AUDIO =================
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from gtts import gTTS
import pygame

recognizer = sr.Recognizer()

def listen(seconds=4, samplerate=16000):
    audio = sd.rec(
        int(seconds * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    return sr.AudioData(audio.tobytes(), samplerate, 2)

def speak(text, language="en", accent="com.au"):
    if not text.strip():
        return

    temp_file = "temp.mp3"
    tts = gTTS(text=text, lang=language, tld=accent)
    tts.save(temp_file)

    pygame.mixer.init()
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.2)

    pygame.mixer.quit()
    os.remove(temp_file)

# ================= CONFIG =================
load_dotenv()

BASE_DIR = "/home/pi/Desktop/golang/ai"

try:
    with open(os.path.join(BASE_DIR, "define.json")) as f:
        configure = json.load(f)
    print("✅ Successfully found json file")
except Exception as e:
    print("❌ Failed to load json:", e)
    exit(1)

# ================= TOOLS =================
@tool
def time_teller(_: str = ""):
    """Tell current time"""
    return datetime.now().strftime("%H:%M:%S")

@tool
def date_teller(_: str = ""):
    """Tell current date"""
    return datetime.now().strftime("%d-%m-%Y")

@tool
def get_data_1():
    """Get sensor data from server"""
    return requests.get(configure["server1"]).json()

@tool
def get_data_2():
    """Get LED data from server"""
    return requests.get(configure["server2"]).json()

@tool
def turn_led_on():
    """Turn LED on"""
    data = requests.get(configure["server2"]).json()
    data["ledState"] = "on"
    return requests.put(configure["server2"], json=data).json()

@tool
def turn_led_off():
    """Turn LED off"""
    data = requests.get(configure["server2"]).json()
    data["ledState"] = "off"
    return requests.put(configure["server2"], json=data).json()

tools = [
    time_teller,
    date_teller,
    get_data_1,
    get_data_2,
    turn_led_on,
    turn_led_off,
]

# ================= MODELS =================
try:
    tool_model = ChatOllama(model=configure["tool_model"]).bind_tools(tools)
    print("✅ AI models are ready")
except Exception as e:
    print("❌ Model error:", e)
    exit(1)

# ================= STATE =================
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f"""
You are {configure["name"]}, a helpful home assistant.

Rules:
- Call tools only when needed
- Keep answers short, and straight to the point, don't include unnecessary informations
- Be friendly and natural
""")

    response = tool_model.invoke([system_prompt] + state["messages"])

    if response.tool_calls:
        for call in response.tool_calls:
            print(f"🔧 Tool call: {call['name']}")
    else:
        print("AI:", response.content)
        speak(response.content)

    state["messages"].append(response)
    return state

def should_continue(state: AgentState):
    return "tools" if state["messages"][-1].tool_calls else "end"

# ================= GRAPH =================
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("our_agent")
graph.add_edge(START, "our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {"tools": "tools", "end": END},
)
graph.add_edge("tools", "our_agent")

agent = graph.compile()

# ================= LOOP =================
WAKE_WORD = "hello"
history = []

print("🎤 Assistant is running...")
speak("Listening")

while True:
    try:
        print("Listening...")
        audio = listen()

        try:
            text = recognizer.recognize_google(audio).lower()
            print("User:", text)
        except sr.UnknownValueError:
            continue

        if text in ["exit", "close", "goodbye"]:
            print("Shutting down")
            break

        if WAKE_WORD not in text:
            continue

        speak("Yes?")
        audio = listen()
        try:
            command = recognizer.recognize_google(audio).lower()
            print("Command:", command)
        except sr.UnknownValueError:
            continue

        history.append(HumanMessage(content=command))
        result = agent.invoke({"messages": history})
        history = result["messages"]

    except KeyboardInterrupt:
        print("\nKeyboard shutdown")
        break

print("System stopped")
speak("See you later")
