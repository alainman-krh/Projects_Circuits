#CouchVolumeAV_2040pico\main.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.Timebase import now_ms, ms_elapsed
from filter_adc import FilterADC
from analogio import AnalogIn
import board


#=Platform/build-dependent config (RP2040-Pico)
#===============================================================================
#HW: Behringer Monitor 1 sensed with RP2040-Pico
volmainp_pin = board.GP28
volmainn_pin = board.GP27


#=Configuration Options (Yamaha RXV-475)
#===============================================================================
MSGBASE_VOLMAIN = "SIG CTRL:MAINVOL " #Add: Volume
volmain_normrange = (0.01, 0.99) #ADC sense limits normalized between (0, 1).
#Can go downto -80dB... but limit to -40 due to log potentiometer range issue:
volmain_dbrange = (-40, -10) #Safety: Don't let knob go beyond -10. Use remote/RXV if needed
volmain_mute = -90 #Indicates mute is desired (avoids separate signal)
volmain_stop_per_db = 2 #2 stops per dB (0.5dB steps)
#Averaging filter length used to suppress volume changes due to measurement noise:
avgfilt_nbits_len = 5 #32 samples. NOTE: keep <16bit to avoid overflow/use of largeint????
avgfilt_thresh_nstops = 4 #How many stops of noise do we have to filter?
avgfilt_deltamin_nstops = 1 #How many stops does the average have to change before registering?
Tupdate_ms = 100 #ms: Maximum update rate


#==VolumeState object
#===============================================================================
class VolumeState:
	def __init__(self, Tupdate_ms):
		self.ismute = True
		self.stopidx = 0 #Current "stop" index (volume level)
		self.canupdate = True
		self.lastupdate_ms = now_ms()
		self.Tupdate_ms = Tupdate_ms

	def tryupdate(self, ismute_new, stopidx_new):
		_now_ms = now_ms()
		if not self.canupdate:
			if ms_elapsed(self.lastupdate_ms, _now_ms) > self.Tupdate_ms:
				self.canupdate = True
			else:
				return False

		changed = (ismute_new != self.ismute) or (stopidx_new != self.stopidx)
		if changed:
			self.ismute = ismute_new
			self.stopidx = stopidx_new
			self.lastupdate_ms = _now_ms
			self.canupdate = False
			return True
		return False


#==Global declarations
#===============================================================================
ADC_max = 65535 #CktPy-specific. Not neccassarily representative of #of bits
(volmain_dbmin, volmain_dbmax) = volmain_dbrange #unpack (convenience)
volmain_Nstops = (volmain_dbmax - volmain_dbmin)*volmain_stop_per_db #Actually # of stops -1... or last index
volmain_cmin = round(min(volmain_normrange)*ADC_max) #Minimum ADC code
volmain_crange = round(ADC_max*(max(volmain_normrange)-min(volmain_normrange)))
#Convert delta code to # of stops:
volmain_stops_per_code = volmain_crange // (volmain_Nstops)
volmain_c2stops = (volmain_Nstops)/volmain_crange
#Senses differential volume potentiometer:
volmainp = AnalogIn(volmainp_pin)
volmainn = AnalogIn(volmainn_pin)
volmain_state = VolumeState(Tupdate_ms) #Main volume state
volmain_filt = FilterADC(avgfilt_nbits_len, #Filter ADC/resistor noise
	thresh=int(avgfilt_thresh_nstops*volmain_stops_per_code),
	deltamin=int(avgfilt_deltamin_nstops*volmain_stops_per_code)
)


#=Main loop
#===============================================================================
print("HELLO24") #DEBUG: Change me to ensure uploaded version matches.
print(f"CouchVolumeAV: ready to rock!")
#COM_VOLCTRL.io.write("\n") #Not sure why... but seems to be needed to not miss first message
while True:
	#Read raw ADC values:
	volmain_raw = (volmainp.value - volmainn.value)
	volmain_read = volmain_filt.getfiltered(volmain_raw)
	#print(f"volmain_read: {volmain_read} (volmainp: {volmainp.value}, volmainn: {volmainn.value})")

	#Convert to "stop index":
	ismute_now = (volmain_read <= volmain_cmin)
	volmain_stopidx_now = round((volmain_read-volmain_cmin) * volmain_c2stops)
	volmain_stopidx_now = min(max(0, volmain_stopidx_now), volmain_Nstops) #Clamp

	changed = volmain_state.tryupdate(ismute_now, volmain_stopidx_now)
	if not changed:
		pass
	elif volmain_state.ismute:
		#print("MUTED!")
		print(MSGBASE_VOLMAIN, end="")
		print(volmain_mute*10)
	else:
		#Only compute dB if necessary:
		volmain_db = volmain_dbmin + volmain_state.stopidx/volmain_stop_per_db
		#print(f"volmain_stopidx: {volmain_state.stopidx}, volmain_db: {volmain_db}")
		volmain_dbx10 = round(volmain_db*10)
		print(MSGBASE_VOLMAIN, end="")
		print(volmain_dbx10)
#end program