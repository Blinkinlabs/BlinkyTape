import serial
import time

class blinkyBoard:
  def init(self, port, baud):
    self.serial = serial.Serial(port, baud)

  def sendPixel(self,r,g,b):
    data = bytearray()
    if r == 255: r = 254
    if g == 255: g = 254
    if b == 255: b = 254
    data.append(r)
    data.append(g)
    data.append(b)
    self.serial.write(data)
    self.serial.flush()

  def flush(self):
    self.serial.write(chr(255))
    self.serial.flush()

  
b = blinkyBoard()
b.init('/dev/cu.usbmodem1d11', 115200)

while True:

  b.flush() # Using 0xFF as a start latch semaphore

  for x in range(0, 60):
    b.sendPixel(255,255,255)
  b.flush();

  for x in range(0, 60):
    b.sendPixel(0,0,0)

  b.flush()


  print "draw"
