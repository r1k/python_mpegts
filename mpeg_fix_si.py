#!/usr/bin/env python

import sys
from bitstring import BitArray, BitStream, ConstBitStream


class TsPacketFileIO:

	filename=''
	filestream = None

	byte_reader = None

	wr = 'read'

	def open(self, filename, wr='read'):
		self.wr = wr
		self.filename = filename
		try:
			if wr == 'read':
				self.filestream = ConstBitStream( filename=self.filename )
				self.byte_reader = self.filestream.cut(188*8)
			else:
				self.filestream = open(filename, 'wb')
		except Exception, e:
			raise e

	def getpacket(self):
		if self.wr == 'read':
			return next(self.byte_reader)
		else:
			raise Exception("trying to write to input stream")

	def writepacket(self, packet):
		if self.wr == 'write':
			self.filestream.write(packet.tobytes())
		else:
			raise Exception("trying to read from output stream")


if __name__ == '__main__':

	input_filename = sys.argv[1]
	output_filename = sys.argv[2]

	pid = int(sys.argv[3])

	reader = TsPacketFileIO()
	reader.open(filename=input_filename)

	writer = TsPacketFileIO()
	writer.open(filename=output_filename, wr='write')

	for packet in reader.byte_reader:

		PID = packet[11:24]

		if pid == PID.uint:

			writer.writepacket(packet)

	print "Done!"

