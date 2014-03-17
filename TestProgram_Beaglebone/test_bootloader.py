import time
import subprocess

import BlinkyTapeUnitTest
import TestRig
import UserInterface
import IcspUtils
import Logger

class TestProgramBootloader(BlinkyTapeUnitTest.BlinkyTapeTestCase):
  def __init__(self, methodName):
    super(TestProgramBootloader, self).__init__(methodName)
    self.testRig = TestRig.testRig
    self.port = self.testRig.port
    self.i = UserInterface.interface

  def setUp(self):
    self.stopMe = True

  def tearDown(self):
    self.testRig.connect(self.port)
    self.testRig.resetState()

    if self.stopMe:
      self.Stop()

  def test_010_program_fuses(self):
    self.i.DisplayMessage("Programming fuses...")

    self.testRig.resetState()
    self.testRig.enableRelay('EN_USB_VCC')
    self.testRig.enableRelay('EN_USB_GND')
    self.testRig.setProgrammerSpeed(0)
    self.testRig.disconnect()

    lockFuses = 0x2F
    eFuses    = 0xCB
    hFuses    = 0xD8
    lFuses    = 0xFF
#    lFuses    = 0x5E #default
    
    result = IcspUtils.writeFuses(self.port, lockFuses, eFuses, hFuses, lFuses)
    
    self.LogDataPoint('fuses stdout', result[1])
    self.LogDataPoint('fuses stderr', result[2])

    self.assertEqual(result[0], 0)
    self.stopMe = False

  def test_020_program_production(self):
    self.i.DisplayMessage("Programming firmware...")

    self.testRig.connect(self.port)
    self.testRig.resetState()
    self.testRig.enableRelay('EN_USB_VCC')
    self.testRig.enableRelay('EN_USB_GND')
    self.testRig.setProgrammerSpeed(1)
    self.testRig.disconnect()

    productionFile = "firmware/BlinkyTape-Production.hex"

    result = IcspUtils.loadFlash(self.port, productionFile)

    self.LogDataPoint('firmware stdout', result[1])
    self.LogDataPoint('firmware stderr', result[2])

    self.assertEqual(result[0], 0)
    self.stopMe = False
