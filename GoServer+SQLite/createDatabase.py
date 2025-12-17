import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()

try:
    c.execute("""
        CREATE TABLE sensor (
            id INTEGER PRIMARY KEY,
            temp REAL,
            hum REAL,
            gas INTEGER,
            voltage REAL
        )
    """)
    c.execute("""
        CREATE TABLE cData (
              id INTERGER PRIMARY KEY,
              ledState TEXT,
              lightState TEXT
        )
    """)
    print("Successfully created table")
except:
    print("Table exit")


try :
    c.execute("""
        INSERT INTO sensor (id, temp, hum, gas, voltage)
        VALUES (?, ?, ?, ?, ?)
    """, (1, 0, 0, 0, 0))

    c.execute("""
        INSERT INTO cData (id, ledState, lightState) VALUES (?, ?, ?)
    """, (1, "off", "off"))
    print("Successfully enter sample value for database")
except:
    print("Failed to put sample value in database")

conn.commit()

conn.close()
