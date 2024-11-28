#MyState/SigIO
#-------------------------------------------------------------------------------
from .Signals import SigUpdate, SigSet, SigGet, SigIncrement, SigToggle
from .Signals import SigAbstract, SigValue, SigDump
from .SigTools import SignalAwareStateIF, Signal_Deserialize
from .IOWrap import IOWrapIF, IOWrap_Script


#==Constants
#===============================================================================
MSGDUMP_EOT = "DMP EOT"
MSG_SIGACK = "ACK" #For blocking transmissions (if not returning SigValue)


#==SigCom
#===============================================================================
class SigCom:
	r"""Base "signal" communication layer.
	TODO:
	- Find a way NOT to create list of signals when reading IO-stream (using Signal_Deserialize).
	- Likely beneficial to minimize allocations."""

	def __init__(self, io:IOWrapIF):
		self.io = io
		self.sigqueue = [] #Unprocessed signals/messages
		self.cache_sigval = SigValue("", "", 0) #For sending OUT signals

#-------------------------------------------------------------------------------
	def _cache_siglist_append(self, siglist):
		if (siglist is None) or (len(siglist) < 1):
			pass #Nothing to append
		else:
			self.sigqueue.extend(siglist)
		return self.sigqueue

#-------------------------------------------------------------------------------
	def send_signal(self, sig:SigAbstract):
		"""Send a signal through this IO interface.
		Blocks on SigGet for a limited amount of time (don't hang).

		Returns SigValue (return for SigGet), True for simple Signal ack, or None on error/timeout.
		"""
		needsval = (type(sig) is SigGet)
		block = needsval #Might decouple in future - but now: only block (for limited time) on SigGet.

		msgstr = sig.serialize()
		if not block:
			#self.io.write("!") #TODO: Have a flag to indicate non-blocking?
			self.io.write(msgstr)
			self.io.write("\n")
			return True #Assume worked

		#self.io.write("?") #TODO: Have a flag to indicate blocking/needing response?
		self.io.write(msgstr)
		self.io.write("\n")
		ans_str = self.io.readline_block() #Might timeout, get bad response, etc (must keep going)
		if ans_str is None:
			return None #Error
		ans_str = ans_str.strip()
		siglist_new = Signal_Deserialize(ans_str) #Check for new signals
		ans_sig = siglist_new[-1] #Last element likely the answer.
		if needsval: #Currently suports: SigGet / expecting SigValue
			issought = False #Recieved what we asked?
			if (SigValue == type(ans_sig)) and (ans_sig.section == sig.id) and (ans_sig.id == sig.id):
				issought = True

			if issought:
				self._cache_siglist_append(siglist_new[:-1])
				return ans_sig.val
			else:
				#Don't try too hard. Can't guarantee signal order
				self._cache_siglist_append(siglist_new)
				return None #Error

		#Simple ack expected (else: None):
		result = (MSG_SIGACK == ans_str)
		return result

#-------------------------------------------------------------------------------
	def getvalue_orhang(self, sig:SigGet):
		"Will try until succeeds"
		#TODO? Is this a good idea?
		pass

#-------------------------------------------------------------------------------
	def signalqueue_processio(self):
		"""Read in/cache any signal available in `self.io`.
		"""
		#Read in new signals so they don't fill up IO queue:
		while True:
			msgstr = self.io.readline_noblock()
			if msgstr is None:
				break #Done
			#print("NEWMSG"); print(msgstr)
			newsiglist = Signal_Deserialize(msgstr.strip())
			self._cache_siglist_append(newsiglist)

#-------------------------------------------------------------------------------
	def signalqueue_isempty(self):
		return (len(self.sigqueue) < 1)

	def signalqueue_popnext(self):
		"""Must first run .signalqueue_processio()"""
		q = self.sigqueue
		if len(q) < 1:
			return None
		sig = q[0]
		if (len(q) < 2):
			self.sigqueue.clear()
		else:
			self.sigqueue = q[1:] #Update cache
		return sig


#==SigLink
#===============================================================================
class SigLink(SigCom): #Must implement IOWrapIF
	r"""Establishes a direct link between `SigIO` and `SignalAwareStateIF`."""

	def __init__(self, io:IOWrapIF, state:SignalAwareStateIF):
		super().__init__(io)
		self.state = state

#-------------------------------------------------------------------------------
	def _signal_dump(self, sig:SigDump):
		msg_list = self.state.state_getdump(sig.section)
		for msg in msg_list:
			self.io.write(msg); self.io.write("\n")
		self.io.write(MSGDUMP_EOT); self.io.write("\n")
		return True #wasproc

#-------------------------------------------------------------------------------
	def _signal_get(self, sig:SigGet):
		val = self.state.state_getval(sig.section, sig.id)
		if val is None:
			self.io.write(MSG_SIGACK); self.io.write("\n") #Need some reply
			return False #wasproc
		self.cache_sigval.id = sig.id
		self.cache_sigval.section = sig.section
		self.cache_sigval.val = val
		msgval = self.cache_sigval.serialize()
		self.io.write(msgval); self.io.write("\n")
		return True #wasproc

#-------------------------------------------------------------------------------
	def process_signals(self):
		"""Process any incomming signals"""
		#Read in new signals so they don't fill up IO queue:
		self.signalqueue_processio()
		success = True

		while not self.signalqueue_isempty():
			#NOTE: A single signal can have multiple components (ex: R,G,B)
			sig = self.signalqueue_popnext()
			if type(sig) is SigGet:
				wasproc = self._signal_get(sig)
			elif type(sig) is SigDump:
				wasproc = self._signal_dump(sig)
			else:
				wasproc = self.state.process_signal(sig)
				#Acknowledge signal even if not detected:
				self.io.write(MSG_SIGACK); self.io.write("\n")
			success &= wasproc


#==Convenience constructors (SigCom_Script/SigLink_Script)
#===============================================================================
def SigCom_Script(scriptlines=tuple()):
	io = IOWrap_Script(scriptlines)
	return SigCom(io)
def SigLink_Script(state:SignalAwareStateIF, scriptlines=tuple()):
	io = IOWrap_Script(scriptlines)
	return SigLink(io, state)

#Last line