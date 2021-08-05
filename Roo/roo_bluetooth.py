import bluetooth
import sys
from time import sleep

# incoming data sample
sample = """
344.7,-966.7
569.9,-931.1
670.7,-915.1
-438.4,-1136.3
-318.0,-1071.7
-91.8,-1035.9
120.5,-1002.3
344.7,-966.7
569.9,-931.1
"""

roo_addr = "98:D3:31:F3:F6:97"
port = 1
size = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


def roomba_connect():
    connected = False
    while not connected:
        try:
            sock.connect((roo_addr, port))
            connected = True
            print("Connected to Roomba. Awaiting Data.")
        except:
            print("Connection failed, retrying in 5 seconds...")
            sleep(5)


roomba_connect()

while True:
    try:
        data_string = ''
        while ";" not in data_string:
            try:
                data = sock.recv(size).decode()
                if not data.isspace():
                    data_string += data
            except:
                print("Socket disconnected. Attempting to reconnect")
                roomba_connect()
        print(data_string[:-1])
    except KeyboardInterrupt:
        print("Closing")
        sock.close()
        sys.exit()