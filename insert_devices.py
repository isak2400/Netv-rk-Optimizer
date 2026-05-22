import sqlite3

conn = sqlite3.connect("network_monitor.db")
cursor = conn.cursor()

devices = [
    ("MAKHTAL-PC", "192.168.10.3"),
    ("PC-02", "192.168.20.3"),
    ("PC-03", "192.168.20.2"),
    ("PC-04", "192.168.10.2"),
    
]

for name, ip in devices:
    cursor.execute("""
        INSERT OR IGNORE INTO devices (name, ip_address)
        VALUES (?, ?)
    """, (name, ip))

conn.commit()
conn.close()

print("Enheder indsat korrekt!")