import time

import BlinkyTapeUnitTest
import TestRig
import UserInterface

class TestPowerOnTests(BlinkyTapeUnitTest.BlinkyTapeTestCase):
  def __init__(self, methodName):
    super(TestPowerOnTests, self).__init__(methodName)
    self.testRig = TestRig.testRig
    self.i = UserInterface.interface

  def setUp(self):
    self.stopMe = True

    self.testRig.resetState()

  def tearDown(self):
    self.testRig.resetState()

    if self.stopMe:
      self.Stop()


  def test_010_off_current(self):
    MIN_OFF_CURRENT = -1
    MAX_OFF_CURRENT = 2
    self.testRig.enableRelay('EN_USB_GND')
    time.sleep(.5)

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("Off current: %0.2f < %0.2f < %0.2f." % (MIN_OFF_CURRENT, current, MAX_OFF_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    result = current > MIN_OFF_CURRENT and current < MAX_OFF_CURRENT
    self.assertTrue(result)
    self.stopMe = False

  def test_020_limited_current(self):
    MIN_LIMITED_CURRENT = 15
    MAX_LIMITED_CURRENT = 35

    self.testRig.enableRelay('EN_USB_GND')
    self.testRig.enableRelay('EN_USB_VCC_LIMIT')
    time.sleep(.5)

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("Limited current: %0.2f < %0.2f < %0.2f." % (MIN_LIMITED_CURRENT, current, MAX_LIMITED_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    result = current > MIN_LIMITED_CURRENT and current < MAX_LIMITED_CURRENT
    self.assertTrue(result)
    self.stopMe = False

  def test_030_full_current(self):
    MIN_OPERATING_CURRENT = 20
    MAX_OPERATING_CURRENT = 40
 
    self.testRig.enableRelay('EN_USB_GND')
    self.testRig.enableRelay('EN_USB_VCC')
    time.sleep(.5)

    current = self.testRig.measure('DUT_CURRENT')

    self.i.DisplayMessage("Full current: %0.2f < %0.2f < %0.2f." % (MIN_OPERATING_CURRENT, current, MAX_OPERATING_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    result = current > MIN_OPERATING_CURRENT and current < MAX_OPERATING_CURRENT
    self.assertTrue(result)
    self.stopMe = False
