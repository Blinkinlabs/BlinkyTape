import subprocess
import time
import optparse
import sys
import cStringIO

def writeFuses(portName, lockFuses, eFuses, hFuses, lFuses, programmer="STK500v1"):
  """
  Attempt to write the fuses of the attached Atmega device.

  """
  command = [
    "avrdude",
    "-c", programmer,
    "-P", portName,
    "-p", "m32u4",
    "-B", "200",
    "-e",
    "-U", "lock:w:%#02X:m"  % lockFuses,
    "-U", "efuse:w:%#02X:m" % eFuses,
    "-U", "hfuse:w:%#02X:m" % hFuses,
    "-U", "lfuse:w:%#02X:m" % lFuses,
  ]

  s = open('result.log','w')
  e = open('errorresult.log','w')
  result = subprocess.call(command, stdout=s, stderr=e)
  s.close()
  e.close()

  s = open('result.log','r')
  e = open('errorresult.log','r')
  stdout = s.readlines()
  stderr = e.readlines()
  s.close()
  e.close()

  return result, stdout, stderr
  
def loadFlash(portName, bootloaderFile, appFile, programmer="STK500v1"):
  """
  Attempt to write a .hex file to the flash of the attached Atmega device.
  @param portName String of the port name to write to
  @param flashFile Array of file(s) to write to the device
  """
  command = [
    "avrdude",
    "-c", programmer,
    "-P", portName,
    "-p", "m32u4",
    "-B", "8MHz",
    "-U" "flash:w:%s:i" % bootloaderFile,
    "-U" "flash:w:%s:i" % appFile,
  ]

  s = open('result.log','w')
  e = open('errorresult.log','w')
  result = subprocess.call(command, stdout=s, stderr=e)
  s.close()
  e.close()

  s = open('result.log','r')
  e = open('errorresult.log','r')
  stdout = s.readlines()
  stderr = e.readlines()
  s.close()
  e.close()

  return result, stdout, stderr


if __name__ == '__main__':
  parser = optparse.OptionParser()

  parser.add_option("-p", "--port", dest="portname",
                    help="serial port (ex: /dev/ttyUSB0)", default="/dev/ttyACM0")
  (options, args) = parser.parse_args()

  port=options.portname

  #lockFuses = 0x2F
  lockFuses = 0xEF
  eFuses    = 0xCB
  hFuses    = 0xD8
  lFuses    = 0xFF
  
  while True:
    raw_input("press Enter to program...")

    returnCode = writeFuses(port, lockFuses, eFuses, hFuses, lFuses)
   
    if (returnCode[0] != 0):
      print "FAIL. Error writing the fuses!"
      #exit(1)
      continue
    print "PASS. Fuses written correctly"

    bootloaderFile = "BlinkyTape-Bootloader-v200.hex"
    appFile = "factory.hex"

    returnCode = loadFlash(port, bootloaderFile, appFile)

    if (returnCode[0]!= 0):
      print "FAIL. Error programming bootloader!"
      #exit(1)
      continue
    print "PASS. Bootlaoder programmed successfully"
