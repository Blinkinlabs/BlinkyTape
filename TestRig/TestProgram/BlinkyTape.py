import serial
import glob

class BlinkyTape:
  def __init__(self, port=None):
    self.port = port

    if port != None:
      self.serial = serial.Serial(port, 115200)
      self.show() # Flush

  def connect(self, port):
    self.port = port

    self.serial = serial.Serial(port, 115200)
    self.show() # Flush

  def disconnct(self):
    self.port = None
    self.serial = None

  def sendPixel(self,r,g,b):
    data = bytearray()
    if r == 255: r = 254
    if g == 255: g = 254
    if b == 255: b = 254
    data.append(r)
    data.append(g)
    data.append(b)
    self.serial.write(str(data))  # change for new python/pyserial?
    self.serial.flush()

  def show(self):
    self.serial.write(chr(255))
    self.serial.flush()

class BlinkyTape_LPD8806:
  def __init__(self, port):
    self.serial = serial.Serial(port, 115200)

  def sendPixel(self,r,g,b):
    data = bytearray()
    data.append(0x80 | (r>>1))
    data.append(0x80 | (g>>1))
    data.append(0x80 | (b>>1))
    self.serial.write(data)
    self.serial.flush()

  def show(self):
    data = bytearray()
    for i in range(0,8):
      data.append(0x00)
    self.serial.write(data)
    self.serial.flush()


if __name__ == "__main__":

  import sys

  LED_COUNT = 60

  parser = optparse.OptionParser()
  parser.add_option("-p", "--port", dest="portname",
                    help="serial port (ex: /dev/ttyUSB0)", default=None)
  (options, args) = parser.parse_args()

  if options.portName != None:
    port = options.portname
  else:
    serialPorts = glob.glob("/dev/cu.usbmodem*")
    port = serialPorts[0]

  bb = BlinkyTape(port)


  while True:

    for x in range(0, LED_COUNT):
      bb.sendPixel(255,255,255)
    bb.show();

    for x in range(0, LED_COUNT):
      bb.sendPixel(0,0,0)
    bb.show()
