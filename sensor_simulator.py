import os
import json
import time
import random
from datetime import datetime
from dotenv import load_dotenv
from azure.iot.device import IoTHubDeviceClient, Message

#Load environment variables from .env
load_dotenv()

#Device environment variable names
DEVICE_ENV_VARS = {
    "device_A": "IOTHUB_DEVICE_A",
    "device_B": "IOTHUB_DEVICE_B",
    "device_C": "IOTHUB_DEVICE_C",
}

#Device locations (safe for Cosmos DB partition key)
DEVICE_LOCATIONS = {
    "device_A": "Dow's Lake",
    "device_B": "Fifth Avenue",
    "device_C": "NAC",
}

def load_connection_strings():
    device_connections = {}
    for device_id, env_var in DEVICE_ENV_VARS.items():
        conn = os.getenv(env_var)
        if not conn:
            raise ValueError(f"Missing connection string: '{env_var}' not set in .env")
        device_connections[device_id] = conn
    return device_connections

def generate_telemetry(device_id):
    """
    Generate telemetry for Rideau Canal ice safety monitoring.
    """
    return {
        "device_id": device_id,
        "location": DEVICE_LOCATIONS[device_id],
        "timestamp": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "ice_thickness_cm": round(random.uniform(10.0, 45.0), 2),
        "surface_temperature_c": round(random.uniform(-20.0, 5.0), 2),
        "snow_accumulation_cm": round(random.uniform(0.0, 50.0), 2),
        "external_temperature_c": round(random.uniform(-25.0, 5.0), 2),
    }


def main():
    device_connections = load_connection_strings()
    clients = {d: IoTHubDeviceClient.create_from_connection_string(c) for d, c in device_connections.items()}

    print("Sending telemetry every 10 seconds. Press Ctrl+C to stop.")
    try:
        while True:
            for device_id, client in clients.items():
                telemetry = generate_telemetry(device_id)
                message = Message(json.dumps(telemetry))
                message.content_type = "application/json"
                message.content_encoding = "utf-8"
                client.send_message(message)
                print(f"[{device_id}] Sent → {telemetry}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Telemetry stopped.")
    finally:
        for client in clients.values():
            client.disconnect()

if __name__ == "__main__":
    main()

