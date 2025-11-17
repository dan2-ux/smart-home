import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()

try:
    c.execute("""
        CREATE TABLE sensor (
            id INTEGER PRIMARY KEY,
            temp REAL,
            hum REAL,
            gas INTEGER
        )
    """)
    c.execute("""
        CREATE TABLE cData (
              id INTERGER PRIMARY KEY,
              ledState TEXT
        )
    """)
    print("\nSuccessfully created table")
except:
    print("\nTable exit")

c.execute("""
    INSERT INTO sensor (id, temp, hum, gas)
    VALUES (?, ?, ?, ?)
""", (1, 0, 0, 0))

c.execute("""
    INSERT INTO cData (id, ledState) VALUES (?, ?)
""", (1, "off"))

conn.commit()

conn.close()
