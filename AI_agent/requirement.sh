#!/bin/bash

# Install Python libraries
pip install typing-extensions langgraph langchain-core langchain-ollama python-dotenv requests SpeechRecognition pyttsx3

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

echo "All libraries + Ollama installed!"




# # Install Python libraries for Windows
# pip install typing-extensions langgraph langchain-core langchain-ollama python-dotenv requests SpeechRecognition pyttsx3

# # Download Ollama installer
# Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile "OllamaSetup.exe"

# Write-Host "Starting Ollama installer..."
# Start-Process "OllamaSetup.exe"

# Write-Host "All libraries installed. Run the Ollama installer to finish."
