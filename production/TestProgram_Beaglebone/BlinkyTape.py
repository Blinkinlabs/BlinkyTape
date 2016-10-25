"""BlinkyTape Python communication library.

  This code assumes stock serialLoop() in the firmware.

  Commands are issued in 3-byte blocks, with pixel data
  encoded in RGB triplets in range 0-254, sent sequentially
  and a triplet ending with a 255 causes the accumulated pixel
  data to display (a show command).

  Note that with the stock firmware changing the maximum brightness
  over serial communication is impossible.
"""

import serial


class BlinkyTape(object):
    def __init__(self, port, ledCount=60, buffered=True):
        """Creates a BlinkyTape object and opens the port.

        Parameters:
          port
            Required, port name as accepted by PySerial library:
            http://pyserial.sourceforge.net/pyserial_api.html#serial.Serial
            It is the same port name that is used in Arduino IDE.
            Ex.: COM5 (Windows), /dev/ttyACM0 (Linux).
          ledCount
            Optional, total number of LEDs to work with,
            defaults to 60 LEDs. The limit is enforced and an
            attempt to send more pixel data will throw an exception.
          buffered
            Optional, enabled by default. If enabled, will buffer
            pixel data until a show command is issued. If disabled,
            the data will be sent in byte triplets as expected by firmware,
            with immediate flush of the serial buffers (slower).

        """
        self.port = port
        self.ledCount = ledCount
        self.position = 0
        self.buffered = buffered
        self.buf = ""
        self.serial = serial.Serial(port, 115200)
        self.show()  # Flush any incomplete data

    def send_list(self, colors):
        if len(colors) > self.ledCount:
            raise RuntimeError("Attempting to set pixel outside range!")
        for r, g, b in colors:
            self.sendPixel(r, g, b)
        self.show()

    def send_list(self, colors):
        data = ""
        for r, g, b in colors:
            if r >= 255:
                r = 254
            if g >= 255:
                g = 254
            if b >= 255:
                b = 254
            data += chr(r) + chr(g) + chr(b)
        self.serial.write(data)
        self.show()

    def sendPixel(self, r, g, b):
        """Sends the next pixel data triplet in RGB format.

        Values are clamped to 0-254 automatically.

        Throws a RuntimeException if [ledCount] pixels are already set.
        """
        data = ""
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0
        if r >= 255:
            r = 254
        if g >= 255:
            g = 254
        if b >= 255:
            b = 254
        data = chr(r) + chr(g) + chr(b)
        if self.position < self.ledCount:
            if self.buffered:
                self.buf += data
            else:
                self.serial.write(data)
                self.serial.flush()
            self.position += 1
        else:
            raise RuntimeError("Attempting to set pixel outside range!")

    def show(self):
        """Sends the command(s) to display all accumulated pixel data.

        Resets the next pixel position to 0, flushes the serial buffer,
        and discards any accumulated responses from BlinkyTape.
        """
        control = chr(0) + chr(0) + chr(255)
        if self.buffered:
            self.serial.write(self.buf + control)
            self.buf = ""
        else:
            self.serial.write(control)
        self.serial.flush()
        self.serial.flushInput()  # Clear responses from BlinkyTape, if any
        self.position = 0

    def displayColor(self, r, g, b):
        """Fills [ledCount] pixels with RGB color and shows it."""
        for i in range(0, self.ledCount):
            self.sendPixel(r, g, b)
        self.show()

    def resetToBootloader(self):
        """Initiates a reset on BlinkyTape.

        Note that it will be disconnected.
        """
        self.serial.setBaudrate(1200)
        self.close()

    def close(self):
        """Safely closes the serial port."""
        self.serial.close()


# Example code

if __name__ == "__main__":

    import glob
    import optparse

    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", dest="portname",
                      help="serial port (ex: /dev/ttyUSB0)", default=None)
    (options, args) = parser.parse_args()

    if options.portname is not None:
        port = options.portname
    else:
        serialPorts = glob.glob("/dev/cu.usbmodem*")
        port = serialPorts[0]

    bt = BlinkyTape(port)

    while True:
        bt.displayColor(255, 0, 0)
        bt.displayColor(0, 255, 0)
        bt.displayColor(0, 0, 255)
        bt.displayColor(255, 255, 255)
        bt.displayColor(0, 0, 0)
