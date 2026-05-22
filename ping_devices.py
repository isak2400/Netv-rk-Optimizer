import sqlite3
import subprocess
import re
import time

DB_NAME = "network_monitor.db"


def ping_device(ip_address):

    command = ["ping", "-n", "10", ip_address]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15
        )

        output = result.stdout

        loss_match = re.search(
            r"Lost = \d+ \((\d+)% loss\)",
            output
        )

        avg_match = re.search(
            r"Average = (\d+)ms",
            output
        )

        packet_loss = (
            float(loss_match.group(1))
            if loss_match else 100.0
        )

        ping_ms = (
            float(avg_match.group(1))
            if avg_match and packet_loss < 100
            else None
        )

        return ping_ms, packet_loss

    except:

        print("Ping timeout eller fejl")

        return None, 100.0


def get_devices():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, ip_address
        FROM devices
    """)

    devices = cursor.fetchall()

    conn.close()

    return devices


def save_measurement(device_id, ping_ms, packet_loss):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO measurements (
            device_id,
            ping_ms,
            packet_loss
        )
        VALUES (?, ?, ?)
    """, (device_id, ping_ms, packet_loss))

    conn.commit()

    conn.close()


while True:

    print("\nStarter ny scanning...\n")

    devices = get_devices()

    for device_id, name, ip_address in devices:

        print(f"Pinger {name} ({ip_address})...")

        ping_ms, packet_loss = ping_device(ip_address)

        save_measurement(
            device_id,
            ping_ms,
            packet_loss
        )

        print(
            f"{name}: "
            f"{ping_ms} ms | "
            f"Packet loss: {packet_loss}%"
        )

    print("\nVenter 30 sekunder...\n")

    time.sleep(30)