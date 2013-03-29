import serial
import time
import urllib
from bs4 import BeautifulSoup
import Image
import base64
import tempfile
import serial.tools.list_ports

class blinkyBoard:
  def init(self, port, baud):
    self.serial = serial.Serial(port, baud)
    self.rgamma = 2.0
    self.ggamma = 1.0
    self.bgamma = 4.0

  def sendPixel(self,g,r,b):
    data = bytearray()
    
    r = self.gamma(r, self.rgamma)
    g = self.gamma(g, self.ggamma)
    b = self.gamma(b, self.bgamma)
    
    data.append(0x80 | (r>>1))
    data.append(0x80 | (g>>1))
    data.append(0x80 | (b>>1))
    self.serial.write(data)
    self.serial.flush()
    
  def gamma(self, input, tweak):
    return int(pow(input/256.0, tweak) * 256)

  def sendBreak(self):
    data = bytearray()
    for i in range(0,8):
      data.append(0x00)
    self.serial.write(data)
    self.serial.flush()

ports = serial.tools.list_ports.comports();
port = ports[0][0]

blink = blinkyBoard()
blink.init(port, 57600)

#url = "http://www.aqicn.info/city/hongkong/"
#url = "http://www.aqicn.info/city/shenzhen/"
url = "http://www.aqicn.info/city/shenzhen/huaqiaocheng/"
#url = "http://www.aqicn.info/city/beijing/"
#url = "http://www.aqicn.info/city/shanghai/"
#url = "http://www.aqicn.info/"

positions = [243, 238, 233, 228, 223, 218, 213, 208, 203, 198, 193, 188, 183, 178, 173, 168, 163, 158, 153, 148, 143, 138, 133, 128, 123, 118, 113]

for i in range(0, 30):
  blink.sendPixel(0,0,0);
blink.sendBreak()

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
            blink.sendPixel(r, g, b);
          blink.sendBreak()

          time.sleep(delay)

          for idx, x in enumerate(positions):
            r, g, b = img.getpixel((x, yheight))
            if idx == 0:
              r = 0
              g = 0
              b = 0

            blink.sendPixel(r, g, b);
          blink.sendBreak()
          
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