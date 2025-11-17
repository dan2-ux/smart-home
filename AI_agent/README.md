# This directory contains the second architecture within central layer.

The AI agent for this smart home is built using free and open platforms: Langgraph and Ollama.

- Langgraph: A Python-based programming language designed specifically for creating and deploying AI agents.

- Ollama: Provides free and unlimited access to large language models (LLMs) for developers worldwide.

# Workflow
The AI agent uses two cooperating AI modules to handle user commands efficiently:

### 1. Command Detection & Tool Invocation AI

- Responsible for understanding user input.

- Determines which tool or function should be called to execute the command.

### 2. Response AI

- Reads the output of the first AI.

- Generates a human-readable response for the user based on the result.

Together, these two AI modules allow the smart home system to interpret commands accurately and respond intelligently, creating a seamless and interactive user experience.

## Runing guidance
Run the .sh file to install the neccesary libraries.

For choosing LLM models, you can choose whatever LLM model you like. However, the fact is Pi 5 doesn't have GPU making running large model extremely difficult, therefore I recomment using small or cloud models.

Run the following code to run AI model:
<pre>
  python main.py
</pre>
