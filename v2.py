import serial


incoming_buffer = []

ser = serial.Serial("/dev/tty.usbserial-AD012345", 9600, timeout=1)
print "Decoder Link Initialized"


def update():
    while ser.in_waiting > 0:

        new_data = ser.read(ser.in_waiting)

        new_hex_data = new_data.encode("hex")
        print new_hex_data
        incoming_buffer.append(new_hex_data)

def valid_command_received():
    return len(incoming_buffer) >= 20

def get_command():
    return incoming_buffer.join("")
    incoming_buffer = []

while(True):
    update()
    if valid_command_received():
        print get_command()
