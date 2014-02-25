import subprocess
import time
import optparse

def writeFuses(portName, lockFuses, eFuses, hFuses, lFuses, programmer="avrisp"):
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
  print command

  return subprocess.call(command)
  
def loadFlash(portName, flashFile, programmer="avrisp"):
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
    "-B", "1",
    "-U" "flash:w:%s:i" % flashFile,
  ]

  return subprocess.call(command)



if __name__ == '__main__':
  parser = optparse.OptionParser()

  parser.add_option("-p", "--port", dest="portname",
                    help="serial port (ex: /dev/ttyUSB0)", default="/dev/ttyACM0")
  (options, args) = parser.parse_args()

  port=options.portname

  lockFuses = 0x2F
  eFuses    = 0xCB
  hFuses    = 0xD8
  lFuses    = 0xFF
  
  returnCode = writeFuses(port, lockFuses, eFuses, hFuses, lFuses, programmer="usbtiny")

 
  if (returnCode != 0):
    print "FAIL. Error writing the fuses!"
    exit(1)
  print "PASS. Fuses written correctly"

  productionFile = "firmware/BlinkyTape-Production.hex"

  returnCode = loadFlash(port, productionFile, programmer="usbtiny")

  if (returnCode!= 0):
    print "FAIL. Error programming bootloader!"
    exit(1)
  print "PASS. Bootlaoder programmed successfully"
