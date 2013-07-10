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
    self.testRig.resetState()

  def tearDown(self):
    self.testRig.resetState()

  def getDutCurrent(self):
    # TODO: Move this to the test rig?
    CURRENT_A = 994
    CURRENT_B = -2.3
    return CURRENT_B*(self.testRig.measure('DUT_CURRENT') - CURRENT_A)

  def test_010_off_current(self):
    MIN_OFF_CURRENT = -100
    MAX_OFF_CURRENT = 100
    current = self.getDutCurrent()

    self.i.DisplayMessage("Off current: %0.2f < %0.2f < %0.2f." % (MIN_OFF_CURRENT, current, MAX_OFF_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    result = current > MIN_OFF_CURRENT and current < MAX_OFF_CURRENT
    self.assertTrue(result)
    

  def test_020_limited_current(self):
    MIN_LIMITED_CURRENT= 50
    MAX_LIMITED_CURRENT = 70

    self.testRig.enableRelay('EN_USB_GND')
    self.testRig.enableRelay('EN_USB_VCC_LIMIT')
    time.sleep(.5)

    current = self.getDutCurrent()

    self.i.DisplayMessage("Limited current: %0.2f < %0.2f < %0.2f." % (MIN_LIMITED_CURRENT, current, MAX_LIMITED_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    result = current > MIN_LIMITED_CURRENT and current < MAX_LIMITED_CURRENT
    self.assertTrue(result)

  def test_030_full_current(self):
    MIN_OPERATING_CURRENT = 25
    MAX_OPERATING_CURRENT = 35
 
    self.testRig.enableRelay('EN_USB_GND')
    self.testRig.enableRelay('EN_USB_VCC')
    time.sleep(.5)

    current = self.getDutCurrent()

    self.i.DisplayMessage("Full current: %0.2f < %0.2f < %0.2f." % (MIN_OPERATING_CURRENT, current, MAX_OPERATING_CURRENT))
    self.StoreTestResultData("%0.2f" % current)

    result = current > MIN_OPERATING_CURRENT and current < MAX_OPERATING_CURRENT
    self.assertTrue(result)
