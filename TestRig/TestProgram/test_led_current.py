import time
import glob
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

  def test_010_usbEnumeration(self):
    self.i.DisplayMessage("Waiting for device to enumerate on USB...")

    MAX_ENUMERATION_TIME_S = 5
    platform = DetectPlatform.detectPlatform()
    if platform == 'Darwin':
      SERIAL_DEVICE_PATH = "/dev/cu.usbmodem*"
    else:
      # TODO: linux?
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
        self.dut.port = list(newPorts)[0]
        break

    self.LogDataPoint("DUT Usb port:", self.dut.port)
    self.assertTrue(self.dut.port != '')
    self.stopMe = False

  def test_020_dutConnected(self):
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

  def test_030_stepGrayscaleBrightness(self):
    self.i.DisplayMessage("Measuring current for strip brightness 0-255")
    self.testRig.enableRelay('EN_LED_OUT')

    for bright in range(0,255):
      # TODO: Why send this twice?
      for j in range (0, 2):
        for x in range(0, 60):
          self.dut.sendPixel(bright,0,0)
        self.dut.show();
      current = self.testRig.measure('DUT_CURRENT')
      print bright, current

    self.stopMe = False

