import datetime
import json
#import MySQLdb
import traceback
import sys

import TestRig
import UserInterface
import Config

class FileSink():
  def __init__(self, fileName):
    self.fileName = fileName
    print "Logging to logfile: %s" % self.fileName

    try:
      self.logFile = open(self.fileName, 'a')
    except Exception:
      self.logFile = None
      print "Cannot open USB logfile at %s" % self.fileName

  def Log(self, data):
    """ Log a message to the file """
    try:
      msg = json.dumps(data)   
      if self.logFile is not None:
        self.logFile.write(msg + '\n')
        self.logFile.flush()
    except:
      print "Error logging to file %s." % self.FileName
      #raise #prevent logging errors from killing things.

class Logger():
  def __init__(self):
    self.r = TestRig.testRig
    self.i = UserInterface.interface

    config = Config.Config()
    self.RequireDB = config.get('Logger','RequireDB',False)

    self.Verbose       = config.get('Logger','Verbose',True)
    self.ProductionRun = config.get('Logger','ProductionRun',"pp")

    self.dbHost     = config.get('Logger','dbHost',"host")
    self.dbUser     = config.get('Logger','dbUser',"user")
    self.dbPassword = config.get('Logger','dbPassword',"pw")
    self.dbDatabase = config.get('Logger','dbDatabase',"db")

    self.testIds = {}  # dictionary to store test <--> database ID mappings.

    self.sinks = []

  def Init(self):
    self.sinks.append(FileSink("./usb-log.log"))
    self.sinks.append(FileSink("./sd-log.log"))

    if self.RequireDB:
      self.InitDB() # moved to menu_functional test area.

  def InitDB(self):
    try: 
      self.db = MySQLdb.connect(host = self.dbHost, user = self.dbUser, passwd = self.dbPassword, db = self.dbDatabase)
    except Exception as err:
      self.db = None
      if self.RequireDB:
        traceback.print_exc(file=sys.stderr)
        raise Exception("CANNOT CONNECT TO DATABASE")

    self.ClearStaleEntries()
    self.LookupMachineInfo()

  def ClearStaleEntries(self):
    """Sometimes we get stale tests if the code crashes.  Clear and error them out."""
    if self.RequireDB:
      cursor = self.db.cursor()
      try:
        cursor.execute("UPDATE test_log SET test_status = 'error', test_result = 'STALLED' WHERE mac = %s AND test_status = 'running'", (self.MACAddress))
        self.db.commit()
        cursor.close()
      except Exception as err:
        traceback.print_exc(file=sys.stderr)
        self.db.rollback()
        raise Exception("DB LOGGING ERROR #6")
        
  def LookupMachineInfo(self, create = True):
    """Look to see if we have any info about our machine available."""
    if self.RequireDB:
      cursor = self.db.cursor()
      try:
        cursor.execute("SELECT * FROM machines WHERE mac = %s", (self.MACAddress))
        row = cursor.fetchone()
        if row == None:
          if create:
            self.CreateMachineEntry()
        else:
          self.MachineInfo = row
        cursor.close()
      except Exception as err:
        traceback.print_exc(file=sys.stderr)
        raise Exception("DB LOGGING ERROR #7")   

  def CreateMachineEntry(self):
    """Create a machine entry in our tracking table."""
    if self.RequireDB:
      cursor = self.db.cursor()
      try:
        cursor.execute("INSERT INTO machines (mac, production_run, machine_type, manufacture_date) VALUES (%s, %s, %s, NOW())", (self.MACAddress, self.ProductionRun, self.MachineType))
        self.db.commit()
        cursor.close()
        self.LookupMachineInfo(False) #pull it into our 
      except Exception as err:
        traceback.print_exc(file=sys.stderr)
        self.db.rollback()
        raise Exception("DB LOGGING ERROR #8")
        
  def Log(self, testName, message, extraData = None, logType = "raw", testId=0):
    """
    Logs a message during testing.  The message will be converted to a JSON string and
    sprayed across as many different output modes as possible: all file logers, and database.
    """
    data = {}
    data['production_run'] = self.ProductionRun
    data['test'] = testName
    d = datetime.datetime.today()
    data['timestamp'] = d.strftime("%Y-%m-%d %H:%M:%S")
    data['message'] = message
    data['data'] = extraData
    data['type'] = logType

    #send the data to all our various endpoints
    if self.RequireDB:
      self.LogToDB(data, testId)

    for sink in self.sinks:
      sink.Log(data)

  def LogToDB(self, data, testId=0):
    """Record the log message to the database if present."""
    if self.RequireDB:
      cursor = self.db.cursor()
      try:
        cursor.execute("INSERT INTO raw_log (result_id, production_run, mac, log_type, test_name, test_time, message, data, machine_status) VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s)",
                                            (testId, self.ProductionRun, self.MACAddress, data['type'], data['test'], data['message'], json.dumps(data['data']), json.dumps(data['status'])))
        self.db.commit()
        cursor.close()
      except:
        traceback.print_exc(file=sys.stderr)
        #self.db.rollback() #if our db has gone away... then this triggers another error.  plus mysql does not do transactions.
        #raise Exception("DB LOGGING ERROR #1") #raise #prevent logging errors from killing things.

  def GetTestId(self, testId):
    if self.RequireDB:
      return self.testIds[testId]
    else:
      return 0
      
  def TestStart(self, test):
    #insert new record into test_log table
    if self.RequireDB:
      cursor = self.db.cursor()
      try:
        cursor.execute("INSERT INTO test_log (mac, production_run, test_name, test_start, test_status) VALUES (%s, %s, %s, NOW(), 'running')",
                                            (self.MACAddress, self.ProductionRun, test.id()))
        self.db.commit()
        self.testIds[test.id()] = cursor.lastrowid #store new id test:id dictionary for later use
        cursor.close()
      except Exception as err:
        traceback.print_exc(file=sys.stderr)
        self.db.rollback()
        raise Exception("DB LOGGING ERROR #2")

    self.Log(test.id(), "START", testId=self.GetTestId(test.id()))

  def TestPass(self, test):
    tid = self.GetTestId(test.id())
    self.Log(test.id(), "PASS", test.testResultData, testId=tid)

    if self.RequireDB:
      cursor = self.db.cursor()
      try:
        cursor.execute("UPDATE test_log SET test_status = 'pass', test_end = NOW(), test_result = %s WHERE id = %s", (test.testResultData, self.GetTestId(test.id())))
        self.db.commit()
        cursor.close()
      except Exception as err:
        traceback.print_exc(file=sys.stderr)
        self.db.rollback()
        raise Exception("DB LOGGING ERROR #3")

  def TestError(self, test, err):
    tid = self.GetTestId(test.id())
    etype, value, tb = err
    data = traceback.format_exception(etype, value, tb, 10)
    self.Log(test.id(), "ERROR", data, "error", testId=tid)

    if self.RequireDB:
      cursor = self.db.cursor()
      try:
        cursor.execute("UPDATE test_log SET test_status = 'error', test_end = NOW(), test_result = %s WHERE id = %s", (test.testResultData, self.GetTestId(test.id())))
        self.db.commit()
        cursor.close()
      except Exception as err:
        traceback.print_exc(file=sys.stderr)
        self.db.rollback()
        raise Exception("DB LOGGING ERROR #4")

  def TestFail(self, test):
    tid = self.GetTestId(test.id())
    self.Log(test.id(), "FAIL", test.testResultData, testId=tid)

    if self.RequireDB:
      cursor = self.db.cursor()
      try:
        cursor.execute("UPDATE test_log SET test_status = 'fail', test_end = NOW(), test_result = %s WHERE id = %s", (test.testResultData, self.GetTestId(test.id())))
        self.db.commit()
        cursor.close()
      except Exception as err:
        traceback.print_exc(file=sys.stderr)
        self.db.rollback()
        raise Exception("DB LOGGING ERROR #5")

# Declare a single instance of the logger interface, that all modules can share
# TODO: This is so that new modules can be loaded dynamically and run, but there
# is probably a more elegent way to do this.
logger = Logger()

