import dbus

# Initialize dbus session
bus = dbus.SystemBus()

# Replace with the actual device path found through discovery
device_path = "/org/bluez/hci1/dev_C4_18_E9_EE_0B_FA"

# Connect to the MessageAccess1 interface of the device
map_interface = dbus.Interface(bus.get_object("org.bluez", device_path),
                               "org.bluez.MessageAccess1")

def send_sms(recipient, message):
    try:
        # Construct dbus types for message properties
        message_properties = {
            "Recipient": dbus.String(recipient),
            "Body": dbus.String(message),
            "Transparent": dbus.Boolean(False),
            "Retry": dbus.Boolean(False)
        }

        # Call SendMessage method
        map_interface.SendMessage(dbus.Dictionary(message_properties, signature='sv'))

        print(f"SMS sent to {recipient}: {message}")
    except dbus.exceptions.DBusException as e:
        print(f"Failed to send SMS: {e}")

# Example usage
phone_number = "+251914+++++"
message = "Hello, this is a test SMS!"
send_sms(phone_number, message)
