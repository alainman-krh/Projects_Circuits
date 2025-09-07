#demos\LightCtrl3Boards_2040pico\main.py
#-------------------------------------------------------------------------------
from StateDef import MYSTATE #Defines device state
#from MyState.SigTools import SignalListenerIF
from EasyCktIO.USBSerial import SigLink_USBHost
from EasyCktIO.UART import SigCom_UART
from MyState.Signals import SigEvent, SigUpdate
from StateReact import MainStateSync, SenseFilter
import board, busio
import os


#==Main configuration
#===============================================================================
#Common baud rates: 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600
BAUDRATE_MACROPAD = 115200 #Talking to macropad
TX_MACROPAD = board.GP12; RX_MACROPAD = board.GP13
BAUDRATE_LIGHTDISPLAY = 115200 #Talking to device that displays lights (not just macropad keys)
TX_LIGHTDISPLAY = board.GP20; RX_LIGHTDISPLAY = board.GP21
MAP_LIGHTINDEX = { #Mapping for {light index => id_light} (See: StateDef.STATEBLK_MAIN for id_light)
	0: "kitchen", 1: "livingroom", 2: "garage",
	3: "bedroom1", 4: "bedroom2", 5: "bedroom3",
	6: "hallway1", 7: "hallway2", 8: "hallway3",
	9: "basement", 10: "mechroom", 11: "mainentrance",
}
FILEPATH_CONFIG = "config_reset.state" #User can set initial state here (list of "SET" commands)
SIGBUFSZ_RX = 128 #Buffer size for recieving MyState "signals". Should be sufficient for a few signals without overflowing
USEOPT_ROTENCODERS = True #Disable if no NeoRotary 4 connected through I2C.


#==Global declarations
#===============================================================================
LINK_USBHOST = SigLink_USBHost(MYSTATE) #Direct link to state.
UART_MACROPAD = busio.UART(TX_MACROPAD, RX_MACROPAD, baudrate=BAUDRATE_MACROPAD, receiver_buffer_size=SIGBUFSZ_RX) #Talking to MacroPad
COM_MACROPAD = SigCom_UART(UART_MACROPAD) #No direct link to state. Manually process messages.
UART_LIGHTDISPLAY = busio.UART(TX_LIGHTDISPLAY, RX_LIGHTDISPLAY, baudrate=BAUDRATE_LIGHTDISPLAY, receiver_buffer_size=SIGBUFSZ_RX) #Talking to light display unit
COM_LIGHTDISPLAY = SigCom_UART(UART_LIGHTDISPLAY) #No direct link to state. Manually process messages.

STATE_SYNC = MainStateSync(MAP_LIGHTINDEX, [COM_MACROPAD, COM_LIGHTDISPLAY]) #Keep MacroPad + Circuit Playground displays in sync with state
SENSE_FILT = SenseFilter(STATE_SYNC.roomcache_map)
if USEOPT_ROTENCODERS:
	from Opt_RotEncoder import ENCODERS_I2C
	print("ENCODERS DETECTED")


#==Configuration before main loop
#===============================================================================
COM_LIGHTDISPLAY.io.write("\n") #Not sure why... but seems to be needed to not miss first message
COM_MACROPAD.io.write("\n") #Not sure why... but seems to be needed to not miss first message
SENSE_FILT.lights_setactive(0) #Knobs will control this light/area @ startup

if FILEPATH_CONFIG in os.listdir("/"):
	print("Loading user defaults...", end="")
	MYSTATE.script_load(FILEPATH_CONFIG)
	print("Done.")


#==Main loop
#===============================================================================
print("HELLO-mainboard (LightCtrl3Boards)") #DEBUG: Change me to ensure uploaded version matches.
while True:
	LINK_USBHOST.process_signals() #Host might send signals through USB serial

	#In case display controller (Circuit Playground) itself requests an update:
	COM_LIGHTDISPLAY.signalqueue_processio()
	while not COM_LIGHTDISPLAY.signalqueue_isempty(): #Process all available signals (shouldn't be too many)
		sig = COM_LIGHTDISPLAY.signalqueue_popnext() #Low event count... don't need to loop
		if SigUpdate == type(sig):
			STATE_SYNC.handle_update(None) #Entire state will get sync'd
			#TODO: Should we instead use: MYSTATE.process_signal(sig)???

	#Process signals from MacroPad:
	COM_MACROPAD.signalqueue_processio()
	while not COM_MACROPAD.signalqueue_isempty(): #Process all available signals (shouldn't be too many)
		sig = COM_MACROPAD.signalqueue_popnext() #Low event count... don't need to loop
		if SigEvent == type(sig):
			#print(sig.serialize())
			from_macropad = ("MP" == sig.section)
			iskeypress = from_macropad and ("BTNPRESS" == sig.id)
			isencdelta = from_macropad and ("ENCCHANGE" == sig.id)
			if iskeypress:
				light_idx = sig.val
				SENSE_FILT.filter_keypress(light_idx)
			elif isencdelta:
				SENSE_FILT.filter_MPencoder(sig.val)
			else:
				print("Unexpected `SigEvent` from Macropad.")
		elif SigUpdate == type(sig):
			STATE_SYNC.handle_update(None) #Entire state will get sync'd
		elif sig != None:
			print("Unexpected signal from Macropad.")

	#Filter external I2C encoder knobs (NeoRotary 4) - mostly to control RGB:
	if USEOPT_ROTENCODERS:
		for (i, enc) in enumerate(ENCODERS_I2C):
			delta = enc.read_delta() #Relative to last time read.
			if delta != 0:
				#print(f"ENC{i}, delta:{delta}")
				SENSE_FILT.filter_I2Cencoder(i, delta)

#Last line