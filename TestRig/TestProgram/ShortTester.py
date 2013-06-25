#! /usr/bin/env python
import serial
import time

class TestPin:
  def __init__(self, name, number, type):
    self.name = name
    self.number = number
    self.type = type

  def __str__(self):
    return self.name

GND  = 0
IO   = 1
VCC  = 2

shortTestPins = [
#  TestPin('ANALOG_IN',  0, IO),   #Not a pogo pin yet
#  TestPin('BUTTON'      1, IO),   #Not probable yet (RevD?)
  TestPin('ICSP_MISO',  2, IO),
  TestPin('ICSP_SCK',   3, IO),
  TestPin('ICSP_RESET', 4, IO),
  TestPin('ICSP_MOSI',  5, IO),
  TestPin('USB_VCC',    6, VCC),
  TestPin('USB_GND',    7, GND),
  TestPin('USB_D+',     8, IO),
  TestPin('USB_D-',     9, IO),
  TestPin('OUT_SIG',   10, IO),   # No pogo pin yet!
  TestPin('OUT_VCC',   11, VCC),  # No pogo pin yet!
  TestPin('OUT_GND',   12, GND),  # No pogo pin yet!
  ]

# List of pins that are expected to be shorted. All others must be open.
# TODO: Explicitly test for shorts here
knownShortCircuits = [
  ('ICSP_GND', 'ICSP_VCC'),
  ('ICSP_GND', 'OUT_VCC'),
  ('OUT_GND', 'ICSP_VCC'),
  ('OUT_GND', 'OUT_VCC')
]

class TestRig:
  def __init__(self, port):
    self.serial = serial.Serial(port)

  def analogRead(self, testPin):
    self.serial.write('m')
    self.serial.write(chr(testPin.number))
    return float(self.serial.readline())

  def digitalRead(self, testPin):
    self.serial.write('r')
    self.serial.write(chr(testPin.number))
    return int(self.serial.readline())

  def pinMode(self, testPin, mode):
    if mode == 'OUTPUT':
      self.serial.write('o');
      self.serial.write(chr(testPin.number))
    elif mode == 'INPUT':
      self.serial.write('i');
      self.serial.write(chr(testPin.number))
    elif mode == 'INPUT_PULLUP':
      self.serial.write('p');
      self.serial.write(chr(testPin.number))

  def digitalWrite(self, testPin, value):
    if value == 'HIGH':
      self.serial.write('h')
    elif value == 'LOW':
      self.serial.write('l')
    self.serial.write(chr(testPin.number))


testRig = TestRig('/dev/cu.usbmodemfd121')

faults = []

# Step through each pin, setting it as a low output, then reading in the value of all other pins
for pin in shortTestPins:
  # Short everything together by setting it to high output, to discharge passives
  for p in shortTestPins:
    testRig.pinMode(p, 'OUTPUT')
    testRig.digitalWrite(p, 'HIGH')
  time.sleep(.05)

  # Reset all pins to inputs
  for p in shortTestPins:
    testRig.pinMode(p, 'INPUT')

  # Set the left-side pin to low output
  print 'Setting pin ' + str(pin) + ' low'
  testRig.pinMode(pin, 'OUTPUT')
  testRig.digitalWrite(pin, 'LOW')

  # Now, iterate through all the other pins
  for inputPin in shortTestPins:
    if (pin.name != inputPin.name) \
        and (pin.type <= inputPin.type):
      testRig.pinMode(inputPin, 'INPUT_PULLUP')
      time.sleep(.05)
      val = testRig.digitalRead(inputPin)

      if val != 1:
        known = False
        for circuit in knownShortCircuits:
          if (str(pin) == circuit[0]) \
              and (str(inputPin) == circuit[1]):
            known = True
        
        if not known:
          faults.append((pin, inputPin))

      testRig.pinMode(inputPin, 'INPUT')

if len(faults) == 0:
  print "PASS: No faults detected"
else:
  for fault in faults:
    print 'FAIL: Fault detected! Pin ' + str(fault[0]) + ' shorted to ' + str(fault[1])
