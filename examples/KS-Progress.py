# Based on LED-AQI by Zach Hoeken Smith (http://hoektronics.com)

import time
import math
import urllib
from bs4 import BeautifulSoup #pip install beautifulsoup4 html5lib
import tempfile
import serial.tools.list_ports
import sys

from Blinkyboard import Blinkyboard

url = "http://www.kickstarter.com/projects/740956622/blinkytape-the-led-strip-reinvented"
time_delay = 10
yheight = 25

def connect():

  port = None

  busses = serial.tools.list_ports.comports();
  for bus in busses:
    for potential_port in bus:
      if "usbmodem" in potential_port:
        port = potential_port

  if not port:
    sys.exit("Could not locate a Blinkyboard.")

  print "Blinkyboard found at: %s" % port

  bb = Blinkyboard(port, 60, 'WS2811', gamma=[1,1,1])
  bb.allOff()
  bb.show()
  return bb

def get_ks_amount():

  try:
    data = urllib.urlopen(url)
    soup = BeautifulSoup(data, "html5lib")
    pledge_dom = soup.find_all(id="pledged")

    if len(pledge_dom):
      return float(pledge_dom[0]['data-percent-raised'])

    if not len(pledge_dom):
      return 0
  
  except Exception as ex:
    print ex

if __name__ == "__main__":

  bb = connect()
  progress = get_ks_amount()
  leds = int(progress * 60)
  print "Progress: %s, %s" % (progress, leds)
  last_time = time.time()
  while True:
    try:
      now = time.time()
      if(now > last_time + time_delay):
        print "Updating..."
        progress = get_ks_amount()
        if progress > 1.0:
          progress = 1.0
        leds = int(progress * 60)
        print "Progress: %s, %s" % (progress, leds)
        last_time = now

    
      for i in range(60):
        if(i < leds):
          time_part = time.time() * 10.0
          dimval = 0.05
          redval = int(dimval * (math.sin(time_part - i) * 128.0 + 127.0))
          greenval = int(dimval * (math.sin(time_part - i + math.pi) * 128.0 + 127.0))
          blueval = int(dimval * (math.sin(time_part - i + math.pi + math.pi) * 128.0 + 127.0))
          bb.sendPixel(redval, greenval, blueval)
        else:
          bb.sendPixel(0,0,0)
      bb.show()


    except KeyboardInterrupt as ex:
      print "Exiting."
      sys.exit(0)
