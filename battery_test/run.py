import serial

device = serial.Serial("/dev/tty.usbmodemfd121", 19200)

file = open("output.csv", "a");

while True:
  file.write(device.readline())
  file.flush()
