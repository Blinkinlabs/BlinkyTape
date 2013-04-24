from Blinkyboard import Blinkyboard
  
bb = Blinkyboard('/dev/cu.usbmodem1d11', 'WS2811')

while True:

  for x in range(0, 60):
    bb.sendPixel(255,255,255)
  bb.show();

  for x in range(0, 60):
    bb.sendPixel(0,0,0)

  bb.show()