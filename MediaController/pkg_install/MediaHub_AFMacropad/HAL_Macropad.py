#demos\LightCtrl3Boards_AFMacropad\HAL_Macropad.py: Hardware Abstraction Layer
#-------------------------------------------------------------------------------
from MyState.CtrlInputs.Buttons import EasyButton, Profiles
from EasyCktIO.digitalio import ButtonSensorDIO
from EasyCktIO.rotaryio import EncoderSensorRIO
from neopixel import NeoPixel
import digitalio
import board
r"""HAL layer helping to reduce complexity of interfacing with Adafruit Macropad"""


#==Constants
#===============================================================================
KEYPAD_SENSEPIN_LIST = ( #Pin references only. Does not directly measure input state:
	board.KEY1, board.KEY2, board.KEY3, board.KEY4, board.KEY5, board.KEY6,
	board.KEY7, board.KEY8, board.KEY9, board.KEY10, board.KEY11, board.KEY12,
)
KEYPAD_KEYCOUNT = len(KEYPAD_SENSEPIN_LIST)
KEYPAD_NPX = NeoPixel(board.NEOPIXEL, KEYPAD_KEYCOUNT) #One object. Indexable per key.
KEYPAD_ENCODER = EncoderSensorRIO(board.ENCODER_A, board.ENCODER_B)


#=EasyMPKey
#===============================================================================
class EasyMPKey(EasyButton):
	def __init__(self, idx, profile=Profiles.DEFAULT):
		pin = KEYPAD_SENSEPIN_LIST[idx]
		btnsense = ButtonSensorDIO(pin, pull=digitalio.Pull.UP, active_low=True)
		super().__init__(idx, btnsense=btnsense, profile=profile) #Stores self.id=idx
	def pixel_set(self, value):
		"""Must be a tuple(R,G,B)"""
		idx = self.id
		KEYPAD_NPX[idx] = value

