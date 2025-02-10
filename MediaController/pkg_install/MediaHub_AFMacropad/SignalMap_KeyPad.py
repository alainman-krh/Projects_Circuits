#SignalMap_Keypad.py: Maps keypad indicies => media control ID strings
#-------------------------------------------------------------------------------

#Defining map as a simple vector (since we store index):
SIGNALMAP_VEC = (
    "NAV_LEFT", "|<<", "MUTE",
    "NAV_DOWN", "NAV_UP", "PAUSE",
    "NAV_RIGHT", ">>|", "STOP",
    "SELECT", "PLAY", "EXIT", #TODO: Find code for "FIND"
)

#Last line