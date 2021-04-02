import serial
from time import sleep
import json
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Make sure Python doesn't flood Arduino with messages
global sent
sent = False

x_vals = []
y_vals = []

def arduino_interact(i):

    message = arduino.readline().decode("utf-8").strip()
    print(message)
    global sent
    if message == 'ready' and not sent:
        # change to 1 after debug
        arduino.write('0'.encode())
        arduino.flush()
        sent = True
    # Prevents saving irrelevant 'ready' and 'busy' messages from arduino
    # This needs a proper condition 
    elif message and message != 'busy' and message != 'starting roo':
        x, y = (message.split(';', 1))
        x = float(x)
        y = float(y)
        
        x_vals.append(x)
        y_vals.append(y)

        plt.cla()
        plt.plot(x_vals, y_vals, color="mediumblue", marker="2",markevery=1, markersize=5, markeredgecolor="orangered")

    #    data_archive['distances'].append(distance)
    #    data_archive['angles'].append(angle)
        # dump to json
    #    with open('sensordata.json', 'w+') as jf:
    #        json.dump(data_archive, jf)
    #    sent = False   

# Connect to Arduino
try:
    arduino = serial.Serial("/dev/cu.linvor-DevB", 9600, timeout=2)
    sleep(1)
    print("Connected")
except:
    print("Check Bluetooth")
    sys.exit()

# laod JSON structure
# with open('sensordata.json') as jf:
#     data_archive = json.load(jf)

# Draw graph
plt.figure(figsize=(10,5))
ani = FuncAnimation(plt.gcf(), arduino_interact, interval=752) 
plt.show(block=True)

# try:
#     while True:
#         ani = FuncAnimation(plt.gcf(), arduino_interact, interval=1000) 
#         # arduino_interact()
#         # sleep(1)
# except KeyboardInterrupt:
#     print("bye-bye")