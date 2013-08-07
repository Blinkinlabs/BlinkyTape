import subprocess
import time
import optparse

def writeFuses(portName, lockFuses, eFuses, hFuses, lFuses):
  """
  Attempt to write the fuses of the attached Atmega device.

  """
  command = [
    "./avrdude",
    "-c", "avrisp",
    "-p", "m32u4",
    "-P", portName,
    "-B", "200",
    "-u",
    "-U", "lock:w:%#02X:m"  % lockFuses,
    "-U", "efuse:w:%#02X:m" % eFuses,
    "-U", "hfuse:w:%#02X:m" % hFuses,
    "-U", "lfuse:w:%#02X:m" % lFuses,
  ]
  print command

  return subprocess.call(command)
  
def loadFlash(portName, flashFile):
  """
  Attempt to write a .hex file to the flash of the attached Atmega device.
  @param portName String of the port name to write to
  @param flashFile Array of file(s) to write to the device
  """
  command = [
    "./avrdude",
    "-c", "avrisp",
    "-p", "m32u4",
    "-P", portName,
    "-B", "1",
    "-U" "flash:w:%s:i" % flashFile,
  ]

  return subprocess.call(command)



if __name__ == '__main__':
  parser = optparse.OptionParser()
  parser.add_option("-p", "--port", dest="portname",
                    help="serial port (ex: /dev/ttyUSB0)", default="/dev/ttyACM0")
  (options, args) = parser.parse_args()

  config = {
    "bootlader_filename" : "Caterina-BlinkyTape.hex",
    "lockFuses"          : "0x2f",
    "eFuses"             : "0xcb",
    "hFuses"             : "0xd8",
    "lFuses"             : "0xff",
  }


  # Write the fuses
  print "Writing fuses..."
  fuseResult = writeFuses(options.portname,
                          config['lockFuses'],
                          config['eFuses'],
                          config['hFuses'],
                          config['lFuses'])
 
  if (fuseResult != 0):
    print "FAIL. Error writing the fuses!"
    exit(1)
  print "PASS. Fuses written correctly"


  # Program the bootloader
  print "Programming bootloader"
  bootloaderResult = loadFlash(options.portname,
                               config["bootlader_filename"])
  
  if (bootloaderResult != 0):
    print "FAIL. Error programming bootloader!"
    exit(1)
  print "PASS. Bootlaoder programmed successfully"
