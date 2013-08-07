import subprocess
import time
import glob


def detectPlatform():
  data = []
  proc = subprocess.Popen(["uname"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

  while True:
    read = proc.stdout.readline() #block / wait
    if not read:
        break
    data.append(read)

  if data[0] == 'Darwin\n':
    return "Darwin"

  return "Unknown"

def ListSerialPorts():
  platform = detectPlatform()

  if platform == 'Darwin':
    SERIAL_DEVICE_PATH = "/dev/cu.usbmodem*"
  else:
    # TODO: linux?
    SERIAL_DEVICE_PATH = "/dev/ttyACM*"

  # Scan for all connected devices; platform dependent
  return glob.glob(SERIAL_DEVICE_PATH)
  

