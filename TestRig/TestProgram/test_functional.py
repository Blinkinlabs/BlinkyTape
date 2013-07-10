import time
import glob

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
    print "setUpClass"
    # TODO: Why can't access self.testRig from __init__ here?
    self.testRig = TestRig.testRig
    self.testRig.resetState()

    self.i = UserInterface.interface
    self.dutPort = None
    self.dut = None

  @classmethod
  def tearDownClass(self):
    print "tearDownClass"
    self.dut = None
    self.testRig.resetState()

  def getDutCurrent(self):
    # TODO: Move this to the test rig?
    CURRENT_A = 994
    CURRENT_B = -2.3
    return CURRENT_B*(self.testRig.measure('DUT_CURRENT') - CURRENT_A)

  def test_010_dutDisconnectedCurrent(self):
    MIN_OFF_CURRENT = -60
    MAX_OFF_CURRENT = 35

    current = self.getDutCurrent()

    self.LogDataPoint("DUT disconnected current", current)
    self.assertTrue(current> MIN_OFF_CURRENT
                    and current < MAX_OFF_CURRENT)

  def test_020_usbEnumeration(self):
    MAX_ENUMERATION_TIME_S = 5
    platform = DetectPlatform.DetectPlatform()
    if platform == 'Darwin':
      SERIAL_DEVICE_PATH = "/dev/cu.usbmodem*"
    else:
      SERIAL_DEVICE_PATH = "/dev/cu.usbmodem*"

    # Scan for all connected devices; platform dependent
    originalPorts = set(glob.glob(SERIAL_DEVICE_PATH))
 
    self.testRig.enableRelay('EN_USB_GND')
    self.testRig.enableRelay('EN_USB_VCC')
    self.testRig.enableRelay('EN_USB_DATA')

    # Wait for the device to enumerate
    startTime = time.time()
    while(time.time() < startTime + 5):
      finalPorts =set(glob.glob("/dev/cu.usbmodem*"))
      newPorts = finalPorts - originalPorts
      if len(newPorts) == 1:
        self.dutPort = list(newPorts)[0]
        break

    self.LogDataPoint("DUT Usb port:", self.dutPort)
    self.assertTrue(self.dutPort != None)

  def test_030_dutConnected(self):

    self.dut = BlinkyTape.BlinkyTape(self.dutPort, "WS2811")
    print self.dut

  def test_040_dutConnectedCurrent(self):
    print self.dut
    MIN_CONNECTED_CURRENT = 25
    MAX_CONNECTED_CURRENT = 35

    current = self.getDutCurrent()

    self.LogDataPoint("DUT connected current", current)
    self.assertTrue(current > MIN_CONNECTED_CURRENT
                    and current < MAX_CONNECTED_CURRENT)

  def test_050_redLedsOnCurrent(self):
    MIN_RED_CURRENT = 100
    MAX_RED_CURRENT = 2000
    # TODO: Why send this twice?
    for j in range (0, 2):
      for x in range(0, 60):
        self.dut.sendPixel(255,0,0)
      self.dut.show();

    current = self.getDutCurrent()

    self.LogDataPoint("Red leds current", current)
    self.assertTrue(current > MIN_RED_CURRENT
                    and current < MAX_RED_CURRENT)

  def test_060_greenLedsOnCurrent(self):
    MIN_GREEN_CURRENT = 100
    MAX_GREEN_CURRENT = 2000
    # TODO: Why send this twice?
    for j in range (0, 2):
      for x in range(0, 60):
        self.dut.sendPixel(0,255,0)
      self.dut.show();

    current = self.getDutCurrent()

    self.LogDataPoint("Green leds current", current)
    self.assertTrue(current > MIN_GREEN_CURRENT
                    and current < MAX_GREEN_CURRENT)

  def test_070_blueLedsOnCurrent(self):
    MIN_BLUE_CURRENT = 100
    MAX_BLUE_CURRENT = 2000
    # TODO: Why send this twice?
    for j in range (0, 2):
      for x in range(0, 60):
        self.dut.sendPixel(0,0,255)
      self.dut.show();

    current = self.getDutCurrent()

    self.LogDataPoint("Blue leds current", current)
    self.assertTrue(current > MIN_BLUE_CURRENT
                    and current < MAX_BLUE_CURRENT)

  def test_080_whiteLedsOnCurrent(self):
    MIN_WHITE_CURRENT = 100
    MAX_WHITE_CURRENT = 2000
    # TODO: Why send this twice?
    for j in range (0, 2):
      for x in range(0, 60):
        self.dut.sendPixel(255,255,255)
      self.dut.show();

    current = self.getDutCurrent()

    self.LogDataPoint("White leds current", current)
    self.assertTrue(current > MIN_WHITE_CURRENT
                    and current < MAX_WHITE_CURRENT)
