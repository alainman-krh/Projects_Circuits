#CouchVolumeAV_2040pico\filter_adc.py
#-------------------------------------------------------------------------------

class FilterADC:
	"""Filters ADC values to avoid wandering codes due to noise

	For algorithm efficiency:
	- Filter lengths must be powers of 2.
	- ADC values must be integers.
	"""
	def __init__(self, nbits_len, thresh, deltamin):
		"""
		#NOTE:
		- filter length = 2^nbits_len. Pick something that won't overflow given 
		- UPDATE: Algorithm doesn't actually need power of 2. Keeping just in case.
		"""
		N = 1<<nbits_len
		self.mask = N-1
		self.buf = [0]*N
		self.thresh = int(thresh)
		self.deltamin = int(deltamin)
		self.pos = 0

		self.activeval = 0

	def getfiltered(self, newval):
		if abs(newval - self.activeval) > self.thresh:
			#Sigificantly different newval. Do not filter:
			self.pos = 0
			self.activeval = newval
			return newval
		else: #newval is similar to previous. Must filter.
			self.buf[self.pos] = newval
			self.pos = (self.pos+1) & self.mask
			if 0 == self.pos:
				newval = int(sum(self.buf) / len(self.buf)) #Assumes values are integers
				#Only update if > deltamin. Avoids ping-pong between values
				if (newval - self.activeval) > self.deltamin:
					self.activeval = newval #Sufficiently different to update
		return self.activeval #Keep last value until changes sufficiently.
		
