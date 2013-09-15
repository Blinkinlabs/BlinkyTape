# Note: the current sensor on this board is a little whack, and also it uses the wrong sense resistor,
# so these constants were adjusted accordingly.

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

    self.testRig.enableRelay("LED_B")

  @classmethod
  def tearDownClass(self):
    self.dut = None
    self.testRig.resetState()

  def setUp(self):
    self.stopMe = True

  def tearDown(self):
    if self.stopMe:
      self.Stop()

  def test_010_off_current(self):
    MIN_OFF_CURRENT = -1
    MAX_OFF_CURRENT = 2

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("Off current: %0.2f < %0.2f < %0.2f." % (MIN_OFF_CURRENT, current, MAX_OFF_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    result = current > MIN_OFF_CURRENT and current < MAX_OFF_CURRENT
    self.assertTrue(result)
    self.stopMe = False

  def test_020_limited_current(self):
    MIN_LIMITED_CURRENT = 200
    MAX_LIMITED_CURRENT = 500

    self.testRig.enableRelay('EN_USB_VCC_LIMIT')
    time.sleep(.5)

    current = self.testRig.measure('DUT_CURRENT')

    self.testRig.disableRelay('EN_USB_VCC_LIMIT')

    self.i.DisplayMessage("Limited current: %0.2f < %0.2f < %0.2f." % (MIN_LIMITED_CURRENT, current, MAX_LIMITED_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    result = current > MIN_LIMITED_CURRENT and current < MAX_LIMITED_CURRENT
    self.assertTrue(result)
    self.stopMe = False


  def test_040_usbEnumeration(self):
    self.i.DisplayMessage("Waiting for device to enumerate on USB...")

    MAX_ENUMERATION_TIME_S = 5
    # Scan for all connected devices; platform dependent
    originalPorts = set(DetectPlatform.ListSerialPorts())
 
    self.testRig.enableRelay('EN_USB_VCC')

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

  def test_050_dutConnected(self):
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

  def test_060_dutConnectedCurrent(self):
    self.i.DisplayMessage("Checking connected current...")

    MIN_CONNECTED_CURRENT = 200
    MAX_CONNECTED_CURRENT = 4000

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("DUT connected current: %0.2f < %0.2f < %0.2f." % (MIN_CONNECTED_CURRENT, current, MAX_CONNECTED_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    self.assertTrue(current > MIN_CONNECTED_CURRENT
                    and current < MAX_CONNECTED_CURRENT)
    self.stopMe = False


  def test_050_redLedsOnCurrent(self):
    self.i.DisplayMessage("Checking red LEDs on...")

    MIN_RED_CURRENT = 500
    MAX_RED_CURRENT = 10000
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

  def test_080_whiteLedsOnCurrent(self):
    self.i.DisplayMessage("Checking white LEDs on...")

    MIN_WHITE_CURRENT = 100
    MAX_WHITE_CURRENT = 30000
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

