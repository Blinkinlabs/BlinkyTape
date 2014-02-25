import time
import pygame
import textrect
import TestRig

class UserInterface():
  """
  The user interface is a simple class for displaying messages on the LCD screen,
  and reading input from the front keypad.
  """
  screen = {}

  def __init__(self):
    self.rig = TestRig.testRig

    pygame.init()
    size=[320,240]
    self.screen=pygame.display.set_mode(size)
    pygame.mouse.set_visible(False)

    self.font = pygame.font.Font("FreeMono.ttf", 20)
    self.displayRect = pygame.Rect((0,0,320,240))
   
  def DisplayFill(self, color):
    """
    Fill screen in a color
    @param color Fill color (RGB tuple)
    """
    self.screen.fill(color)
    pygame.display.flip()
    pass

  def DisplayMessage(self, message, color=(255,255,255), bgcolor=(0,0,0), boxed=False): 
    """
    Display a message on the screen
    @param message Message to display, can be multi-line
    @apram color Text color (RGB tuple)
    @param bgcolor Background color (RGB tuple)
    """
    self.screen.fill(bgcolor, self.displayRect)

    text = textrect.render_textrect(message,self.font,self.displayRect,color,bgcolor,0)
   
    self.screen.blit(text, self.displayRect.topleft)

    pygame.display.flip()
    if boxed:
      print "**********************************************************************"
      print ""
    print message
    if boxed:
      print ""
      print "**********************************************************************"

  def DisplayPass(self, message = 'PASS', timeout=.5):
    """
    Display a pass message to the user, for a given amout of time.
    @param timeout Time to display the message, in seconds
    """
    self.DisplayMessage(message, color=(0,0,0), bgcolor=(0,255,0), boxed=True)
    time.sleep(timeout)

  def DisplayError(self, message = 'ERROR', timeout=.5):
    """
    Display a failure message to the user, for a given amout of time.
    @param timeout Time to display the message, in seconds
    """
    self.DisplayMessage(message, color=(0,0,0), bgcolor=(255,0,0), boxed=True)
    
  def DisplayFail(self, message = 'FAIL', timeout=.5):
    """
    Display a failure message to the user, for a given amout of time.
    @param timeout Time to display the message, in seconds
    """
    self.DisplayMessage(message, color=(0,0,0), bgcolor=(255,0,0), boxed=True)
    time.sleep(timeout)

  def Notify(self, message, color=(255,255,255), bgcolor=(0,0,0), strobe = False, strobeColor = (0,0,1)):
    """
    Display a message, then wait for user conformation
    To confirm that a message was received, press the right arrow key.
    @param message Messgae to display, can be multi-line
    """
    self.DisplayMessage(message, color, bgcolor, boxed=True)
    
#    pygame.event.clear()  # clear previous events
#    
#    while True:
#      for event in pygame.event.get(pygame.KEYUP):
#        if (event.key == pygame.K_RIGHT):
#          return 
    raw_input('Press return to continue')

  def StrobeInit(self, scMax = 10.0):
    self.sc = 0.0
    self.scDir = True
    self.scMax = scMax
  
  def UpdateStrobe(self, strobeColor):
    red = strobeColor[0] * (self.sc/self.scMax)
    green = strobeColor[1] * (self.sc/self.scMax)
    blue = strobeColor[2] * (self.sc/self.scMax)

    if self.scDir:
      self.sc += 1.0
    else:
      self.sc -= 1.0
    if self.sc > self.scMax:
      self.scDir = False
    elif self.sc < 0:
      self.scDir = True
      self.sc = 0.0

  def YesNo(self, message, color=(255,255,255), bgcolor=(0,0,0), strobe = False, strobeColor = (0,0,1)):
    """
    Display a question, then prompt user for yes/no response
    To select yes, press the right arrow key. To select down, press the
    down arrow key.
    @param message Messgae to display, can be multi-line
    @return true if yes was selected, false otherwise
    """
    self.DisplayMessage(message, color, bgcolor, boxed=True)

#    pygame.event.clear()  # clear previous events
#
#    while True:
#      for event in pygame.event.get(pygame.KEYUP):
#        if (event.key == pygame.K_RIGHT):
#          return True
#        if (event.key == pygame.K_UP):
#          return False
    s = ''
    while(s != 'y' and s != 'n'):
      s = raw_input('y for yes, n for no')
    return s == 'y'


# Declare a single instance of the user interface, that all modules can share
# TODO: This is so that new modules can be loaded dynamically and run, but there
# is probably a more elegent way to do this.
interface = UserInterface()
