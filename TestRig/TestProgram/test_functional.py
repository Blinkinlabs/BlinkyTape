import time
import serial

import BlinkyTapeUnitTest
import TestRig
import UserInterface
import BlinkyTape
import DetectPlatform

class TestFunctionalTests(BlinkyTapeUnitTest.BlinkyTapeTestCase):
  def __init__(self, methodName):
    super(TestFunctionalTests, self).__init__(methodName)

  @classmethod
  def setUpClass(self):
    # TODO: Why can't access self.testRig from __init__ here?
    self.testRig = TestRig.testRig
    self.testRig.resetState()

    self.i = UserInterface.interface
    self.dut = BlinkyTape.BlinkyTape()

  @classmethod
  def tearDownClass(self):
    self.dut = None
    self.testRig.resetState()

  def setUp(self):
    self.stopMe = True

  def tearDown(self):
    if self.stopMe:
      self.Stop()

  def test_010_dutDisconnectedCurrent(self):
    self.i.DisplayMessage("Checking disconnected current...")
    MIN_OFF_CURRENT = -1
    MAX_OFF_CURRENT = 1

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("DUT disconnectd current: %0.2f < %0.2f < %0.2f." % (MIN_OFF_CURRENT, current, MAX_OFF_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    self.assertTrue(current> MIN_OFF_CURRENT
                    and current < MAX_OFF_CURRENT)
    self.stopMe = False

  def test_020_usbEnumeration(self):
    self.i.DisplayMessage("Waiting for device to enumerate on USB...")

    MAX_ENUMERATION_TIME_S = 5
    # Scan for all connected devices; platform dependent
    originalPorts = set(DetectPlatform.ListSerialPorts())
 
    self.testRig.enableRelay('EN_USB_GND')
    self.testRig.enableRelay('EN_USB_VCC')
    self.testRig.enableRelay('EN_USB_DATA')

    # Wait for the device to enumerate
    startTime = time.time()
    while(time.time() < startTime + 5):
      finalPorts = set(DetectPlatform.ListSerialPorts())
      newPorts = finalPorts - originalPorts
      if len(newPorts) == 1:
        self.dut.port = list(newPorts)[0]
        break

    self.LogDataPoint("DUT Usb port:", self.dut.port)
    self.assertTrue(self.dut.port != '')
    self.stopMe = False

  def test_030_dutConnected(self):
    self.i.DisplayMessage("Connecting to DUT")

    connected = False
    try:
      self.dut.connect(self.dut.port)
    except serial.SerialException:
      pass
    else:
      connected = True

    self.assertTrue(connected)
    self.stopMe = False

  def test_040_dutConnectedCurrent(self):
    self.i.DisplayMessage("Checking connected current...")

    MIN_CONNECTED_CURRENT = 20
    MAX_CONNECTED_CURRENT = 40

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("DUT connected current: %0.2f < %0.2f < %0.2f." % (MIN_CONNECTED_CURRENT, current, MAX_CONNECTED_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    self.assertTrue(current > MIN_CONNECTED_CURRENT
                    and current < MAX_CONNECTED_CURRENT)
    self.stopMe = False

  def test_045_LedsConnectedCurrent(self):
    self.i.DisplayMessage("Checking LEDs connected current...")

    MIN_CONNECTED_CURRENT = 30
    MAX_CONNECTED_CURRENT = 50

    self.testRig.enableRelay('EN_LED_OUT')

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("LEDs connected current: %0.2f < %0.2f < %0.2f." % (MIN_CONNECTED_CURRENT, current, MAX_CONNECTED_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    self.assertTrue(current > MIN_CONNECTED_CURRENT
                    and current < MAX_CONNECTED_CURRENT)
    self.stopMe = False

  def test_050_redLedsOnCurrent(self):
    self.i.DisplayMessage("Checking red LEDs on...")

    MIN_RED_CURRENT = 130
    MAX_RED_CURRENT = 150
    # TODO: Why send this twice?
    for j in range (0, 2):
      for x in range(0, 60):
        self.dut.sendPixel(255,0,0)
      self.dut.show();

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("Red LEDs current: %0.2f < %0.2f < %0.2f." % (MIN_RED_CURRENT, current, MAX_RED_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    self.assertTrue(current > MIN_RED_CURRENT
                    and current < MAX_RED_CURRENT)
    self.stopMe = False

  def skip_test_060_greenLedsOnCurrent(self):
    self.i.DisplayMessage("Checking green LEDs on...")

    MIN_GREEN_CURRENT = 130
    MAX_GREEN_CURRENT = 150
    # TODO: Why send this twice?
    for j in range (0, 2):
      for x in range(0, 60):
        self.dut.sendPixel(0,255,0)
      self.dut.show();

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("Green LEDs current: %0.2f < %0.2f < %0.2f." % (MIN_GREEN_CURRENT, current, MAX_GREEN_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    self.assertTrue(current > MIN_GREEN_CURRENT
                    and current < MAX_GREEN_CURRENT)
    self.stopMe = False

  def skip_test_070_blueLedsOnCurrent(self):
    self.i.DisplayMessage("Checking blue LEDs on...")

    MIN_BLUE_CURRENT = 130
    MAX_BLUE_CURRENT = 150
    # TODO: Why send this twice?
    for j in range (0, 2):
      for x in range(0, 60):
        self.dut.sendPixel(0,0,255)
      self.dut.show();

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("Blue LEDs current: %0.2f < %0.2f < %0.2f." % (MIN_BLUE_CURRENT, current, MAX_BLUE_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    self.assertTrue(current > MIN_BLUE_CURRENT
                    and current < MAX_BLUE_CURRENT)
    self.stopMe = False

  def test_080_whiteLedsOnCurrent(self):
    self.i.DisplayMessage("Checking white LEDs on...")

    MIN_WHITE_CURRENT = 250
    MAX_WHITE_CURRENT = 350
    # TODO: Why send this twice?
    for j in range (0, 2):
      for x in range(0, 60):
        self.dut.sendPixel(255,255,255)
      self.dut.show();

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("White LEDs current: %0.2f < %0.2f < %0.2f." % (MIN_WHITE_CURRENT, current, MAX_WHITE_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    self.assertTrue(current > MIN_WHITE_CURRENT
                    and current < MAX_WHITE_CURRENT)
    self.stopMe = False

  def test_090_D7_connected(self):
    self.i.DisplayMessage("Checking D7 input works...")
    self.testRig.setOutputLow('DUT_D7')

    pinStates = 0
    for j in range (0, 2):
      for x in range(0, 60):
        self.dut.sendPixel(0,0,0)
      pinStates = self.dut.show();

    self.testRig.setInput('DUT_D7')
    
    self.assertTrue(ord(pinStates[0]) == 11)
    self.stopMe = False

  def test_091_D11_connected(self):
    self.i.DisplayMessage("Checking D11 input works...")
    self.testRig.setOutputLow('DUT_D11')

    pinStates = 0
    for j in range (0, 2):
      for x in range(0, 60):
        self.dut.sendPixel(0,0,0)
      pinStates = self.dut.show();

    self.testRig.setInput('DUT_D11')
    
    self.assertTrue(ord(pinStates[0]) == 13)
    self.stopMe = False

  def test_092_A10_connected(self):
    self.i.DisplayMessage("Checking A10 input works...")
    self.testRig.setOutputLow('DUT_A10')

    pinStates = 0
    for j in range (0, 2):
      for x in range(0, 60):
        self.dut.sendPixel(0,0,0)
      pinStates = self.dut.show();

    self.testRig.setInput('DUT_A10')
   
    self.assertTrue(ord(pinStates[0]) == 14)
    self.stopMe = False

  def test_100_button_connected(self):
    self.i.DisplayMessage("Checking button input works...")

    MAX_TIME_SECONDS = 60;

    startTime = time.time()
    found = False
    mode = True

    while((not found) and (time.time() < startTime + MAX_TIME_SECONDS)):
      pinStates = 0
      for j in range (0, 2):
        for x in range(0, 60):
	  if mode:
            self.dut.sendPixel(0,0,100)
          else:
            self.dut.sendPixel(0,0,0)
        pinStates = self.dut.show();

      if ord(pinStates[0]) == 0x07:
        found = True

      mode = not mode
      time.sleep(.5)
   
    self.assertTrue(found)
    self.stopMe = False

