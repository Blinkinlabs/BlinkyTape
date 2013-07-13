import json

class Config():
  """
  Hopefully the simplest configuration object that could possibly work.
  Configurations are stored in json format to a text file, and are updated
  immediately when accessed.
  """
  def __init__(self, filename = 'default.cfg'):
    self.filename = filename
    self.reload()

  def reload(self):
    """
    Reload all configuration data from the config file. If the file cannot be loaded,
    the configuration data is cleared. This is automatically called by module initialization,
    and should not need to be called directly.
    """
    try:
      json_data = open(self.filename,'r')
      self.data = json.load(json_data)
    except:
      self.data = {}
      pass

  def save(self):
    """
    Save the configuration data to the configuration file. This is handled automatically
    by the set() and get() functions, and should not need to be called directly.
    """
    json_data = json.dumps(self.data)
      
    file = open(self.filename,'w')
    file.write(json_data)


  def set(self, module, key, value):
    """
    Set a value in the config file
    @param module Name of the module that the config value belongs to (for example, Logger)
    @param key Name of the config option to store
    @param value Value to store
    """
    if not self.data.has_key(module):
      self.data[module] = {}

    self.data[module][key] = value
    self.save()

  def get(self, module, key, default = ""):
    """
    Retrieve a value from the config file. If the value was not previously contained
    in the config file, then the default is saved to the file, and returned.
    @param module Name of the module that the config value belongs to (for example, Logger)
    @param key Name of the config option to store
    @param default Default value of the option, used if the config file does not already
                   contain the config option.
    """
    if not self.data.has_key(module):
      self.data[module] = {}

    if not self.data[module].has_key(key):
      self.data[module][key] = default
      self.save()

    return self.data[module][key]
