#CouchVolumeAV_2040pico\filter_sense.py: Filter Sensor data
#-------------------------------------------------------------------------------


#=Constants
#===============================================================================
CPY_ADC_NBITS = 16 #CktPy-specific. Not necessarily representative of any particular ADC
CPY_ADC_MAX = (1<<CPY_ADC_NBITS)-1


#=FilterNoisy_Int
#===============================================================================
class FilterNoisy_Int:
	"""Filters integer values to avoid wandering codes due to noise

	For algorithm efficiency:
	- Filter lengths must be powers of 2.
	- Sensed values must be integers.
	"""
	def __init__(self, nbits_len, thresh_avg, thresh_noise):
		"""
		- `thresh_avg`: Threshold where averaging filter kicks in.
		- `thresh_noise`: Threshold after which averaged data is considered above noise.
		#NOTE:
		- filter length = 2^nbits_len. Pick something that won't overflow given 
		- UPDATE: Algorithm doesn't actually need power of 2. Keeping just in case.
		"""
		N = 1<<nbits_len
		self.mask = N-1
		self.buf = [0]*N
		self.thresh_avg = int(thresh_avg)
		self.thresh_noise = int(thresh_noise)
		self.pos = 0

		self.activeval = 0

	def getfiltered(self, newval):
		if abs(newval - self.activeval) > self.thresh_avg:
			#Sigificantly different newval. Do not filter:
			self.pos = 0
			self.activeval = newval
			return newval
		else: #newval is similar to previous. Must filter.
			self.buf[self.pos] = newval
			self.pos = (self.pos+1) & self.mask
			if 0 == self.pos:
				newval = int(sum(self.buf) / len(self.buf)) #Assumes values are integers
				#Only update if > thresh_noise. Avoids ping-pong between values
				if (newval - self.activeval) > self.thresh_noise:
					self.activeval = newval #Sufficiently different to update
		return self.activeval #Keep last value until changes sufficiently.
		

#=FilterRescale
#===============================================================================
class FilterRescale:
	"""Table-based implementation to reduce real-time computational load.
	NOTE:
	- Better to use smaller bit resolution on input (in_range) - especially
	  given sensors are often noisy.
	"""

	def __init__(self, out_range=(0, 10), in_range=(0, 511), out_ndigits=0, under=None, over=None):
		(out_min, out_max) = out_range
		(in_min, in_max) = in_range
		if under is None: under = out_min
		if over is None: over = out_max

		out_delta = out_max - out_min
		in_delta = in_max - in_min
		m = out_delta/in_delta
		makeint = (out_ndigits<1)

		N = in_max - in_min + 1
		fmap = [0]*N #Filter map
		for i in range(N):
			mx = round(m*i, out_ndigits)
			if makeint: mx = int(mx)
			out = mx+out_min
			out = min(max(out_min, out), out_max) #Just in case
			fmap[i] = out

		#Make properties available:
		self.fmap = fmap
		self.in_min = in_min; self.in_max = in_max
		self.under = under; self.over = over

	def getfiltered(self, newval):
		if newval < self.in_min:
			return self.under
		elif newval > self.in_max:
			return self.over
		i = newval - self.in_min
		return self.fmap[i]
