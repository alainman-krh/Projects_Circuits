#demos\MediaHub_AFMacropad: Media control hub your PC/MAC/phone/thing supporting keyboard media keys.
#-------------------------------------------------------------------------------
from CodeMap_MediaControls import CODEMAP, usenumpad, useskip_if_ffrew_only
from HAL_Macropad import KEYPAD_ENCODER, KEYPAD_KEYCOUNT, EasyMPKey
import SignalMap_LGremote, SignalMap_ADA389, SignalMap_KeyPad

from CelIRcom.TRx_pulseio import IRRx
from CelIRcom.ProtocolsBase import IRMsg32
import CelIRcom.Protocols_PDE as PDE
from CelIRcom.EasyIRRx import EasyRx
import board


#=Platform/build-dependent config
#===============================================================================
#Choose pin used for receiving IR signals (depends on platform/variant):
rx_pin = board.SDA #Only available pin: BUILT-IN STEMMA-QT port


#=Configuration Options
#===============================================================================
SEND_CONSUMERCONTROL_ONLY = False #Support basic media keys only
#NOTE: You might prefer not handling "extras" (beyond consumer control codes).
#      ==> Will act as if someone is typing in numbers, etc on the keyboard.
#usenumpad(CODEMAP) #Map to numpad keycodes instead of standard ones.
useskip_if_ffrew_only(CODEMAP) #Re-define meaning of "<<-only" & ">>-only" "buttons".
#Filter encoder clicks to number of generated of Vol+/- messages:
def FilterVolClicks(delta): return delta*delta*1 #Square the value, and scale by 1


#=Map IR remote signals to "media buttons" (dict-keys) defined in CODEMAP
#===============================================================================
#Respond to both remotes (Watch out for overlapping IR codes.)
CTRLMAP_IR = {}
CTRLMAP_IR.update(SignalMap_ADA389.SIGNALMAP_CCC)
CTRLMAP_IR.update(SignalMap_LGremote.SIGNALMAP_CCC)
if not SEND_CONSUMERCONTROL_ONLY:
    #You might prefer not handling "extras" (beyond consumer control codes).
    #Will act as if someone is typing in numbers, etc on the keyboard.
    CTRLMAP_IR.update(SignalMap_ADA389.SIGNALMAP_EXTRAS)
    CTRLMAP_IR.update(SignalMap_LGremote.SIGNALMAP_EXTRAS)


#=Event handlers: IR receiver
#===============================================================================
class IRDetect(EasyRx):
    def handle_press(self, msg:IRMsg32):
        sig = CTRLMAP_IR.get(msg.bits, None)
        IRcodestr = msg.str_hex()
        if sig is None:
#            if USEOPT_MOUSECLICK:
#                handled = handle_mouseclick(msg)
#                if handled:
#                    sig = "Mouse click"
#                    print(f"New message: {IRcodestr} ({sig})")
#                    return #Special button handled. Don't continue
            print("Unknown message:", IRcodestr)
            return
        print(f"New message: {IRcodestr} ({sig})")
        keycode = CODEMAP[sig] #A key that can be sent out through USB-HID interface
        keycode.press()

    def handle_hold(self, msg:IRMsg32):
        print(f"Repeat!") #Doesn't matter what msg is - USB-HID key still held down.

    def handle_release(self, msg:IRMsg32):
        sig = CTRLMAP_IR.get(msg.bits, None)
        if sig is None:
            return
        keycode = CODEMAP[sig] #A key that can be sent out through USB-HID interface
        keycode.release()


#=Event handlers: Macropad key presses
#===============================================================================
KEYCODE_MPKEY = tuple(CODEMAP[id] for id in SignalMap_KeyPad.SIGNALMAP_VEC) #Cached
class EasyMPKey_HID(EasyMPKey):
    """Translates macropad key events to HID keycodes"""
    def handle_press(self, id):
        keycode = KEYCODE_MPKEY[id]
        keycode.press()
        #print("Press:", id) #DEBUG
    def handle_release(self, id):
        keycode = KEYCODE_MPKEY[id]
        keycode.release()
        #print("Release:", id) #DEBUG


#=Event handlers: Macropad rotary encoder
#===============================================================================
KEYCODE_VOLDN = CODEMAP["VOL-"]; KEYCODE_VOLUP = CODEMAP["VOL+"] #Cached
def Handle_MPencoderDelta(delta):
    keycode = KEYCODE_VOLDN if delta < 0 else KEYCODE_VOLUP
    NMSG = FilterVolClicks(delta)
    for i in range(NMSG):
        keycode.press()
    #Not sure if ok to release only once, but seems better behaved in Windows 10:
    keycode.release()


#==Global declarations
#===============================================================================
rx = IRRx(rx_pin)
irdetect = IRDetect(rx, PDE.DecoderNEC(), PDE.DecoderNECRPT(), msgRPT=PDE.IRMSG32_NECRPT)
#For Samsung remotes, use the following:
#irdetect = IRDetect(rx, PDE.DecoderSamsung()) #This remote doesn't have a special "repeat" command
KEYPAD_KEYS = tuple(EasyMPKey_HID(idx=i) for i in range(KEYPAD_KEYCOUNT))


#=Main loop
#===============================================================================
print("HELLO24") #DEBUG: Change me to ensure uploaded version matches.
print(f"MediaHub: ready to rock!")
while True:
    #Filter built-in rotary encoder knob into state control signals:
    delta = KEYPAD_ENCODER.read_delta() #Resets position to 0 every time.
    if delta != 0:
        Handle_MPencoderDelta(delta)
        #print("CHANGE:", delta) #DEBUG

    for key in KEYPAD_KEYS:
        key.process_inputs()
#end program