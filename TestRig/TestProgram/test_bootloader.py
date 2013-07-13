import time
import subprocess

import BlinkyTapeUnitTest
import TestRig
import UserInterface
import IcspUtils
import Config


class TestProgramBootloader(BlinkyTapeUnitTest.BlinkyTapeTestCase):
  def __init__(self, methodName):
    super(TestProgramBootloader, self).__init__(methodName)
    self.testRig = TestRig.testRig
    self.port = self.testRig.port
    self.i = UserInterface.interface

  def setUp(self):
    self.stopMe = True

    self.testRig.resetState()
    self.testRig.disableRelay('EN_USB_VCC')
    self.testRig.disableRelay('EN_USB_GND')
    self.testRig.disconnect()

  def tearDown(self):
    self.testRig.connect(self.port)
    self.testRig.resetState()

    if self.stopMe:
      self.Stop()

  def test_010_program_fuses(self):
    config = Config.Config()
    lockFuses = config.get('ICSP', 'lockFuses', 0x2f)
    eFuses = config.get('ICSP', 'eFuses', 0xcb)
    hFuses = config.get('ICSP', 'hFuses', 0xd8)
    lFuses = config.get('ICSP', 'lFuses', 0xff)
    
    returnCode = IcspUtils.writeFuses(self.port, lockFuses, eFuses, hFuses, lFuses)
    
    self.assertEqual(returnCode, 0)
    self.stopMe = False

  def test_020_program_fuses(self):
    config = Config.Config()
    bootloaderFile = config.get('ICSP', 'bootloaderFile', "Caterina-BlinkyTape.hex")
    
    returnCode = IcspUtils.loadFlash(self.port, bootloaderFile)

    self.assertEqual(returnCode, 0)
    self.stopMe = False
