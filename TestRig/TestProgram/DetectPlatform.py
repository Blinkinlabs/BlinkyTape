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
  # Scan for all connected devices; platform dependent
  platform = detectPlatform()

  if platform == 'Darwin':
    ports =      glob.glob("/dev/cu.usb*")
  else:
    # TODO: linux?
    ports =      glob.glob("/dev/ttyACM*")
    ports.extend(glob.glob("/dev/ttyUSB*"))

  return ports
