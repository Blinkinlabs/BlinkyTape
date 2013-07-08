#! /usr/bin/env python
import serial
import time
import glob
import BlinkyTape


STK_OK      = 0x10
STK_INSYNC  = 0x14
CRC_EOP     = 0x20
BT_COMMAND  = 0x21

class RemoteArduino:
  """Class to control an Arduino remotely. A light Firmata-like thing."""
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
    response = self.sendCommand('m', pin, 2)
    analogValue = (response[0]*256 + response[1])/10
    return float(analogValue)

  def digitalRead(self, pin):
    """Read the value of a digital pin"""
    return self.sendCommand('r', pin, 1)

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

class ArduinoPin:
  def __init__(self, name, number, net = None, suppressHigh = False, suppressLow = False):
    self.name = name
    self.number = number

    if(net == None):
      self.net = name
    else:
      self.net = net

    self.suppressHigh = suppressHigh
    self.suppressLow = suppressLow

  def __str__(self):
    return self.name


class TestRig:
  """ Class that represents a BlinkyTape test rig"""
  def __init__(self, port, measurementPins, relayPins, shortTestPins):
    """Initialize a connection to a test rig"""
    self.arduino = RemoteArduino(port)
    remoteVersion = self.arduino.getRemoteVersion()
    if remoteVersion < 1:
      raise Exception("Remote version (" + hex(remoteVersion) + ") too low, upgrade the Arduino sketch")

    self.measurementPins = measurementPins
    self.relayPins = relayPins
    self.shortTestPins = shortTestPins

  def resetState(self):
    """ Set all relay pins to output and low, and all short test pins to high-impedance inputs """
    for pin in self.relayPins:
      self.arduino.digitalWrite(pin.number, 'LOW')
      self.arduino.pinMode(pin.number, 'OUTPUT')

    for pin in self.shortTestPins:
      self.arduino.pinMode(pin.number, 'INPUT')

    # TODO: reset analog pins?

  def enableRelay(self, relayName):
    """ Enable an output relay """
    for pin in self.relayPins:
      if pin.name == relayName:
        self.arduino.digitalWrite(pin.number, 'HIGH')
        return
    raise Exception("Relay " + relayName + "not found!")
    
  def disableRelay(self, relayName):
    """ Disable an output relay """
    for pin in self.relayPins:
      if pin.name == relayName:
        self.arduino.digitalWrite(pin.number, 'LOW')
        return
    raise Exception("Relay " + relayName + "not found!")

  def measure(self, measurementName):
    """ Read a measurement pin """
    for pin in self.measurementPins:
      if pin.name == measurementName:
        return self.arduino.analogRead(pin.number)
    raise Exception("Measurement pin " + measurementName + "not found!")
    

  def shortTest(self):
    """ Perform an n*n short test on the shortTestPins """
    faults = []

    # Step through each pin, setting it as a low output, then reading in the value of all other pins
    for pin in self.shortTestPins:
      if pin.suppressLow == True:
        continue

      # TODO: add a list of suppressed pins (eg, VCC) that should never be taken low

      # Short everything together by setting it to high output, to discharge passives
      for p in self.shortTestPins:
        self.arduino.pinMode(p.number, 'OUTPUT')
        self.arduino.digitalWrite(p.number, 'LOW')
      time.sleep(.2)

      # Reset all pins to inputs
      for p in self.shortTestPins:
        self.arduino.pinMode(p.number, 'INPUT')

      # Set the left-side pin to low output
      print 'Setting pin ' + str(pin) + ' low'
      self.arduino.pinMode(pin.number, 'OUTPUT')
      self.arduino.digitalWrite(pin.number, 'LOW')

      # Now, iterate through all the other pins
      for inputPin in self.shortTestPins:
        if ((pin.name != inputPin.name) and (inputPin.suppressHigh == False)):
          self.arduino.pinMode(inputPin.number, 'INPUT_PULLUP')
          time.sleep(.05)

          shorted = (0 == self.arduino.digitalRead(inputPin.number))
          expectedShorted = (inputPin.net == pin.net)

          if shorted != expectedShorted:
            # sort the pins alphabetically
#            if(pin.name < inputPin.name):
              faults.append((pin.name, inputPin.name, expectedShorted, shorted))
#            else:
#              faults.append((inputPin.name, pin.name, expectedShorted, shorted))

          self.arduino.pinMode(inputPin.number, 'INPUT')
   
    # TODO: don't put dupicaltes into the list in the first place... 
    return sorted(list(dict.fromkeys(faults)))
    


# List of pins that are connected to analog sensors on the board
measurementPins = [
  ArduinoPin('DUT_CURRENT',    0),  # Note: an analog pin!
  ]

# List of pins that control a relay on the test rig
relayPins = [
  ArduinoPin('EN_USB_VCC_LIMIT', 8),
  ArduinoPin('EN_USB_VCC',       9),
  ArduinoPin('EN_USB_DATA',     10),
  ArduinoPin('EN_USB_GND',      11),
  ArduinoPin('EN_LED_OUT',      23),
  ]
  

# List of pins that are connected directly to an I/O pin on the DUT,
# that should be used to do an n*n short test
# For nodes with reverse protection diodes (eg, VCC and GND), specifcy
# 'suppressHigh' to prevent them from being pulled higher than any other
# nets, and 'suppressLow' to prevent them from being pulled lower than any
# other nets.
shortTestPins = [
  ArduinoPin('DUT_USB_GND',    19, net='GND', suppressHigh=True), # Analog input pins as digital, A0 = 18, A1 = 19, etc
  ArduinoPin('DUT_OUT_GND',    22, net='GND', suppressHigh=True),
  ArduinoPin('DUT_USB_VCC',    20, net='VCC', suppressLow=True),
  ArduinoPin('DUT_OUT_VCC',    21, net='VCC', suppressLow=True),
  ArduinoPin('ICSP_RESET',      2),  # Regular digital pins
  ArduinoPin('DUT_A10',         3),
  ArduinoPin('DUT_D11',         4),
  ArduinoPin('DUT_D7',          5),
  ArduinoPin('DUT_D13',         6),
  ArduinoPin('DUT_USB_SHIELD',  7),
  ArduinoPin('TAP_USB_D-',     12),
  ArduinoPin('TAP_USB_D+',     13),
  ArduinoPin('ICSP_MISO',      14),   # ICSP pins
  ArduinoPin('ICSP_SCK',       15),
  ArduinoPin('ICSP_MOSI',      16),
  ]


testRig = TestRig('/dev/tty.usbmodemfd1221', measurementPins, relayPins, shortTestPins)

# Test procedure:
# 0. reset board state (relays, etc)
print "Resetting board state..."
testRig.resetState()

# 1. n*n short test
if False:
  print "Running n*n short test..."
  faults = testRig.shortTest()
  for fault in faults:
    print fault

# 2. vcc current-limited
CURRENT_A = 994
CURRENT_B = -2.3

if False:
  MIN_LIMITED_CURRENT= 50
  MAX_LIMITED_CURRENT = 70

  print "Running current limited VCC test..."
  testRig.enableRelay('EN_USB_GND')
  testRig.enableRelay('EN_USB_VCC_LIMIT')
  time.sleep(.5)
  limitedCurrent = CURRENT_B*(testRig.measure('DUT_CURRENT') - CURRENT_A)
  print limitedCurrent
  if limitedCurrent < MIN_LIMITED_CURRENT:
    # TODO: Recover gracefully here!
    raise Exception("Open detected: Current draw (" + str(limitedCurrent) + ") below setpoint (" + str(MIN_LIMITED_CURRENT) + ")")
  if limitedCurrent > MAX_LIMITED_CURRENT:
    # TODO: Recover gracefully here!
    raise Exception("Short detected: Current draw (" + str(limitedCurrent) + ") exceeds setpoint (" + str(MAX_LIMITED_CURRENT) + ")")

  testRig.disableRelay('EN_USB_VCC_LIMIT')
  testRig.disableRelay('EN_USB_GND')

# 3. vcc full power current test
if False:
  MIN_OPERATING_CURRENT = 25
  MAX_OPERATING_CURRENT = 35

  print "Measuring unlimted VCC test..."
  testRig.enableRelay('EN_USB_GND')
  testRig.enableRelay('EN_USB_VCC')
  time.sleep(.5)
  fullCurrent = CURRENT_B*(testRig.measure('DUT_CURRENT') - CURRENT_A)
  print fullCurrent
  if fullCurrent > MAX_OPERATING_CURRENT:
    # TODO: Recover gracefully here!
    raise Exception("Device draws too much power: Current draw (" + str(fullCurrent) + ") exceeds setpoint (" + str(MAX_OPERATING_CURRENT) + ")")
  if fullCurrent < MIN_OPERATING_CURRENT:
    # TODO: Recover gracefully here!
    raise Exception("Device draws too little power: Current draw (" + str(fullCurrent) + ") below setpoint (" + str(MIN_OPERATING_CURRENT) + ")")

  testRig.disableRelay('EN_USB_VCC')
  testRig.disableRelay('EN_USB_GND')

# 4. program firmware
# 5. USB enumeration test
dutPort = ''
if True:
  # Scan for all connected devices; platform dependent
  time.sleep(1)
  originalPorts = set(glob.glob("/dev/cu.usbmodem*"))

  testRig.enableRelay('EN_USB_GND')
  testRig.enableRelay('EN_USB_VCC')
  testRig.enableRelay('EN_USB_DATA')
  print CURRENT_B*(testRig.measure('DUT_CURRENT') - CURRENT_A)
  time.sleep(2)

  finalPorts =set(glob.glob("/dev/cu.usbmodem*"))

  newPorts = finalPorts - originalPorts
  if len(newPorts) != 1:
    raise Exception("DUT did not enumerate as a USB device- expected 1 serial device, saw " + str(len(newPorts)))
  
  dutPort = list(newPorts)[0]
  print "DUT enumerated as device " + dutPort

  testRig.disableRelay('EN_USB_DATA')
  testRig.disableRelay('EN_USB_VCC')
  testRig.disableRelay('EN_USB_GND')

# 6. LED output current test
if True:
  testRig.enableRelay('EN_USB_DATA')
  testRig.enableRelay('EN_USB_VCC')
  testRig.enableRelay('EN_USB_GND')
  time.sleep(.5)

  dut = BlinkyTape.BlinkyTape(dutPort, "WS2811")

  for j in range (0, 254):
    for x in range(0, 60):
      dut.sendPixel(j,j,j)
    dut.show();
    for x in range(0, 60):
      dut.sendPixel(j,j,j)
    dut.show();
    for x in range(0, 60):
      dut.sendPixel(j,j,j)
    dut.show();
    time.sleep(1)
    print str(j) + ": " + str(CURRENT_B*(testRig.measure('DUT_CURRENT') - CURRENT_A))

#  while True:
#    for x in range(0, 60):
#      dut.sendPixel(255,255,255)
#    dut.show();
#    for x in range(0, 60):
#      dut.sendPixel(255,255,255)
#    dut.show();
#
#    time.sleep(.5)
#    print ("h: "),
#    print CURRENT_B*(testRig.measure('DUT_CURRENT') - CURRENT_A),
#
#    for x in range(0, 60):
#      dut.sendPixel(0,0,0)
#    dut.show()
#    for x in range(0, 60):
#      dut.sendPixel(0,0,0)
#    dut.show()
#    time.sleep(.5)
#    print ("l: "),
#    print CURRENT_B*(testRig.measure('DUT_CURRENT') - CURRENT_A)
