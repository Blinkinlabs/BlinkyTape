import time

import DetectPlatform
import RemoteArduino



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

class MeasurementPin():
  def __init__(self, name, number, M, B):
    self.name = name
    self.number = number
    self.M = M
    self.B = B

  def __str__(self):
    return self.name


class TestRig:
  """ Class that represents a BlinkyTape test rig"""

  def __init__(self, port, measurementPins, relayPins, shortTestPins):
    self.measurementPins = measurementPins
    self.relayPins = relayPins
    self.shortTestPins = shortTestPins

    # TODO: don't connect here?
    self.connect(port)

  def connect(self, port):
    """Initialize a connection to a test rig"""
    self.port = port
    self.arduino = RemoteArduino.RemoteArduino(port)
    remoteVersion = self.arduino.getRemoteVersion()
    if remoteVersion < 1:
      raise Exception("Remote version (" + hex(remoteVersion) + ") too low, upgrade the Arduino sketch")

    self.resetState()

  def disconnect(self):
    self.arduino = None

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

  def setOutputLow(self, pinName):
    """ Disable an output relay """
    for pin in self.shortTestPins:
      if pin.name == pinName:
        self.arduino.pinMode(pin.number, 'OUTPUT')
        self.arduino.digitalWrite(pin.number, 'LOW')
        return
    raise Exception("Pin" + pinName + "not found!")

  def setInput(self, pinName):
    """ Disable an output relay """
    for pin in self.shortTestPins:
      if pin.name == pinName:
        self.arduino.pinMode(pin.number, 'INPUT')
        return
    raise Exception("Pin" + pinName + "not found!")

  def measure(self, measurementName):
    """ Read a measurement pin """
    for pin in self.measurementPins:
      if pin.name == measurementName:
        return pin.M*(self.arduino.analogRead(pin.number) + pin.B)

    raise Exception("Measurement pin " + measurementName + "not found!")
    

  def shortTest(self, pinName):
    """ Perform a short test between the given pin and all other pins by pulling the given pin low,
        then each other pin high using a weak pull-up, and measuring the other pin
    """
    faults = []

    # Step through each pin, setting it as a low output, then reading in the value of all other pins
    for pin in self.shortTestPins:
      if pin.name != pinName:
        continue

      # Short everything together by setting it to high output, to discharge passives
      for p in self.shortTestPins:
        self.arduino.pinMode(p.number, 'OUTPUT')
        self.arduino.digitalWrite(p.number, 'LOW')
      time.sleep(.2)

      # Reset all pins to inputs
      for p in self.shortTestPins:
        self.arduino.pinMode(p.number, 'INPUT_PULLUP')

      # Set the left-side pin to low output
      self.arduino.pinMode(pin.number, 'OUTPUT')
      self.arduino.digitalWrite(pin.number, 'LOW')


      # Now, iterate through all the other pins
      # There are a few cases here:
      # - If neither pin nor inputPin are suppressHigh nor suppressLow, test them against each other.
      # - If pin is suppresslow or inputPin is suppresshigh, only test if they are on the same net.
      for inputPin in self.shortTestPins:
        if pin.name != inputPin.name:
          if (pin.suppressLow or inputPin.suppressHigh) and (pin.net != inputPin.net):
            continue

          shorted = (0 == self.arduino.digitalRead(inputPin.number))
          expectedShorted = (inputPin.net == pin.net)

          if shorted != expectedShorted:
            faults.append((pin.name, inputPin.name, expectedShorted, shorted))
   
    return sorted(list(dict.fromkeys(faults)))

def MakeDefaultRig():
  """ Actually we only have one version of the hardware. Make a class instance to represent it.
  """
  serialPorts = DetectPlatform.ListSerialPorts()
  port = serialPorts[0]

  # List of pins that are connected to analog sensors on the board
  measurementPins = [
    MeasurementPin('DUT_CURRENT',0, 1, 0),  # Note: an analog pin! Values determined by experiment
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
    ArduinoPin('ICSP_RESET',      0),  # Regular digital pins
    ArduinoPin('DUT_A10',         1),
    # 2,3 used by I2C port for current sensor
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
  

  return TestRig(port, measurementPins, relayPins, shortTestPins)


testRig = MakeDefaultRig()
