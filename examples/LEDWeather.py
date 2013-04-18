# Original example by Zach Hoeken Smith (http://hoektronics.com)
# Modified for the new Blinkyboard library by Max Henstell 3/2013
# Modified for Weather Underground by Marty McGuire 4/2013
# To use this behind a proxy, set the http_proxy environment variable, like so:
# export http_proxy=http://127.0.0.1:3213
# before running this script

import time
import urllib
import json
import tempfile
import serial.tools.list_ports
import sys
import colorsys
import os

from Blinkyboard import Blinkyboard

# Get your API key at http://www.wunderground.com/weather/api
# Specify it here or in the WUNDERGROUND_KEY environment var. E.g.:
# $ WUNDERGROUND_KEY=abcdefg123456 python LEDWeather.py
#apikey = "abcdefg123456"
apikey = os.environ.get('WUNDERGROUND_KEY')
state = "NV"
city = "Las_Vegas"
url = "http://api.wunderground.com/api/{}/hourly/q/{}/{}.json".format(apikey, state, city)
num_leds = 32

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

  bb = Blinkyboard(port, num_leds, 'LPD8806', gamma=[1,1,1])
  bb.allOff()
  return bb


def get_hourly_data():

  print "[%d] Fetching %s" % (time.time(), url)

  try:
    page_data = urllib.urlopen(url)
    data = json.load(page_data)

    if not len(data) or data is None:
      raise Exception("Error parsing hourly data")
    return data
  
  except Exception as ex:
    print ex

color_map = {
  -10: (255,0,255),
  0: (158,0,255),
  10: (0,0,255),
  20: (0,126,255),
  30: (0,204,255),
  40: (5,247,247),
  50: (127,255,0),
  60: (247,247,5),
  70: (255,204,0),
  80: (255,153,0),
  90: (255,79,0),
  100: (204,0,0),
  110: (169,3,3),
  120: (186,50,50)
}
def color_for_temp(temp):
  """Returns an RGB color triplet for the given (Fahrenheit scale) temp.

  Temps colors taken from the Weather Channel mapping found at:
  http://wattsupwiththat.com/2008/06/26/color-and-temperature-perception-is-everything/
  """
  color = None
  for temp_ceil in sorted(color_map.iterkeys()):
    color = color_map[temp_ceil]
    if(temp < temp_ceil):
      break
  return adjust_color(color)

def adjust_color(color, dim_factor = 0.10):
  r,g,b = color
  h,s,v = colorsys.rgb_to_hsv(r/256.0, g/256.0, b/256.0)
  r,g,b = colorsys.hsv_to_rgb(h, s, v*dim_factor)
  return (int(r*256),int(g*256),int(b*256))

if __name__ == "__main__":

  bb = connect()
  data = get_hourly_data()

  if not data:
    sys.exit("Could not fetch weather data. Check your proxy settings and try again. Try: export http_proxy=PROXY_IP:PROXY_PORT before running this script.")

  for hour in data['hourly_forecast']:
    temp = int(hour['temp']['english'])
    r,g,b = color_for_temp(temp)
    print "Temp: {}. Color: {},{},{}".format(temp, r,g,b)
    bb.sendPixel(r,g,b)
  bb.show()
