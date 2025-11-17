from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END ,START
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage ,AIMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from dotenv import load_dotenv
import json
from datetime import datetime

#import speech_recognition as sr

import requests

#recognizer = sr.Recognizer()

#import pyttsx3

# voice_model = pyttsx3.init()

# voice_setup = voice_model.getProperty('voices')

# voice_model.setProperty('voice', voice_setup[1].id)

# def speak(text: str, voice : bool):
#     engine = pyttsx3.init()
#     voice_setup = engine.getProperty('voices')
#     voice_choose = voice_setup[1] if voice else voice_setup[0]
#     engine.setProperty('voice', voice_choose.id)
#     engine.say(text)
#     engine.runAndWait()
#     engine.stop()

# from gtts import gTTS
# import pygame

import time
import os

# def speak(text: str, voice: bool = True, language="en", accent="com.au"):
#     temp_file = "temp.mp3"
    
#     speech = gTTS(text=text, lang=language, tld=accent, slow=not voice)
#     speech.save(temp_file)

#     pygame.mixer.init()
#     pygame.mixer.music.load(temp_file)
#     pygame.mixer.music.play()

#     while pygame.mixer.music.get_busy():
#         time.sleep(0.5)

#     pygame.mixer.music.stop()
#     pygame.mixer.quit()
#     os.remove(temp_file)

load_dotenv()

@tool
def time_teller(t : str):
    """ Time teller function """
    t = datetime.now().strftime("%H:%M:%S %p")
    return t

@tool
def date_teller(d : str):
    """ Date , year and month teller function """
    d = datetime.now().strftime("%d-%m-%Y")
    return d

@tool
def get_data_1():
    """Get data from golang server """
    res = requests.get(configure["server1"])
    return res.json()

@tool 
def get_data_2():
    """ Set the data from golang server """
    res = requests.get(configure["server2"])
    return res.json()

@tool 
def turn_led_on():
    """ Set the data from golang server """
    get = requests.get(configure["server2"])
    newData = get.json()

    newData["ledState"] = "on"
    res = requests.put(configure["server2"], json=newData)
    return res.json()

@tool
def turn_led_off():
    """ Set the data from golang server """
    get = requests.get(configure["server2"])
    newData = get.json()

    newData["ledState"] = "off"
    res = requests.put(configure["server2"], json=newData)
    return res.json()

try:
    with open("define.json") as F:
        configure = json.load(F)
    print("✅Successfully found json file")
except Exception as e:
    print("❌Failed to find json file")

tools = [time_teller, date_teller, get_data_1, get_data_2, turn_led_on, turn_led_off]
get_date = datetime.now().strftime("%Y_%m_%d")

try:
    tool_model = ChatOllama(model= configure["tool_model"]).bind_tools(tools)
    talk_model = ChatOllama(model= configure["talk_model"])
    print("✅ AI models are ready")
except Exception as e:
    print("❌ AI model Error: ", e)

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


try:
    server1 = configure["server1"]
    server2 = configure["server2"]
    res1 = requests.get(server1) 
    res2 = requests.get(server1) 
    if res1.status_code == 200 and res2.status_code == 200:
        print("✅ Connected to server")
    else :
        print("❌ Failed to connect to server")
except Exception as e:
    print("Error: ", e)


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f"""
    You are {configure["name"]}, a helpful and polite home assistant AI. {configure["workflow"]}

    You have access to the following tools:
    - **time_teller** — tells the current time
    - **date_teller** — tells the current date
    - **get_data_1** — retrieves the current sensor value from golang server.
    - **get_data_2** — retrieves the current values from golang server.
    - **turn_led_on** - tool for turning the LED on.
    - **turn_led_on** - tool for turning the LED off.

    **Important behavioral rules:**
    1. Only call `time_teller` or `date_teller` if the user explicitly asks for the time or date.
    2. Only call `getData` if the user asks about the LED or its current status.
    3. Keep all responses short, direct, and natural — no unnecessary words.
    4. Speak in a friendly and conversational tone, as if you’re talking to someone at home.
    5. The database consits of temperature, humidity and gas value, if user want to know either of those value call "get_data_1".
    5. Call "get_data_2" when user want to know the current value of led or other changable things.
    6. Call "turn_led_on" when user want to turn the LED on.
    6. Call "turn_led_off" when user want to turn the LED off.
    """)


    # Let model call tools
    response = tool_model.invoke([system_prompt] + state["messages"])

    if hasattr(response, "tool_calls") and response.tool_calls:
        print("\nAI is making a tool call:")
        for call in response.tool_calls:
            print(f"→ Tool: {call['name']}, Arguments: {call['args']}")
    else:
        print("\nAI:", response.content.strip())
        ##speak(response.content)

    state["messages"].append(response)
    return state
    
def should_continue(state: AgentState): 
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls: 
        return "tools"
    else:
        return "end"

graph = StateGraph(AgentState)
graph.add_edge("tools", "our_agent")
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "tools": "tools",
        "end": END,
    },
)

graph.add_edge(START, "our_agent")
graph.add_edge("our_agent", END)

agent = graph.compile()

tem_history = []

#agent.invoke({"messages": [HumanMessage(content= "Hello")]})

while True:
    try:
        text = input("\nUser: ")
        # try:
        #     with sr.Microphone() as mic:
        #         print("Listening...")
        #         recognizer.adjust_for_ambient_noise(mic, duration=0.3)
        #         audio = recognizer.listen(mic)

        #         text = recognizer.recognize_google(audio)
        #         text = text.lower()

        #         print(f"User: {text}")

        # except sr.UnknownValueError:
        #     recognizer = sr.Recognizer()
        #     print("Could not understand audio, retrying...")
        #     continue
        if text.lower() in ["exit", "close", "end", "goodbye"]:
            print("Shutting down")
            break
        tem_history.append(HumanMessage(content= text))
        result = agent.invoke({"messages": tem_history})
        tem_history = result["messages"]

    except KeyboardInterrupt as e:
        print("Keyboard shutdown")

print(f"Shutting down {configure['tool_model']} model and {configure['talk_model']} model")
