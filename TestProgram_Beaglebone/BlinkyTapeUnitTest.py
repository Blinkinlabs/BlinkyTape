import unittest
import time

import UserInterface
import Logger

class BlinkyTapeTestCase(unittest.TestCase):
  def __init__(self, methodName):
    super(BlinkyTapeTestCase, self).__init__(methodName)
    self.l = Logger.logger
    self.testResultData = None
    self.stopTests = False

  def StoreTestResultData(self, trd):
    self.testResultData = trd

  def Stop(self):
    self.stopTests = True

  def LogDataPoint(self, message, data):
    """Record a datapoint from testing.  This will log to all available logging outputs w/ the included data (db, sdcard, usb)."""
    tid = self.l.GetTestId(self.id())
    self.l.Log(self.id(), message, data, "data", testId=tid)


class BlinkyTapeTestRunner():
  """
  A test runner class that logs to the database and interacts with the LCD screen to display test results.
  """
  def __init__(self):
    self.i = UserInterface.interface
    self.l = Logger.logger

  def run(self, test):
    "Run the given test case or test suite."
    result = BlinkyTapeTestResult()
    startTime = time.time()
    test(result)
    stopTime = time.time()

    timeTaken = stopTime - startTime
    run = result.testsRun
    output = "Ran %d test%s in %.3fs\n" % (run, run != 1 and "s" or "", timeTaken)
    if not result.wasSuccessful():
      failed, errored = map(len, (result.failures, result.errors))
      if failed:
        output += "\nFAILED: %d\n" % failed
      if errored:
        output += "\nERRORS: %d\n" % errored
      textColor = (255, 255, 255)
      outColor = (255, 0, 0)
    else:
      output += "\nALL OK!\n"
      textColor = (0, 0, 0)
      outColor = (0, 255, 0)
    self.i.DisplayMessage(output, color = textColor, bgcolor = outColor, boxed=True)
    time.sleep(2)
      
    return result

class BlinkyTapeTestResult(unittest.TestResult):
  """A test result class that can log formatted text results to a stream.

  Used by BlinkyTapeTestRunner.
  """
  def __init__(self):
    unittest.TestResult.__init__(self)
    self.i = UserInterface.interface
    self.l = Logger.logger

  def getDescription(self, test):
    return test.shortDescription() or str(test)

  def startTest(self, test):
    unittest.TestResult.startTest(self, test)
    self.l.TestStart(test)

  def stopTest(self, test):
    self.shouldStop = test.stopTests

  def addSuccess(self, test):
    unittest.TestResult.addSuccess(self, test)
    self.i.DisplayPass()
    self.l.TestPass(test)

  def addError(self, test, err):
    unittest.TestResult.addError(self, test, err)
    self.i.DisplayError()
    self.l.TestError(test, err)

  def addFailure(self, test, err):
    unittest.TestResult.addFailure(self, test, err)
    self.i.DisplayFail()
    self.l.TestFail(test)

