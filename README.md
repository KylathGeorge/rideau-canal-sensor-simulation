# CST8916 Final Project: Real-time Monitoring System for Rideau Canal Skateway

## Name: Kylath Mamman George

## Student Number: 041198835

## Overview

This is Python code that simulates 3 IoT devices n 3 different locations which sends data every 10 seconds. The data sent will be:

- Ice Thickness (cm)
- Surface Temperature (°C)
- Snow Accumulation (cm)
- External Temperature (°C)
  
## Prequisites

- Python Installed
- Azure Account
  
## Installation

1. Install requirements

```command
pip install -r requirements.txt
python sensor_simulator.py
```

## Usage

The code will automatically simulate sending data every 10 seconds once it is running.

## Code Structure

In the code we have the python libraries imported with dotenv loading the environment variables that holds the Cosmos DB secrets.

The first part of this code holds the variables that points towards the IoT devices on Azure IoT hub. The second part holds the location strings for each device.

```python
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
```

The functiion `load_connection_strings()` loads the device connection strings from the `.env` and returns them in a dictionary. For example: `device_id = "device_A", env_var = "IOTHUB_DEVICE_A"`. The second function `generate_telemetry(device_id)` is the function that generates the fake data for the devices.

In `main()` IoT hub clients are created with three separate persistent connections, one per device. After that an infinite loop of sending the generated telemetry that is converted to JSON message is sent to the IoT Hub.

## Sensor Data Format

### JSON Schema

```JSON
{
  "device_id": "string",
  "location": "string",
  "timestamp": "string",
  "ice_thickness_cm": "number",
  "surface_temperature_c": "number",
  "snow_accumulation_cm": "number",
  "external_temperature_c": "number"
}
```

### Example Output

```command
{
  'device_id': 'device_A',
  'location': "Dow's Lake",
  'timestamp':'2025-12-08T21:26:42Z',
  'ice_thickness_cm': 23.13,
  'surface_temperature_c': -5.44,
  'snow_accumulation_cm': 10.78,
  'external_temperature_c': -18.23
}
```
