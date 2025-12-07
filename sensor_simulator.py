import time
import json
import random
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message

# --- Device connection strings ---
DEVICE_CONNECTIONS = {
    "device_A": "ConnStringForDeviceA",
    "device_B": "ConnStringForDeviceB",
    "device_C": "ConnStringForDeviceC"
}

# --- Device locations ---
DEVICE_LOCATIONS = {
    "device_A": "Lake One",
    "device_B": "Lake Two",
    "device_C": "Lake Three"
}

def generate_telemetry(device_id):
    """Generate telemetry for ASA ice safety analytics."""
    return {
        "device_id": device_id,
        "location": DEVICE_LOCATIONS[device_id],
        "timestamp": datetime.utcnow().isoformat(),

        # --- Fields for Stream Analytics ---
        "ice_thickness_cm": round(random.uniform(10.0, 45.0), 2),
        "surface_temperature_c": round(random.uniform(-15.0, 5.0), 2),
        "snow_accumulation_cm": round(random.uniform(0.0, 40.0), 2),
        "external_temperature_c": round(random.uniform(-20.0, 5.0), 2)
    }

def main():
    #Create IoT Hub clients for each device
    clients = {
        device_id: IoTHubDeviceClient.create_from_connection_string(conn)
        for device_id, conn in DEVICE_CONNECTIONS.items()
    }

    print("Sending telemetry matching ASA requirements every 10 seconds...")

    try:
        while True:
            for device_id, client in clients.items():
                telemetry = generate_telemetry(device_id)
                message_json = json.dumps(telemetry)

                message = Message(message_json)
                message.content_type = "application/json"
                message.content_encoding = "utf-8"

                client.send_message(message)
                print(f"[{device_id}] Sent → {message_json}")

            print("--- batch sent ---\n")
            time.sleep(10)

    except KeyboardInterrupt:
        print("Stopped sending telemetry.")
    finally:
        for client in clients.values():
            client.disconnect()

if __name__ == "__main__":
    main()
