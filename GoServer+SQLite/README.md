# This is directory is one the architect inside the central layer

Golang and SQLite will joing to create a stable, fast and reliable server which runs natively on Pi 5. Making Pi 5 has more room to run AI agent.

## Workflow
Server will continiouesly receive value from sensors through MQTT, which GO will use it to change SQLite.
It also listen to mobile app to detect alter command from user, if command detected it will send MQTT command to alter changable value on embedded layer.

## Running Guidance
### First: create the database
<pre>
  python createDatabase.py
</pre>

### Then run the server
<pre>
  go run main.py
</pre>
