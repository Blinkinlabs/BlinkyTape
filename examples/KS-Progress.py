# Based on LED-AQI by Zach Hoeken Smith (http://hoektronics.com)

import time
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
  while True:
    try:
      progress = get_ks_amount();

      if not progress:
        print("Site could not be scraped. Check your proxy settings and try again. Try: export http_proxy=PROXY_IP:PROXY_PORT before running this script.")

      leds = int(progress * 60)
      print "Progress: %s, %s" % (progress, leds)
    
      for i in range(60):
        if(i < leds):
          bb.sendPixel(255,255,255)
        else:
          bb.sendPixel(0,0,0)
      bb.show()

      time.sleep(time_delay)

    except KeyboardInterrupt as ex:
      print "Exiting."
      sys.exit(0)
