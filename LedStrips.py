import serial
import time
import optparse
import array

class Color:

	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b

	def bytes(self):
		out = chr(self.r) + chr(self.g) + chr(self.b)
		return out

class LedStrips:

	frame_count = 0
	format_time_total = 0


	def __init__(self):
		"""
		Initialize an med strip
		@param offset X position of the image to get LED image data from
		"""

	def get_raw_data(self):
		out = ''
		for pixel in self.data:
			out += (pixel.bytes())
		return out

	def connect(self, port):
		self.ser = serial.Serial(port, 115200, timeout=0)

	def set_pixel(x, color):
		data[x] = color

	def draw(self, data):
		"""
		Draw a portion of an image frame to LED strips.
		@param data Image data, as a 1D, 8bit RGB array.
		"""
		self.load_data()
		self.flip()

	def load_data(self):
		"""
		Load the next frame into the strips, but don't actually clock it out.
		@param data Image data, as a 1D, 8bit RGB array.
		"""

		raw_data = self.get_raw_data()

		# Send the data out in 64-byte chunks
		#output_start_time = time.time()
		for x in range(0, len(raw_data)/64):
			t = raw_data[64 * x : (64 * x) + 64]
			self.ser.write(t)
		#output_time = time.time() - output_start_time


	def flip(self):
		# TODO: Why does 20 work? it make a'no sense.
                # 1 does not work with the listener.
		for i in range(0,64):
			self.ser.write('\x00')

if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option("-p", "--serialport", dest="serial_port",
		help="serial port (ex: /dev/ttyUSB0)", default="/dev/tty.usbmodel12341")
	parser.add_option("-l", "--length", dest="strip_length",
		help="length of the strip", default=30, type=int)

	(options, args) = parser.parse_args()

	strip = LedStrips()
    strip.connect(options.serial_port)

	i = 0
	j = 0
	while True:
		for row in range (0, options.strip_length):
			if ((row+j)%3 == 0): strip.set_pixel(Color(255, 0, 0))
			if ((row+j)%3 == 1): strip.set_pixel(Color(0, 255, 0))
			if ((row+j)%3 == 2): strip.set_pixel(Color(0, 0, 255))

			i = (i+1)%20
            if i == 0: j = (j+1)%255

	        strip.draw()
