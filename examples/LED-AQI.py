import time
import urllib
from bs4 import BeautifulSoup #pip install beautifulsoup4 html5lib
import Image #pip install PIL
import base64
import tempfile
import serial.tools.list_ports

from Blinkyboard import Blinkyboard

ports = serial.tools.list_ports.comports();
port = ports[0][0]

bb = Blinkyboard(port, 60, 'WS2811', gamma=[2,1,4])
bb.allOff()

#url = "http://www.aqicn.info/city/hongkong/"
#url = "http://www.aqicn.info/city/shenzhen/"
url = "http://www.aqicn.info/city/shenzhen/huaqiaocheng/"
#url = "http://www.aqicn.info/city/beijing/"
#url = "http://www.aqicn.info/city/shanghai/"
#url = "http://www.aqicn.info/"

positions = [243, 238, 233, 228, 223, 218, 213, 208, 203, 198, 193, 188, 183, 178, 173, 168, 163, 158, 153, 148, 143, 138, 133, 128, 123, 118, 113]


try:
  while True:
    try:
      print "[%d] Scraping %s" % (time.time(), url)
      data = urllib.urlopen(url)
      soup = BeautifulSoup(data, "html5lib")
      imgs = soup.find_all(id="img_pm25")
      #print imgs
      if len(imgs):
        imgurl = imgs[0]['src']
  
        #print "Parsing image"
        imgdata = base64.b64decode(imgurl[22:])
        tmp = open("data.png", "w")
        tmp.write(imgdata)
        tmp.close()
        img = Image.open("data.png")
        img = img.convert('RGB')
        
        end = time.time() + 60*30;

        delay = 0.75
        yheight = 25

        while (time.time() < end):

          for x in positions:
            r, g, b = img.getpixel((x, yheight))
            #print r, g, b
            bb.sendPixel(r, g, b);
          bb.show()

          time.sleep(delay)

          for idx, x in enumerate(positions):
            r, g, b = img.getpixel((x, yheight))
            if idx == 0:
              r = 0
              g = 0
              b = 0

            bb.sendPixel(r, g, b);
          bb.show()
          
          time.sleep(delay)
        # time.sleep(60*30)
      else:
        print "Site down."
        time.sleep(60)
    except KeyboardInterrupt as ex:
      raise ex
    except Exception as ex:
      print ex
except KeyboardInterrupt as ex:
  print "Exiting."