import BlinkyTapeUnitTest
import UserInterface
import TestRig


class TestShortTests(BlinkyTapeUnitTest.BlinkyTapeTestCase):
  def __init__(self, methodName):
    super(TestShortTests, self).__init__(methodName)
    self.testRig = TestRig.testRig
    self.i = UserInterface.interface

  def setUp(self):
    self.testRig.resetState()

  def tearDown(self):
    self.testRig.resetState()

  def test_010_short_tests(self):
    """ Run the n*n test case """

    for pin in self.testRig.shortTestPins:
      self.i.DisplayMessage("testing pin %s..." % pin.name)

      faults = self.testRig.shortTest(pin.name)
      for fault in faults:
        print fault
      self.assertEquals(len(faults), 0)

