#!/usr/bin/env python

import time
import sys
from bitstring import BitArray, BitStream, ConstBitStream

#class gen:
#	def __init__(self, fn):
#		self.f = fn
#	def next(self):
#		return self.f()
#	def __iter__(self):
#		return self

class TsPacketFileIO:

	filename=''
	filestream = None

	byte_reader = None

	wr = 'read'

#	def open(self, filename, wr='read'):
#		self.wr = wr
#		self.filename = filename
#		try:
#			if wr == 'read':
#				print 'read ' + self.filename
#				self.filestream = ConstBitStream( filename=self.filename )
#				self.byte_reader = self.filestream.cut(188*8)
#			else:
#				self.filestream = open(filename, 'wb')
#		except Exception, e:
#			raise e

	def open(self, filename, wr='read'):
		self.wr = wr
		self.filename = filename
		try:
			if wr == 'read':
				print 'read ' + self.filename
				self.filestream = open( self.filename, 'rb' )
				
				class gen:
					def __init__ (self, s):
						self.s = s
					def next(self):
						temp = self.s.read(188)
						if len(temp) != 188:
							raise StopIteration
						else:
							return bytearray(temp)
					def __iter__(self):
						return self
					
				self.byte_reader = gen(self.filestream)		
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

	os_starttime = time.clock()
	starttime = time.time()
	
	input_filename = sys.argv[1]

	reader = TsPacketFileIO()
	reader.open(filename=input_filename)
	
#	newPAT = TsPacketFileIO()
#	newPAT.open('pat.ts', 'read')
#	nPAT = next(newPAT.byte_reader)
#
#	newPMT = TsPacketFileIO
#	newPMT.open('pmt.ts', 'read')
#	nPMT = next(newPAT.byte_reader)
#	
#	newSDT = TsPacketFileIO()
#	newSDT.open('sdt.ts', 'read')
#	nSDT = next(newSDT.byte_reader)
	
#	newStream = TsPacketFileIO()
#	newStream.open(filename=sys.argv[2], wr='write')

	pids = {}
		
	for packet in reader.byte_reader:

		PID = (BitArray(packet))[11:24]

#		if PID.uint == 0:
#			newStream.writepacket(nPAT)
#		elif PID.uint == 17:
#			newStream.writepacket(nSDT)
#		elif PID.uint == 32:
#			newStream.writepacket(nPMT)
#		else:
#			newStream.writepacket(packet)
		

		p = str(PID.uint)
				
		if p in pids:
			pids[p] = pids[p] + 1
		else:
			pids[p] = 0
			

	print "PID\t\t:Number"
	
	for p in pids:
		print p +"\t\t" + str(pids[p])

	print "Done!"

	print "CPU time: " + str( time.clock() - os_starttime)
	print "TIme    : " + str( time.time() - starttime)

