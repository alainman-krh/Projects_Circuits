#demos\MediaHub2p0_KB2040: Media remote receiver add-on (optional) for MediaHub 2.0.
#-------------------------------------------------------------------------------
from CodeMap_MediaControls import CODEMAP, usenumpad, useskip_if_ffrew_only
import SignalMap_LGremote, SignalMap_ADA389
from CelIRcom.TRx_pulseio import IRRx
from CelIRcom.ProtocolsBase import IRMsg32
import CelIRcom.Protocols_PDE as PDE
from CelIRcom.EasyIRRx import EasyRx
import board


#=Platform/build-dependent config
#===============================================================================
rx_pin = board.A3 #KB2040 "Kee Boar" variant/build using pin near supply/ground leads


#=Configuration Options
#===============================================================================
USEOPT_MOUSECLICK = True #Use optional mouse click
SEND_CONSUMERCONTROL_ONLY = False #Support basic media keys only
#NOTE: You might prefer not handling "extras" (beyond consumer control codes).
#      ==> Will act as if someone is typing in numbers, etc on the keyboard.
#usenumpad(CODEMAP) #Map to numpad keycodes instead of standard ones.
useskip_if_ffrew_only(CODEMAP) #Re-define meaning of "<<-only" & ">>-only" "buttons".

if USEOPT_MOUSECLICK:
	from Opt_MouseClick import handle_mouseclick
	print("Mouse click option enabled")


#=Map IR remote signals to "media buttons" (dict-keys) defined in CODEMAP
#===============================================================================
#Respond to both remotes (Watch out for overlapping IR codes.)
SIGNALMAP_IR = {}
SIGNALMAP_IR.update(SignalMap_ADA389.SIGNALMAP_CCC)
SIGNALMAP_IR.update(SignalMap_LGremote.SIGNALMAP_CCC)
if not SEND_CONSUMERCONTROL_ONLY:
    #You might prefer not handling "extras" (beyond consumer control codes).
    #Will act as if someone is typing in numbers, etc on the keyboard.
    SIGNALMAP_IR.update(SignalMap_ADA389.SIGNALMAP_EXTRAS)
    SIGNALMAP_IR.update(SignalMap_LGremote.SIGNALMAP_EXTRAS)


#=Event handlers: IR receiver
#===============================================================================
class IRDetect(EasyRx):
    def handle_press(self, msg:IRMsg32):
        sig = SIGNALMAP_IR.get(msg.bits, None)
        IRcodestr = msg.str_hex()
        if sig is None:
            if USEOPT_MOUSECLICK:
                handled = handle_mouseclick(msg)
                if handled:
                    sig = "Mouse click"
                    #print(f"New message: {IRcodestr} ({sig})")
                    return #Special button handled. Don't continue
            #print("Unknown message:", IRcodestr) #DEBUG
            return
        #print(f"New message: {IRcodestr} ({sig})") #DEBUG
        keycode = CODEMAP[sig] #A key that can be sent out through USB-HID interface
        keycode.press()

    def handle_hold(self, msg:IRMsg32):
        #print(f"Repeat!") #Doesn't matter what msg is - USB-HID key still held down.
        pass

    def handle_release(self, msg:IRMsg32):
        sig = SIGNALMAP_IR.get(msg.bits, None)
        if sig is None:
            return
        keycode = CODEMAP[sig] #A key that can be sent out through USB-HID interface
        keycode.release()


#==Global declarations
#===============================================================================
rx = IRRx(rx_pin)
irdetect = IRDetect(rx, PDE.DecoderNEC(), PDE.DecoderNECRPT(), msgRPT=PDE.IRMSG32_NECRPT)
#For Samsung remotes, use the following:
#irdetect = IRDetect(rx, PDE.DecoderSamsung()) #This remote doesn't have a special "repeat" command


#=Main loop
#===============================================================================
print("HELLO24") #DEBUG: Change me to ensure uploaded version matches.
print(f"MediaHub: ready to rock!")
while True:
    irdetect.process_events()
#end program