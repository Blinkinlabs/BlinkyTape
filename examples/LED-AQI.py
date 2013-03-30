# Original example by Zach Hoeken Smith (http://hoektronics.com)
# Modified for the new Blinkyboard library by Max Henstell 3/2013
# To use this behind a proxy, set the http_proxy environment variable, like so:
# export http_proxy=http://127.0.0.1:3213
# before running this script

import time
import urllib
from bs4 import BeautifulSoup #pip install beautifulsoup4 html5lib
import Image #pip install PIL
import base64
import tempfile
import serial.tools.list_ports
import sys

from Blinkyboard import Blinkyboard

#url = "http://www.aqicn.info/city/hongkong/"
#url = "http://www.aqicn.info/city/shenzhen/"
url = "http://www.aqicn.info/city/shenzhen/huaqiaocheng/"
#url = "http://www.aqicn.info/city/beijing/"
#url = "http://www.aqicn.info/city/shanghai/"
#url = "http://www.aqicn.info/"

# X positions to sample from the AQICN history image
positions = [243, 238, 233, 228, 223, 218, 213, 208, 203, 198, 193, 188, 183, 178, 173, 168, 163, 158, 153, 148, 143, 138, 133, 128, 123, 118, 113]

time_delay = 0.75
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
  return bb


def get_AQI_image():

  print "[%d] Scraping %s" % (time.time(), url)
  img = None

  try:
    data = urllib.urlopen(url)
    soup = BeautifulSoup(data, "html5lib")
    imgs = soup.find_all(id="img_pm25")

    if len(imgs):
      imgurl = imgs[0]['src']

      print "Parsing image"
      imgdata = base64.b64decode(imgurl[22:])
      tmp = open("data.png", "w")
      tmp.write(imgdata)
      tmp.close()
      img = Image.open("data.png")
      img = img.convert('RGB')

      return img
    
    if not len(imgs) or img is None:
      raise Exception("AQI image not found")
  
  except Exception as ex:
    print ex

if __name__ == "__main__":

  bb = connect()
  img = get_AQI_image()

  if not img:
    sys.exit("AQI image could not be scraped. Check your proxy settings and try again. Try: export http_proxy=PROXY_IP:PROXY_PORT before running this script.")

  while True:
    
    try:
      for position in positions:
        r, g, b = img.getpixel((position, yheight))
        #print "\tPosition: (%i,%i) - (%i, %i, %i)" % (position, yheight, r, g, b)
        bb.sendPixel(r, g, b);
      bb.show()

      time.sleep(time_delay)

      bb.sendPixel(0,0,0);
      bb.show()
      
      time.sleep(time_delay)
        
    except KeyboardInterrupt as ex:
      print "Exiting."
      sys.exit(0)