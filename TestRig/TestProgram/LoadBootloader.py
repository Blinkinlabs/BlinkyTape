import subprocess
import time
from optparse import OptionParser

config = {
  "bootlader_filename" : "Caterina-BlinkyTape.hex",
}

def writeFuses(portName, lockFuses, eFuses, hFuses, lFuses):
  """
  Attempt to write the fuses of the attached Atmega device.

  """
  command = [
    "avrdude",
    "-c", "avrisp",
    "-p", "m32u4",
    "-P", portName,
    " -B", "200",
    "-Ulock:w:"  + "0x2f" + ":m",
    "-Uefuse:w:" + "0xcb" + ":m",
    "-Uhfuse:w:" + "0xd8" + ":m",
    "-Ulfuse:w:" + "0xff" + ":m",
  ]

  returnCode = subprocess.call(command)
  if returnCode != 0:
    raise Exception("Error writing fuses to board: Expected return code 0, got=" + str(returnCode))
  
def loadBootloader(portName, bootloaderFile):
  """
  Attempt to write the fuses of the attached Atmega device.

  """
  command = [
    "avrdude",
    "-c", "avrisp",
    "-p", "m32u4",
    "-P", portName,
    "-B", "1",
    "-Uflash:w:" + bootloaderFile + ":i",
  ]

  returnCode = subprocess.call(command)
  if returnCode != 0:
    raise Exception("Error writing bootloader to board: Expected return code 0, got=" + str(returnCode))



def programChip(options):
  """
  Program the fuses and bootloader into the device
  """

  # Write the fuses
  display_message("Writing fuses...")
  fuseResult = (writeFuses(options.portname) == 0)
 
  if (fuseResult!= True):
    display_message("FAIL. Error writing the fuses!")
    return
  display_message("PASS. Fuses written correctly")


  # Program the bootloader
  display_message("Programming bootloader")
  bootloaderResult = (loadBootloader(options.portname,
                config["bootlader_filename"]) == 0)
  
  if (bootloaderResult != True):
    display_message("FAIL. Error programming bootloader!")
    return
  display_message("PASS. Bootlaoder programmed successfully")


if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option("-p", "--port", dest="portname",
                    help="serial port (ex: /dev/ttyUSB0)", default="/dev/ttyACM0")
  (options, args) = parser.parse_args()

  programChip(options)
