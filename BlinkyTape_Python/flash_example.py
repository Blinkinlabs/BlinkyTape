from Blinkyboard import Blinkyboard
  
bb = Blinkyboard('/dev/tty.usbmodemfa131')

while True:

  for x in range(0, 60):
    bb.sendPixel(10,10,10)
  bb.show();

  for x in range(0, 60):
    bb.sendPixel(0,0,0)
  bb.show()
