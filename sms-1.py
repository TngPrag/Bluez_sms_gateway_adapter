import bluetooth
import time

def connect_bluetooth_device(device_address, port):
    """
    Connect to a Bluetooth device using RFCOMM protocol.
    """
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((device_address, port))
        sock.settimeout(10.0)  # Increase timeout to 10 seconds
        print(f"Connected to {device_address} on port {port}")
        return sock
    except bluetooth.BluetoothError as e:
        print(f"Failed to connect: {e}")
        return None

def send_command(sock, command, wait_time=2.0):
    """
    Send a command to the Bluetooth socket and return the response.
    """
    try:
        print(f"Sending command: {command.strip()}")
        sock.send(command)
        time.sleep(wait_time)  # Wait for the device to process the command
        response = sock.recv(1024).decode()
        print(f"Received response: {response}")
        return response
    except bluetooth.BluetoothError as e:
        print(f"Bluetooth error: {e}")
        return None
    except Exception as e:
        print(f"General error: {e}")
        return None

def send_sms(sock, recipient, message):
    """
    Send an SMS message using the connected Bluetooth socket.
    """
    try:
        # Initialize the modem
        response = send_command(sock, 'ATZ\r')
        if response:
            print(f"ATZ response: {response}")
        else:
            print("No response to ATZ")

        # Set SMS mode to text
        response = send_command(sock, 'AT+CMGF=1\r')
        if response:
            print(f"AT+CMGF=1 response: {response}")
        else:
            print("No response to AT+CMGF=1")

        # Set recipient phone number
        response = send_command(sock, f'AT+CMGS="{recipient}"\r')
        if response:
            print(f"AT+CMGS response: {response}")
        else:
            print("No response to AT+CMGS")

        # Send the message body
        response = send_command(sock, message + '\r')
        if response:
            print(f"Message body response: {response}")
        else:
            print("No response to message body")

        # Send end of message character
        response = send_command(sock, chr(26), wait_time=5.0)  # Allow more time for this step
        if response:
            print(f"Message send response: {response}")
        else:
            print("No response to message send")
    except Exception as e:
        print(f"Error sending SMS: {e}")

# Device and connection details
device_address = "C4:18:E9:EE:0B:FA"  # Replace with your device's MAC address
port = 4  # Replace with the actual port

# Connect to the device
sock = connect_bluetooth_device(device_address, port)
if sock:
    recipient = "+251914232223"  # Replace with the recipient's phone number
    message = "Hello, this is a test SMS."

    # Send the SMS
    send_sms(sock, recipient, message)

    # Close the socket
    sock.close()

