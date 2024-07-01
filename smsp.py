import bluetooth
import serial
import time

# Target device MAC address and UUID for Message Access Server (MAS)
target_mac_address = 'C4:18:E9:EE:0B:FA'
uuid_mas = '00001132-0000-1000-8000-00805f9b34fb'

def connect_to_mas(device_address, mas_uuid):
    try:
        # Discover services on the device
        print(f"Searching for MAS service ({mas_uuid}) on device {device_address}")
        services = bluetooth.find_service(address=device_address, uuid=mas_uuid)

        if len(services) > 0:
            service = services[0]
            port = service['port']
            name = service['name']
            host = service['host']
            print(f"Connecting to {name} on {host}:{port}")

            # Create a Bluetooth socket and connect to the service
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((host, port))

            print(f"Connected to {host} on port {port}")
            return sock  # Return the Bluetooth socket object
        else:
            print(f"MAS service not found on device with address {device_address}")
            return None
    
    except bluetooth.btcommon.BluetoothError as bterror:
        print(f"Bluetooth error: {bterror}")
        return None
    except Exception as e:
        print(f"Connection to MAS failed: {e}")
        return None

def send_at_command(sock, command, expected_response="OK", timeout=10):
    """
    Send an AT command and wait for the expected response.
    """
    try:
        print(f"Sending command: {command.strip()}")
        sock.send((command + "\r\n").encode())
        
        response = b''
        sock.settimeout(timeout)  # Set a timeout for receiving data
        while True:
            data = sock.recv(1024)
            if not data:
                break
            response += data
            if expected_response.encode() in response:
                break

        response_str = response.decode().strip()
        print(f"Received response: {response_str}")
        return response_str

    except Exception as e:
        print(f"Failed to send command {command}: {e}")
        return ""

def send_sms(sock, recipient, message):
    try:
        # Initialize modem and set to text mode
        send_at_command(sock, "AT")
        send_at_command(sock, "AT+CMGF=1")
        send_at_command(sock, "AT+CMEE=2")

        # Send SMS command with recipient number
        response = send_at_command(sock, f'AT+CMGS="{recipient}"', expected_response=">")
        if ">" in response:
            # Send message text and Ctrl+Z to indicate the end of the message
            send_at_command(sock, message + "\x1A", expected_response="OK", timeout=20)

            print(f"Message sent successfully.")
        else:
            print(f"Failed to get '>' prompt: {response}")

    except Exception as e:
        print(f"Failed to send message: {e}")

    finally:
        # Close the Bluetooth socket
        sock.close()

def main():
    sock = connect_to_mas(target_mac_address, uuid_mas)
    if sock:
        try:
            recipient = "+251996877474"  # Replace with the recipient's number
            message = "Hello, this is a test SMS sent via Bluetooth!"
            send_sms(sock, recipient, message)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sock.close()
    else:
        print("Connection to MAS failed.")

if __name__ == "__main__":
    main()
