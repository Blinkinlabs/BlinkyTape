import subprocess
import time


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

print detectPlatform()
