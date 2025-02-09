#KeyMap_MediaButtons.py: maps media buttons (ex: IR remote) => media keycodes
#-------------------------------------------------------------------------------
from EasyCktIO.USBHID_Keyboard import KeysMain, KeysCC, Keycode, CCC


#=Resources for Keycode/CCC (aliases for Keycode/ConsumerControlCode)
#===============================================================================
#https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode
#https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit_hid.consumer_control_code.ConsumerControlCode


#=Base keymap (Maps the function of a button to corresponding keyboard keys)
#===============================================================================
KEYMAP = {
    "PLAY": KeysCC(CCC.PLAY_PAUSE)        , "PAUSE": KeysCC(CCC.PLAY_PAUSE),
    "STOP": KeysCC(CCC.STOP)              , "EJECT": KeysCC(CCC.EJECT),
    "<<" : KeysCC(CCC.REWIND)             , ">>" :   KeysCC(CCC.FAST_FORWARD),
    "|<<": KeysCC(CCC.SCAN_PREVIOUS_TRACK), ">>|":   KeysCC(CCC.SCAN_NEXT_TRACK),
    "VOL-": KeysCC(CCC.VOLUME_DECREMENT)  , "VOL+":  KeysCC(CCC.VOLUME_INCREMENT),
    "MUTE": KeysCC(CCC.MUTE),

    "1": KeysMain(Keycode.ONE),   "2": KeysMain(Keycode.TWO),   "3": KeysMain(Keycode.THREE),
    "4": KeysMain(Keycode.FOUR),  "5": KeysMain(Keycode.FIVE),  "6": KeysMain(Keycode.SIX),
    "7": KeysMain(Keycode.SEVEN), "8": KeysMain(Keycode.EIGHT), "9": KeysMain(Keycode.NINE),
    "0": KeysMain(Keycode.ZERO) , "SELECT": KeysMain(Keycode.ENTER),

    "NAV_UP":   KeysMain(Keycode.UP_ARROW)  , "NAV_DOWN":  KeysMain(Keycode.DOWN_ARROW),
    "NAV_LEFT": KeysMain(Keycode.LEFT_ARROW), "NAV_RIGHT": KeysMain(Keycode.RIGHT_ARROW),
    "BACK":     KeysMain(Keycode.BACKSPACE) , "EXIT":      KeysMain(Keycode.ESCAPE),
}


#=Options: Numeric input (+enter/select/ok)
#===============================================================================
KEYMAP_NUMPAD = {
    "1": KeysMain(Keycode.KEYPAD_ONE),   "2": KeysMain(Keycode.KEYPAD_TWO),   "3": KeysMain(Keycode.KEYPAD_THREE),
    "4": KeysMain(Keycode.KEYPAD_FOUR),  "5": KeysMain(Keycode.KEYPAD_FIVE),  "6": KeysMain(Keycode.KEYPAD_SIX),
    "7": KeysMain(Keycode.KEYPAD_SEVEN), "8": KeysMain(Keycode.KEYPAD_EIGHT), "9": KeysMain(Keycode.KEYPAD_NINE),
    "0": KeysMain(Keycode.KEYPAD_ZERO) , "SELECT": KeysMain(Keycode.KEYPAD_ENTER),
}

def usenumpad(keymap:dict):
    """Option: Map to numpad keycodes instead of standard ones"""
    keymap.update(KEYMAP_NUMPAD) #Overwrite with numpad keycodes


#=Options: Special "buttons"
#===============================================================================
#For remotes/controls that ONLY support FF/REW (missing next/previous track):
KEYMAP["<<-only"] = KEYMAP["<<"]; KEYMAP[">>-only"] = KEYMAP[">>"] #Keep FF/REW behaviour

def useskip_if_ffrew_only(keymap:dict):
    """Option: re-define meaning of "<<-only" & ">>-only" "buttons"."""
    keymap["<<-only"] = keymap["|<<"]; keymap[">>-only"] = keymap[">>|"]

#Last line