# This directory is one the architect inside the central layer

Golang and SQLite work together to create a stable, fast, and reliable server that runs natively on the Raspberry Pi 5, leaving more resources available for the AI agent to operate efficiently.

# Workflow

The server continuously receives sensor data from the embedded layer via MQTT. Golang updates the SQLite database with this incoming data.

The server also listens for commands from the mobile application.

If a command is detected, the server sends an MQTT message to the embedded layer to update or modify the relevant device values.

## Running Guidance
### First: create the database
<pre>
  python createDatabase.py
</pre>

### Then run the server
<pre>
  go run main.py
</pre>
