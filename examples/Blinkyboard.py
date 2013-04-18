import serial
import time

class Blinkyboard(object):
  def __new__(typ, *args, **kwargs):

    if kwargs['gamma'] and (type(kwargs['gamma']) != type([]) or len(kwargs['gamma']) != 3):
      raise Exception("Bad Gamma correction value. Use a list with three values.")

    if "WS2811" in args:
      return Blinkyboard_WS2811(args[0], args[1], kwargs['gamma'])
    elif "LPD8806" in args:
      return Blinkyboard_LPD8806(args[0], args[1], kwargs['gamma'])

class Blinkyboard_WS2811:
  def __init__(self, port, count, gamma = None):
    self.serial = serial.Serial(port, 115200)
    self.LED_COUNT = count
    self.gamma = gamma
    self.show() # Flush

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

  def show(self):
    self.serial.write(chr(255))
    self.serial.flush()

  def gamma(self, input, tweak):
    if not self.gamma: return input
    return int(pow(input/256.0, tweak) * 256)

  def allOn(self):
    for _ in range(0, self.LED_COUNT):
      self.sendPixel(0,0,0)
    self.show()

  def allOff(self):
    for _ in range(0, self.LED_COUNT):
      self.sendPixel(0,0,0)
    self.show()


class Blinkyboard_LPD8806:
  def __init__(self, port, count, gamma = None):
    self.serial = serial.Serial(port, 115200)
    self.LED_COUNT = count
    self._gamma = gamma
    if gamma and (type(gamma) != type([]) or len(gamma) != 3):
      raise Exception("Bad Gamma correction value. Use a list with three values.")

  def sendPixel(self,r,g,b):
    data = bytearray()
    data.append(0x80 | (self.gamma(g, self._gamma[1])>>1))
    data.append(0x80 | (self.gamma(r, self._gamma[0])>>1))
    data.append(0x80 | (self.gamma(b, self._gamma[2])>>1))
    self.serial.write(data)
    self.serial.flush()

  def show(self):
    data = bytearray()
    for i in range(0,8):
      data.append(0x00)
    self.serial.write(data)
    self.serial.flush()

  def gamma(self, input, tweak):
    if not self._gamma: return input
    return int(pow(input/256.0, tweak) * 256)

  def allOn(self):
    for _ in range(0, self.LED_COUNT):
      self.sendPixel(255,255,255)
    self.show()

  def allOff(self):
    for _ in range(0, self.LED_COUNT):
      self.sendPixel(0,0,0)
    self.show()


if __name__ == "__main__":

  import sys

  BOARD_TYPE="LPD8806"
  LED_COUNT = 32;
  bb = None
  gamma = [1,1,1]

  if len(sys.argv) > 1:
    bb = Blinkyboard(sys.argv[1], LED_COUNT, BOARD_TYPE, gamma=gamma)

  else:
    import os
    import re
    regex = re.compile(".*usbmodem.*")
   
    for filenames in os.walk('/dev'):
      for filename in filenames[2]:
        if regex.findall(filename):
          bb = Blinkyboard(os.path.join("/dev", filename), BOARD_TYPE, gamma=gamma)
          break

  if not bb:
    sys.exit("Usage: python test.py (path to serial port)")


  while True:
    bb.allOn()
    bb.allOff()
