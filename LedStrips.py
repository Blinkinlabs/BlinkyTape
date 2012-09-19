import serial
import time
import optparse
import array
import sys
import math
import signal
import struct

class Pixel:

	data = []

	def __init__(self, color):
		self.data = [color[1], color[0], color[2]]

	# def set_dec(self, r, g, b):
	# 	self.data = [r,g,b]

	# def set_hex(self, hex):
	# 	r = (hex >> 16) | 0xFF
	# 	g = (hex >> 8)  | 0xFF
	# 	b = (hex >> 0)  | 0xFF
	# 	self.data = [r,g,b]

	def ints(self):
		return self.data

class LedStrips:

	frame_count = 0
	format_time_total = 0

	def __init__(self, length):
		"""
		Initialize an med strip
		@param offset X position of the image to get LED image data from
		"""
		self.length = length
		self.data = [Pixel([0,0,0]) for x in range(0, self.length)]

	def get_raw_data(self):
		out = ''
		for pix in self.data:
			ints = pix.ints()
			for i in ints:
				out += chr(i | 0x80)
		return out

	def connect(self, port):
		self.ser = serial.Serial(port, 115200, timeout=0)

	def disconnect(self, signal, frame):
		print("Disconnecting")
		self.ser.close()
		sys.exit(0)

	def set_pixel(self, x, pixel):
		self.data[x] = pixel

	def draw(self):
		"""
		Draw a portion of an image frame to LED strips.
		@param data Image data, as a 1D, 8bit RGB array.
		"""
		self.load_data()
		self.flip()

	def set_data(self, data):
		s = ''
		for x in range(0, len(data) / 3):
			r =  struct.unpack("<B", data[(x*3) + 0])[0],
			g =  struct.unpack("<B", data[(x*3) + 1])[0],
			b =  struct.unpack("<B", data[(x*3) + 2])
			self.data[x] = Pixel([r[0],g[0],b[0]])

		self.load_data()

	def load_data(self):
		"""
		Load the next frame into the strips, but don't actually clock it out.
		@param data Image data, as a 1D, 8bit RGB array.
		"""

		raw_data = self.get_raw_data()

		# Send the data out in 64-byte chunks
		#output_start_time = time.time()
		for x in range(0, int(math.ceil(float(len(raw_data))/64))):
			t = raw_data[64 * x : (64 * x) + 64]
			self.ser.write(t)
		#output_time = time.time() - output_start_time



	def flip(self):
		# TODO: Why does 20 work? it make a'no sense.
                # 1 does not work with the listener.
		#for i in range(0,1):
		self.ser.write('\x00')



colors = {"red": [255,0,0], "green": [0,255,0], "blue": [0,0,255], "purple":[0x72,0,0xbe], "orange":[0xff, 0x00, 0]}

if __name__ == "__main__":

	parser = optparse.OptionParser()
	parser.add_option("-p", "--serialport", dest="serial_port", help="serial port (ex: /dev/ttyUSB0)", default="/dev/tty.usbmodem40001")
	parser.add_option("-l", "--length", dest="strip_length", help="length of the strip", default=30, type=int)

	(options, args) = parser.parse_args()

	strip = LedStrips(options.strip_length)
	strip.connect(options.serial_port)

	signal.signal(signal.SIGINT, strip.disconnect)


	i = 0
	j = 0

	while True:
		for pixel in range(0, options.strip_length):
			#strip.set_pixel(pixel, Pixel(colors['orange']))
			if ((pixel+j)%3 == 0): strip.set_pixel(pixel, Pixel(colors['red']))
			if ((pixel+j)%3 == 1): strip.set_pixel(pixel, Pixel(colors['green']))
			if ((pixel+j)%3 == 2): strip.set_pixel(pixel, Pixel(colors['blue']))

			i = (i+1)%20
			if i == 0: j = (j+1)%255

		strip.draw()

