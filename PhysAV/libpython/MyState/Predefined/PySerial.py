#MyState/Predefined/PySerial.py: Implements SigIO for PySerial
#-------------------------------------------------------------------------------
from MyState.SigTools import SignalAwareStateIF
from MyState.SigIO import IOWrapIF, SigCom, SigLink
from serial import Serial
from array import array

r"""Issues
- Changing `timeout` on `Serial` devices causes it to reset. Can't go from blocking
  to non-blocking without custom code.
- Module `serial` is not platform independent. Probably better to migrate out of MyState.
- Not particularly efficient. Much room to improve.
- Likey buggy. Feels overly complicated.
"""


#==SerialIn_Nonblocking
#===============================================================================
class SerialIn_Nonblocking():
	def __init__(self, com:Serial, szbuf=500):
		if com.timeout != 0:
			raise Exception("Timeout incorrectly configured")
		self.com = com
		self.linebuf = []
		self.buf = array("B", [0]*szbuf) #Unsigned
		self.reset_buf()
	def reset_buf(self):
		self.pos = 0

	def buf_append(self, bufin:bytes):
		char_break = (ord("\n"), ord("\r"))
		szbuf = len(self.buf)
		posbuf = self.pos
		szin = len(bufin)
		posin = 0
		newchar = 0

		while posin < szin:
			while szbuf > posbuf:
				if posin >= szin: break
				newchar = bufin[posin]
				self.buf[posbuf] = newchar
				posbuf+=1; posin+=1
				if newchar in char_break: break
			if (newchar in char_break) or (posbuf >= szbuf):
				line = bytes(self.buf[:posbuf]).decode("utf-8")
				self.linebuf.append(line)
				posbuf = 0 #Reset buffer
		self.pos = posbuf

	def readline(self):
		bufin = self.com.readline()
		if len(bufin) > 0:
			self.buf_append(bufin)
		if len(self.linebuf) > 0:
			return self.linebuf.pop(0) #Not super efficient.
		return None


#==IOWrap_PySerial
#===============================================================================
class IOWrap_PySerial(IOWrapIF):
	"""Implement IOWrapIF interface for a USB host device"""
	def __init__(self, com:Serial):
		self.com = com
		self.istream_nonblock = SerialIn_Nonblocking(com)

#Implement IOWrapIF interface:
#-------------------------------------------------------------------------------
	def readline_noblock(self):
		return self.istream_nonblock.readline()

	def readline_block(self):
		raise Exception("Not supported. Can't switch back & forth between blocking and not")

	def write(self, msgstr):
		self.com.write(msgstr)


#==Convenience constructors
#===============================================================================
def SigCom_PySerial(portid):
	com = Serial(portid, timeout=0) #default timeout=None (blocking)
	io = IOWrap_PySerial(com)
	return SigCom(io)
def SigLink_PySerial(portid, state:SignalAwareStateIF):
	com = Serial(portid, timeout=0) #default timeout=None (blocking)
	io = IOWrap_PySerial(com)
	return SigLink(io, state)
