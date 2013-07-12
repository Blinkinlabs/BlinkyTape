import time
import TestRig

class UserInterface():
  """
  The user interface is a simple class for displaying messages on the LCD screen,
  and reading input from the front keypad.
  """
  screen = {}

  def __init__(self):
    self.rig = TestRig.testRig
 
#    self.font = pygame.font.Font('fireflysung.ttf', 24)
#    self.font = pygame.font.Font(None,24)
#    self.displayRect = pygame.Rect((0,0,128,128))
   
  def DisplayFill(self, color):
    """
    Fill screen in a color
    @param color Fill color (RGB tuple)
    """
#    self.screen.fill(color)
#    pygame.display.flip()
    pass

  def DisplayMessage(self, message, color=(255,255,255), bgcolor=(0,0,0), boxed=False): 
    """
    Display a message on the screen
    @param message Message to display, can be multi-line
    @apram color Text color (RGB tuple)
    @param bgcolor Background color (RGB tuple)
    """
#    self.screen.fill(bgcolor, self.displayRect)
#
#    text = textrect.render_textrect(message,self.font,self.displayRect,color,bgcolor,0)
#    
#    # TODO: Handle screen rotation at the framebuffer level
#    #text = pygame.transform.rotate(text, 180)
#    self.screen.blit(text, self.displayRect.topleft)
#
#    #TODO: rotate screen at framebuffer level
#    screen = pygame.transform.rotate(self.screen.subsurface(pygame.Rect(0,0,128,128)), 180)
#    self.screen.blit(screen, self.displayRect.topleft)
#
#    pygame.display.flip()
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
#    self.r.SetRgbLed(0, 1, 0)  # show green
    self.DisplayMessage(message, color=(0,0,0), bgcolor=(0,255,0), boxed=True)
    time.sleep(timeout)
#    self.r.SetRgbLed(1,1,1)  # leds on

  def DisplayError(self, message = 'ERROR', timeout=.5):
    """
    Display a failure message to the user, for a given amout of time.
    @param timeout Time to display the message, in seconds
    """
#    self.r.SetRgbLed(1, 0, 0)  # show red
    self.DisplayMessage(message, color=(0,0,0), bgcolor=(255,0,0), boxed=True)
#    self.r.SetRgbLed(1,1,1)  # leds on
    
  def DisplayFail(self, message = 'FAIL', timeout=.5):
    """
    Display a failure message to the user, for a given amout of time.
    @param timeout Time to display the message, in seconds
    """
#    self.r.SetRgbLed(1, 0, 0)  # show red
    self.DisplayMessage(message, color=(0,0,0), bgcolor=(255,0,0), boxed=True)
    time.sleep(timeout)
#    self.r.SetRgbLed(1,1,1)  # leds on

  def Notify(self, message, color=(255,255,255), bgcolor=(0,0,0), strobe = False, strobeColor = (0,0,1)):
    """
    Display a message, then wait for user conformation
    To confirm that a message was received, press the right arrow key.
    @param message Messgae to display, can be multi-line
    """
    self.DisplayMessage(message, color, bgcolor, boxed=True)
    
#    pygame.event.clear()  # clear previous events
#    
#    if strobe:
#      self.StrobeInit()
#
#    while True:
#      if strobe:
#        self.UpdateStrobe(strobeColor)
#      for event in pygame.event.get(pygame.KEYUP):
#        if (event.key == pygame.K_RIGHT):
#          if strobe:
#            self.r.SetRgbLed(1,1,1)  # leds on
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
#    self.r.SetRgbLed(red, green, blue)

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
#    if strobe:
#      self.StrobeInit()
#  
#    while True:
#      if strobe:
#        self.UpdateStrobe(strobeColor)
#      for event in pygame.event.get(pygame.KEYUP):
#        if (event.key == pygame.K_RIGHT):
#          if strobe:
#            self.r.SetRgbLed(1,1,1)  # leds on
#          return True
#        if (event.key == pygame.K_UP):
#          if strobe:
#            self.r.SetRgbLed(1,1,1)  # leds on
#          return False
    s = ''
    while(s != 'y' and s != 'n'):
      s = raw_input('y for yes, n for no')
    return s == 'y'


# Declare a single instance of the user interface, that all modules can share
# TODO: This is so that new modules can be loaded dynamically and run, but there
# is probably a more elegent way to do this.
interface = UserInterface()
