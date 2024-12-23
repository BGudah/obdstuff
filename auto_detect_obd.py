import obd
import serial.tools.list_ports

def find_obd_port():
    """Find the COM port associated with the OBD-II Bluetooth adapter."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Normalize description to uppercase for case-insensitive comparison
        description = port.description.upper()
        if 'OBD' in description or 'ELM327' in description or 'OBDII' in description:
            return port.device
    return None

# Attempt to find the OBD-II COM port
obd_port = find_obd_port()
if obd_port is None:
    print("No OBD-II Bluetooth adapter found. Please ensure it's paired and connected.")
    exit()

print(f"Connecting to OBD-II adapter on port: {obd_port}")

# Establish connection
connection = obd.OBD(port=obd_port)

if not connection.is_connected():
    print("Failed to connect to the OBD-II adapter.")
    print("Please ensure the adapter is paired, the vehicle is in the correct state, and the COM port is correct.")
    exit()

# Select a command, e.g., vehicle speed
cmd = obd.commands.SPEED

# Query the command
response = connection.query(cmd)

# Check if the response is valid
if response.is_null():
    print("No data received for the SPEED command.")
else:
    print(f"Vehicle Speed: {response.value}")  # e.g., 55.0 mph
    print(f"Vehicle Speed (km/h): {response.value.to('kph')}")
