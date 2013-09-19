import serial
import time

class Blinkyboard(object):
  def __init__(self, port):
    self.serial = serial.Serial(port, 115200)
    self.show() # Flush

  def sendPixel(self,r,g,b):
    data = ""
    if r == 255: r = 254
    if g == 255: g = 254
    if b == 255: b = 254
    data = chr(r) + chr(g) + chr(b)
    self.serial.write(data)
    self.serial.flush()

  def show(self):
    self.serial.write(chr(255))
    self.serial.flush()


if __name__ == "__main__":

  import sys

  LED_COUNT = 60
  bb = None

  if len(sys.argv) > 1:
    bb = Blinkyboard(sys.argv[1], "WS2811")

  else:
    import os
    import re
    regex = re.compile(".*usbmodem.*")
   
    for filenames in os.walk('/dev'):
      for filename in filenames[2]:
        if regex.findall(filename):
          bb = Blinkyboard(os.path.join("/dev", filename), "WS2811")

  if not bb:
    sys.exit("Usage: python test.py (path to serial port)")


  while True:

    for x in range(0, LED_COUNT):
      bb.sendPixel(255,255,255)
    bb.show();

    for x in range(0, LED_COUNT):
      bb.sendPixel(0,0,0)
    bb.show()

