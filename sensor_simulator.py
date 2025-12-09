import os
import json
import time
import random
from datetime import datetime
from dotenv import load_dotenv
from azure.iot.device import IoTHubDeviceClient, Message

#Load environment variables from .env
load_dotenv()

#Device environment variable names with respective connection strings
DEVICE_ENV_VARS = {
    "device_A": "IOTHUB_DEVICE_A",
    "device_B": "IOTHUB_DEVICE_B",
    "device_C": "IOTHUB_DEVICE_C",
}

#Device locations mapped to each device name for telemetry data and also used as the partition key
DEVICE_LOCATIONS = {
    "device_A": "Dow's Lake",
    "device_B": "Fifth Avenue",
    "device_C": "NAC",
}

# Load connection strings from environment variables and stop if connection string is missing, returns a dictionary mapping device id to connection string
def load_connection_strings():
    device_connections = {}
    #loop through each device and get connection string from environment variable
    for device_id, env_var in DEVICE_ENV_VARS.items():
        #pass it to conn variable after reading the environment variable
        conn = os.getenv(env_var)
        #if connection string is missing raise a value error
        if not conn:
            raise ValueError(f"Missing connection string: '{env_var}' not set in .env")
        #add device id and connection string to device_connections dictionary
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
    #Create IoT Hub device clients for each deviceq
    #Each client is created using the connection string from device_connections dictionary, stored in a new dictionary called clients
    clients = {d: IoTHubDeviceClient.create_from_connection_string(c) for d, c in device_connections.items()}

    print("Sending telemetry every 10 seconds. Press Ctrl+C to stop.")
    #Infinite loop to send telemetry every 10 seconds for each device id
    try:
        while True:
            for device_id, client in clients.items():
                telemetry = generate_telemetry(device_id)
                #Create message object with telemetry data in JSON format
                message = Message(json.dumps(telemetry))
                message.content_type = "application/json"
                message.content_encoding = "utf-8"
                #sends the message
                client.send_message(message)
                print(f"[{device_id}] Sent → {telemetry}")
            #Wait for 10 seconds before sending the next batch of telemetry
            time.sleep(10)
    except KeyboardInterrupt:
        print("Telemetry stopped.")
    finally:
        for client in clients.values():
            client.disconnect()

if __name__ == "__main__":
    main()

