import UserInterface
import os
import re
#import pygame
import unittest

class Menu(object):
  """
  Display a menu of all files in the given directory that match the given
  filename, and allow the user to select one and run it.

  The menu looks like this:
  item1  <- Min item
  item2
  item3  <- Top item to display  <-|
  item4                          <-| Items currently being dispalyed
  item5  <- Selected item        <-|
  item6                          <-|
  item7  <- Max item

  This is a simple state machine, which draws a subset of the available items
  in the item list. Unselected items are drawn with one style, and selected items
  are drawn with a different style. The top item and selected item index are updated
  when the user presses the up and down buttons.
  """

  def __init__(self, interface):
    """
    Init a new test menu.
    @param interface UserInterface to draw on
    @param items List of possible items to display
    """
    self.i = interface
#
#    self.visible_item_count = 4 # Maximum items to display at once
# 
#    self.selection_index = 0
#    self.top_visible_index = 0
# 
#    self.selection_animate_state = 0 
#    self.selection_animate_offset = 0

#  def DrawItem(self, name, position, selected):
#    """
#    Draw an unselected menu item
#    @param name Name item to dispaly
#    @param position Place to draw the item (0-3)
#    @param selected True if the current item is selected, false otherwise
#    """
#
#    if (selected):
#      color = (255,255,255)
#      self.i.screen.fill((0,0,200),(0,32*position,128,32))
#      text = self.i.font.render(name,1,color)
#
#      if (self.selection_animate_state < 15):
#        self.selection_animate_state += 1
#      elif (self.selection_animate_state == 15):
#        self.selection_animate_offset += 1
#        if (self.selection_animate_offset > text.get_width() + 10):
#          self.selection_animate_state = 0
#          self.selection_animate_offset = 0
# 
#      offset = -self.selection_animate_offset
#      self.i.screen.blit(text, (offset,32*position))
#      self.i.screen.blit(text, (offset+text.get_width() + 10,32*position))
#
#    else:
#      color = (0,0,0)
#      text = self.i.font.render(name,1,color)
#      offset = 0
#      self.i.screen.blit(text, (offset,32*position))


  def DrawMenu(self):
    """ Draw the current menu screen """
#    self.i.screen.fill((255,255,255))
#
#    for i in range(0, self.visible_item_count):
#      index = self.top_visible_index + i
#      selected = (index == self.selection_index)
#
#      #if this is a valid item, draw it
#      if (index < len(self.items)):
#        name = str(index + 1) + ":" + self.items[index][0]
#        self.DrawItem(name,i,selected)
#    
#    # TODO: rotate screen at framebuffer level
#    screen = pygame.transform.rotate(self.i.screen.subsurface(pygame.Rect(0,0,128,128)), 180)
#    self.i.screen.blit(screen, self.i.displayRect.topleft)
#
#    pygame.display.flip()

    print ""
    i = 1
    for entry in self.items:
      print str(i) + ". " + entry[0]
      i = i + 1

  def Display(self):
    """ Run an interactive menu """
    while True:
      self.DrawMenu()
      s = raw_input("Type a selection or press enter to run all tests")
      try:
        if len(s) == 0:
	  n = 0
        else:
          n = int(s) - 1
      except ValueError:
        pass
      else:
        if n >= 0 and n < len(self.items):
          self.HandleSelection(self.items[n])

#      last_selection_index = self.selection_index
#
#      for event in pygame.event.get(pygame.KEYUP):
#        if (event.key == pygame.K_UP):
#          # Try to decrease the selection index
#          self.selection_index = max(self.selection_index - 1, 0)
#          # If the selection index crashes into the top top visible index, try to decrease the top visible index.
#          if (self.selection_index == self.top_visible_index):
#            self.top_visible_index = max(self.top_visible_index - 1, 0)
#
#        if (event.key == pygame.K_DOWN or event.key == pygame.K_LEFT):
#          # Try to increase the selection index
#          self.selection_index = min(self.selection_index + 1, len(self.items) - 1)
#          # If the selection index crashes into the top top visible index, try to increase the top visible index.
#          if (self.selection_index == self.top_visible_index + self.visible_item_count - 1):
#            self.top_visible_index = min(self.top_visible_index + 1, len(self.items) - self.visible_item_count)
# 
#        if (event.key == pygame.K_RETURN or event.key == pygame.K_RIGHT):
#          self.HandleSelection(self.items[self.selection_index])
#
#        if (event.key == pygame.K_ESCAPE):
#          exit(1)
#
#      # If we have a new selection, reset the animation
#      if (last_selection_index != self.selection_index):
#        self.selection_animate_state = 0 
#        self.selection_animate_offset = 0

  def HandleSelection(self, selection):
    print "Item selected: " + str(selection)

if __name__ == '__main__':
  interface = UserInterface.interface

  # a static array for menu entries
  entries = [
          ('short name', 'a_data'),
          ('This one has a really long name', ''),
          ('Third selection', ''),
          ('Dictionary for data', {'option1':32, 'option2':10}),
          ('Last Selection', '')
  ]

  menu = Menu(interface, entries)
  menu.Display()
