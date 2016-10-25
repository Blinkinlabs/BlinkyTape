import os
import re
import unittest
import inspect
import time
import traceback
import sys

import Logger
import Menu  
import UserInterface
import BlinkyTapeUnitTest
import Config
import menus

class PcbaTestMenu(Menu.Menu):
  """
  Display a menu of the functional tests. When a functional test is selected,
  the pyunit test loader is used to load and run all tests from the module.
  """
  items = []

  def __init__(self, interface):
    # Look up which menu item to display, then display it.
    config = Config.Config()
    self.menu_name = config.get('Menu','name','pcba_test')
    self.items = list(menus.menus[self.menu_name])

    super(PcbaTestMenu, self).__init__(interface)

  def HandleSelection(self, selection):
    # Remove the extension before attempting to load the module.
    module_name = selection[1]

    if type(module_name) is list:
      allTests = unittest.TestSuite()
      for module_n in module_name:
        module = __import__(module_n)
        tests = unittest.defaultTestLoader.loadTestsFromModule(module)
        allTests.addTests(tests)

      runner = BlinkyTapeUnitTest.BlinkyTapeTestRunner()
      result = runner.run(allTests)

    elif (module_name.startswith('test')):
      module = __import__(module_name)

      tests = unittest.defaultTestLoader.loadTestsFromModule(module)

      runner = BlinkyTapeUnitTest.BlinkyTapeTestRunner()
      result = runner.run(tests)

    elif (module_name.startswith('menu')):
      module = __import__(module_name)

      # Look for the first class which inherits from Menu, then load it.
      for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
          for base in obj.__bases__:
            if (base == Menu.Menu):
              menu = obj(self.i)
              menu.Display()

if __name__ == '__main__':
  try:
    Logger.logger.Init()

    interface = UserInterface.interface
    interface.DisplayMessage("Loading test interface...")

    menu = PcbaTestMenu(interface)
    menu.Display()
  except Exception as err:
    traceback.print_exc(file=sys.stderr)
    UserInterface.interface.DisplayError(str(err))
    while True:
      time.sleep(500)

