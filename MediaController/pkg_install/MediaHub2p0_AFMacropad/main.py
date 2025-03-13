#demos\MediaHub_AFMacropad: Media control hub your PC/MAC/phone/thing supporting keyboard media keys.
#-------------------------------------------------------------------------------
from CodeMap_MediaControls import CODEMAP, usenumpad
from HAL_Macropad import KEYPAD_ENCODER, KEYPAD_KEYCOUNT, EasyMPKey
from EasyCktIO.seesaw import EncoderSensorRIO
from adafruit_seesaw.seesaw import Seesaw
import SignalMap_KeyPad
import board


#=Platform/build-dependent config
#===============================================================================
I2CDID_VOLENC = 0x36 #I2C device ID for (volume) rotary encoder "seesaw" module


#=Configuration Options
#===============================================================================
#usenumpad(CODEMAP) #Map to numpad keycodes instead of standard ones.
#Filter encoder clicks to number of generated of Vol+/- messages:
def FilterVolClicks(delta): return delta*delta*1 #Square the value, and scale by 1
RGB_KEYDOWN = (50, 50, 50); RGB_KEYUP = (0, 0, 0)


#=Event handlers: Macropad key presses
#===============================================================================
class EasyMPKey_HID(EasyMPKey):
    """Translates macropad key events to HID keycodes"""
    def __init__(self, idx, keycode):
        super().__init__(idx)
        self.keycode = keycode
        self.pixel_set(RGB_KEYUP)

    def handle_press(self, id):
        self.pixel_set(RGB_KEYDOWN)
        self.keycode.press()
        #print("Press:", id) #DEBUG
    def handle_release(self, id):
        self.pixel_set(RGB_KEYUP)
        self.keycode.release()
        #print("Release:", id) #DEBUG


#=Event handlers: Macropad rotary encoder
#===============================================================================
KEYCODE_REW = CODEMAP["<<"]; KEYCODE_FF = CODEMAP[">>"] #Cached keycode
KEYCODE_VOLDN = CODEMAP["VOL-"]; KEYCODE_VOLUP = CODEMAP["VOL+"] #Cached keycode
def Handle_MPencoderChange(delta):
    keycode = KEYCODE_REW if delta < 0 else KEYCODE_FF
    NMSG = FilterVolClicks(delta) #Use same filtering function for now
    for i in range(NMSG):
        keycode.press()
    #Not sure if ok to release only once, but seems better behaved in Windows 10:
    keycode.release()
def Handle_VolEncoderChange(delta):
    keycode = KEYCODE_VOLDN if delta < 0 else KEYCODE_VOLUP
    NMSG = FilterVolClicks(delta)
    for i in range(NMSG):
        keycode.press()
    #Not sure if ok to release only once, but seems better behaved in Windows 10:
    keycode.release()


#==Global declarations
#===============================================================================
I2C = board.STEMMA_I2C() #Seems to be defined on Pico2
KEYCODE_MPKEY = tuple(CODEMAP[id] for id in SignalMap_KeyPad.SIGNALMAP_VEC) #Figure out what keycode to send for each key on keypad
KEYPAD_KEYS = tuple(EasyMPKey_HID(i, KEYCODE_MPKEY[i]) for i in range(KEYPAD_KEYCOUNT))
VOL_ENCODER = EncoderSensorRIO(Seesaw(I2C, I2CDID_VOLENC), 0)


#=Main loop
#===============================================================================
print("HELLO24") #DEBUG: Change me to ensure uploaded version matches.
print(f"MediaHub: ready to rock!")
while True:
    #Filter built-in rotary encoder knob into state control signals:
    delta = KEYPAD_ENCODER.read_delta() #Resets position to 0 every time.
    if delta != 0:
        Handle_MPencoderChange(delta) #Use for FF/REW
        #print("CHANGE:", delta) #DEBUG
    delta = VOL_ENCODER.read_delta() #Resets position to 0 every time.
    if delta != 0:
        Handle_VolEncoderChange(delta)
        #print("CHANGE:", delta) #DEBUG

    for key in KEYPAD_KEYS:
        key.process_inputs()
#end program