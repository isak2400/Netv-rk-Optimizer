import sqlite3

from werkzeug.security import (
    generate_password_hash
)

username = input("Username: ")

password = input("Password: ")

hashed_password = generate_password_hash(
    password
)

conn = sqlite3.connect(
    "network_monitor.db"
)

cursor = conn.cursor()

cursor.execute("""

INSERT INTO users (
    username,
    password
)

VALUES (?, ?)

""", (username, hashed_password))

conn.commit()

conn.close()

print("Bruger oprettet!")