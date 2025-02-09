#demos\MediaHub_AFMacropad: Media control hub your PC/MAC/phone/thing supporting keyboard media keys.
#-------------------------------------------------------------------------------
from CodeMap_MediaButtons import CODEMAP, usenumpad, useskip_if_ffrew_only
from HAL_Macropad import KeypadElement, KEYPAD_ENCODER
from CelIRcom.TRx_pulseio import IRRx
from CelIRcom.ProtocolsBase import IRMsg32
import CelIRcom.Protocols_PDE as PDE
from CelIRcom.EasyIRRx import EasyRx
import SignalMap_LGremote, SignalMap_ADA389
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
SIGNAL_MAP = {}
SIGNAL_MAP.update(SignalMap_ADA389.SIGNALMAP_CCC)
SIGNAL_MAP.update(SignalMap_LGremote.SIGNALMAP_CCC)
if not SEND_CONSUMERCONTROL_ONLY:
    #You might prefer not handling "extras" (beyond consumer control codes).
    #Will act as if someone is typing in numbers, etc on the keyboard.
    SIGNAL_MAP.update(SignalMap_ADA389.SIGNALMAP_EXTRAS)
    SIGNAL_MAP.update(SignalMap_LGremote.SIGNALMAP_EXTRAS)


#=Event handlers
#===============================================================================
class IRDetect(EasyRx):
    def handle_press(self, msg:IRMsg32):
        sig = SIGNAL_MAP.get(msg.bits, None)
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
        sig = SIGNAL_MAP.get(msg.bits, None)
        if sig is None:
            return
        keycode = CODEMAP[sig] #A key that can be sent out through USB-HID interface
        keycode.release()

rx = IRRx(rx_pin)
irdetect = IRDetect(rx, PDE.DecoderNEC(), PDE.DecoderNECRPT(), msgRPT=PDE.IRMSG32_NECRPT)
#Use this one instead for Samsung remotes:
#irdetect = IRDetect(rx, PDE.DecoderSamsung()) #This remote doesn't have a special "repeat" command

from MyState.CtrlInputs.Buttons import Profiles, EasyButton, ButtonSensorIF


#=Convenient implementations of ::EasyButton
#===============================================================================
class EasyButton_SignalPressRel(EasyButton):
    """Emits signals on press/release only (don't want to make too many objects)"""
    def __init__(self, id, btnsense:ButtonSensorIF, profile=Profiles.DEFAULT):
        super().__init__(id, btnsense, profile=profile)
    def handle_press(self, id):
        pass
    def handle_release(self, id):
        pass

KEYCODE_VOLDN = CODEMAP["VOL-"]; KEYCODE_VOLUP = CODEMAP["VOL+"] #Cached
def Handle_MPencoderDelta(delta):
    keycode = KEYCODE_VOLDN if delta < 0 else KEYCODE_VOLUP
    NMSG = FilterVolClicks(delta)
    for i in range(NMSG):
        keycode.press()
        keycode.release()


#==Global declarations
#===============================================================================
KP_BUTTONS = [KeypadElement(idx=i) for i in range(12)]
KP_ENCKNOB = KEYPAD_ENCODER #Alias


#=Main loop
#===============================================================================
print("HELLO24") #DEBUG: Change me to ensure uploaded version matches.
print(f"MediaHub: ready to rock!")
while True:
    #Filter built-in rotary encoder knob into state control signals:
    delta = KP_ENCKNOB.read_delta() #Resets position to 0 every time.
    if delta != 0:
        Handle_MPencoderDelta(delta)
        print("CHANGE:", delta)

    #irdetect.process_events()
    pass
#end program