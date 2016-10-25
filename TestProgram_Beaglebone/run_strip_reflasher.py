import time
import serial
from serial.tools import list_ports
import BlinkyTape
import IcspUtils


# reset a strip to the booloader
def resetToBootloader(portName):
  print "Resetting to bootloader on %s"%portName
  bt = BlinkyTape.BlinkyTape(portName)
  bt.displayColor(20,0,20)
  bt.resetToBootloader()

# Write the latest firmware to the strip
def flashFirmware(portName):
  print "Writing firmware on %s"%portName
  result = IcspUtils.loadFlash(portName, "firmware/BlinkyTape-Application.hex", "avr109")
  if(result[0] != 0):
    print result
  pass

def showTestPattern(portName):
  print "Showing test pattern on %s"%portName
  try:
    bt = BlinkyTape.BlinkyTape(portName)
    while True:
      bt.displayColor(255,0,0)
      time.sleep(1)
      bt.displayColor(0,255,0)
      time.sleep(1)
      bt.displayColor(0,0,255)
      time.sleep(1)
  except:
    pass

def runSearch():
  ports = list_ports.comports()
  time.sleep(.5)

  for port in ports:
    if port[2] == "USB VID:PID=2341:8036":
      resetToBootloader(port[0])

    elif port[2] == "USB VID:PID=1d50:606c":
      flashFirmware(port[0])

    elif port[2] == "USB VID:PID=1d50:605e":
      showTestPattern(port[0])

    else:
      print "Unrecognized port %s"%port[2]

    time.sleep(1)

while True:
  runSearch()
