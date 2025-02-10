#SignalMap_Keypad.py: Maps keypad indicies => media control ID strings
#-------------------------------------------------------------------------------

#Defining map as a simple vector (since we store index):
SIGNALMAP_VEC = (
    "NAV_LEFT", "|<<", "MUTE",
    "NAV_DOWN", "NAV_UP", "PAUSE",
    "NAV_RIGHT", ">>|", "STOP",
    "SELECT", "0", "EXIT",
    #TODO: Find code for "SEARCH". Using "0" right now. On YouTube, "0" moves to start of video.
)

#Last line