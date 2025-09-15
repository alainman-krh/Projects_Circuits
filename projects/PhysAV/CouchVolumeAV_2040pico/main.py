#CouchVolumeAV_2040pico\main.py
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.Timebase import now_ms, ms_elapsed
from filter_sense import FilterNoisy_Int, FilterRescale, CPY_ADC_NBITS
from analogio import AnalogIn
from time import sleep
import board

DEBUGONLY = False


#=Platform/build-dependent config (RP2040-Pico)
#===============================================================================
#ADC-sensor: RP2040-Pico built-in
volmainp_pin = board.GP28
volmainn_pin = board.GP27
#Potentiometer: Behringer Monitor 1 - Sharply drops in bottom 20% or ADC range:
VOLMAIN_NORMRANGE = (0.2, 0.99) #ADC sense limits normalized between (0, 1).


#=Configuration Options (Yamaha RXV-475)
#===============================================================================
SENSEMAP_NBITS = 9 #Downsample sensed value to reduce size of mapping table
MSGBASE_VOLMAIN = "SIG CTRL:MAINVOL " #Append: Volume in 0.5dB increments (-80dB...10dB?)
#Can go downto -80dB... but limit to -40 due to log potentiometer range issue:
VOLMAIN_DBRANGE = (-40, -10) #Safety: Don't let knob go beyond -10. Use remote/RXV if needed
VOLMAIN_MUTE = -90 #Indicates mute is desired (avoids separate signal)
#Averaging filter length used to suppress volume changes due to measurement noise:
NOISEFILT_NBITS_AVGLEN = 3 #32 samples. NOTE: keep <16bit to avoid overflow/use of largeint????
NOISEFILT_NSTOPS_NOAVG = 4 #How many stops of noise do we have to filter?
NOISEFILT_NSTOPS_NOISEFLOOR = 1 #How many stops does the average have to change before registering?
TUPDATE_MS = 100 #ms: Maximum update rate


#==VolumeState object
#===============================================================================
class VolumeState:
	def __init__(self, Tupdate_ms):
		self.ismute = True
		self.stopidx = 0 #Current "stop" index (volume level)
		self.lastupdate_ms = now_ms()
		self.canupdate = True #Don't just rely on lastupdate_ms (avoid logic error after roll-over)
		self.Tupdate_ms = Tupdate_ms

	def tryupdate(self, ismute_new, stopidx_new):
		"""Don't update unless changed"""
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
#VAL_MUTE = -float('inf')
VAL_MUTE = round(10*VOLMAIN_MUTE)
VOLMAIN_STOP_PER_DB = 2 #2 stops per dB (0.5dB steps)
SENSEREDUCE_NBITS = CPY_ADC_NBITS-SENSEMAP_NBITS #Down-res for efficiency
SENSEMAP_MAXVAL = (1<<SENSEMAP_NBITS)-1
SENSEMAP_VALIDMIN = round(min(VOLMAIN_NORMRANGE)*SENSEMAP_MAXVAL)
SENSEMAP_VALIDMAX = round(max(VOLMAIN_NORMRANGE)*SENSEMAP_MAXVAL)
(VOLMAIN_DBMIN, VOLMAIN_DBMAX) = VOLMAIN_DBRANGE #unpack (convenience)
VOLMAIN_NSTOPS = (VOLMAIN_DBMAX - VOLMAIN_DBMIN)*VOLMAIN_STOP_PER_DB #Actually # of stops -1... or last index
SENSEIN_PER_STOP = (SENSEMAP_VALIDMAX-SENSEMAP_VALIDMIN) / VOLMAIN_NSTOPS

#Senses differential volume potentiometer:
volmainp = AnalogIn(volmainp_pin)
volmainn = AnalogIn(volmainn_pin)
volmain_state = VolumeState(TUPDATE_MS) #Main volume state
volmain_rescale = FilterRescale( #Build with output as "stop number"
	out_range=(0, VOLMAIN_NSTOPS),
	in_range=(SENSEMAP_VALIDMIN, SENSEMAP_VALIDMAX),
	under=VAL_MUTE, over=max(VOLMAIN_DBRANGE)*10,
)
fmap = volmain_rescale.fmap
for i in range(len(fmap)): #Re-compute map to get desired 0.5dB increments (x10):
	fmap[i] = min(VOLMAIN_DBRANGE)*10 + fmap[i]*(10//2)
#print(fmap) #Debug
volmain_denoise = FilterNoisy_Int(NOISEFILT_NBITS_AVGLEN, #Filter ADC/resistor noise
#NOTE:Filtering seem even better with 100uF caps on sense terminals!!
	thresh_avg=NOISEFILT_NSTOPS_NOAVG*SENSEIN_PER_STOP,
	thresh_noise=NOISEFILT_NSTOPS_NOISEFLOOR*SENSEIN_PER_STOP
)
#print(f"thresh_avg: {volmain_denoise.thresh_avg}, thresh_noise: {volmain_denoise.thresh_noise}")
#raise Exception("STOP")


#=Main loop
#===============================================================================
print("HELLO24") #DEBUG: Change me to ensure uploaded version matches.
print(f"CouchVolumeAV: ready to rock!")
#COM_VOLCTRL.io.write("\n") #Not sure why... but seems to be needed to not miss first message
while True:
	#Read raw ADC values:
	volmain_read = (volmainp.value - volmainn.value)>>SENSEREDUCE_NBITS
	volmain_read = volmain_denoise.getfiltered(volmain_read)
	#Convert to dBs:
	volmain_dB = volmain_rescale.getfiltered(volmain_read)

	#Convert to "stop index":
	ismute_now = (volmain_dB == VAL_MUTE)

	changed = volmain_state.tryupdate(ismute_now, volmain_dB)
	if not changed:
		pass
	else:
		if DEBUGONLY and volmain_state.ismute:
			print("MUTED!")
		print(MSGBASE_VOLMAIN, end="")
		print(volmain_dB)
#end program