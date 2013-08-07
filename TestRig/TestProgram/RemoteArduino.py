import serial

STK_OK      = 0x10
STK_INSYNC  = 0x14
CRC_EOP     = 0x20
BT_COMMAND  = 0x21

class RemoteArduino:
  """Class to control an Arduino remotely. A light Firmata-like thing.
     The Arduino must be loaded with the TestProgram_Arduino sketch.
  """
  def __init__(self, port):
    """ Open a connection to an arduino running the SerialTester sketch.
    port: Serial port device name, for example: '/dev/cu.usbmodelfa1321'
    """
    self.serial = serial.Serial(port)

  def sendCommand(self, command, channel, responseCount):
    self.serial.write(chr(BT_COMMAND))
    self.serial.write(command)
    self.serial.write(chr(channel))
    self.serial.write(chr(CRC_EOP))
    # TODO: Read back response?
    # response is: STK_INSYNC, [data], STK_OK
    response = ord(self.serial.read(1))
    if(STK_INSYNC != response):
      raise Exception(" Bad response from test rig. Expected: " + hex(STK_INSYNC) + ", got: " + hex(response))

    returnData = []
    for i in range(0, responseCount):
      returnData.append(ord(self.serial.read(1)))

    response = ord(self.serial.read(1))
    if(STK_OK != response):
      raise Exception(" Bad response from test rig. Expected: " + hex(STK_OK) + ", got: " + hex(response))
    
    return returnData

  def getRemoteVersion(self):
    return self.sendCommand('v', 1, 1)

  def analogRead(self, pin):
    """Read the value of an analog pin"""
    # TODO: How to send float cleanly?
    counts = 100
    analogValue = 0
    for i in range(0, counts):
      response = self.sendCommand('m', pin, 2)
      analogValue += (response[0]*256 + response[1])
    return float(analogValue/counts)

  def digitalRead(self, pin):
    """Read the value of a digital pin"""
    return (self.sendCommand('r', pin, 1))[0]

  def pinMode(self, pin, mode):
    """Change the mode of a digital pin"""
    if mode == 'OUTPUT':
      self.sendCommand('o', pin, 0)
    elif mode == 'INPUT':
      self.sendCommand('i', pin, 0)
    elif mode == 'INPUT_PULLUP':
      self.sendCommand('p', pin, 0)
    else:
      raise Exception("Mode " + mode + " not understood")

  def digitalWrite(self, pin, value):
    """Change the state of a digital pin configured as output"""
    if value == 'HIGH':
      self.sendCommand('h', pin, 0)
    elif value == 'LOW':
      self.sendCommand('l', pin, 0)
    else:
      raise Exception("Value" + value + " not understood")
