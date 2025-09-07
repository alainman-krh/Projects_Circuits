#SignalMap_ADA389.py: maps Adafruit #389 "Mini Remote Control" codes => media control signal IDs
#-------------------------------------------------------------------------------

SIGNALMAP_CCC = { #Base "Consumer Control Codes"
    0xFF629D: "PLAY", 0xFFC23D: "STOP",
    0xFFA25D: "VOL-", 0xFFE21D: "VOL+",
    0xFF22DD: "MUTE", #"setup" button (options: ESCAPE, KEYPAD_NUMLOCK, MUTE?)
}
SIGNALMAP_EXTRAS = { #Map onto normal keyboard keys (like up/down arrows, esc, ...)
    0xFF30CF: "1", 0xFF18E7: "2", 0xFF7A85: "3",
    0xFF10EF: "4", 0xFF38C7: "5", 0xFF5AA5: "6",
    0xFF42BD: "7", 0xFF4AB5: "8", 0xFF52AD: "9",
    0xFF6897: "0", 0xFFA857: "SELECT",
    0xFF02FD: "NAV_UP", 0xFF9867: "NAV_DOWN",
    0xFFE01F: "NAV_LEFT", 0xFF906F: "NAV_RIGHT",
    0xFFB04F: "EXIT", #"return"
}
