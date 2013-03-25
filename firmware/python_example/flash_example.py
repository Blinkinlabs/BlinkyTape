import serial
import time

class blinkyBoard:
  def init(self, port, baud):
    self.serial = serial.Serial(port, baud)

  def sendPixel(self,r,g,b):
    data = bytearray()
    data.append(0x80 | (r>>1))
    data.append(0x80 | (g>>1))
    data.append(0x80 | (b>>1))
    self.serial.write(data)
    self.serial.flush()

  def sendBreak(self):
    data = bytearray()
    for i in range(0,8):
      data.append(0x00)
    self.serial.write(data)
    self.serial.flush()

b = blinkyBoard()
b.init('/dev/cu.usbmodemfa131', 57600)

b.sendBreak()
while True:
  b.sendPixel(0,0,255)
  for i in range(0,30):
    b.sendPixel(255, 0, 0)
  b.sendPixel(0,0,255)
  b.sendBreak()
  time.sleep(.01)

  b.sendPixel(255,0,0)
  for i in range(0,30):
    b.sendPixel(0, 0, 255)
  b.sendPixel(255,0,0)
  b.sendBreak()
  time.sleep(.01)
