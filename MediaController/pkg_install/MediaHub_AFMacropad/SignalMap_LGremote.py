#SignalMap_LGremote.py: maps LG IR remote codes => media buttons
#-------------------------------------------------------------------------------

SIGNALMAP_CCC = { #Base "Consumer Control Codes"
    0x20DF0DF2: "PLAY", 0x20DF5DA2: "PAUSE", 0x20DF8D72: "STOP",
    0x20DFF10E: "<<-only", 0x20DF718E: ">>-only",
    0x20DFC03F: "VOL-", 0x20DF40BF: "VOL+",
    0x20DF906F: "MUTE",
}

SIGNALMAP_EXTRAS = { #Map onto normal keyboard keys (like up/down arrows, esc, ...)
    0x20DF8877: "1", 0x20DF48B7: "2", 0x20DFC837: "3",
    0x20DF28D7: "4", 0x20DFA857: "5", 0x20DF6897: "6",
    0x20DFE817: "7", 0x20DF18E7: "8", 0x20DF9867: "9",
    0x20DF08F7: "0", 0x20DF22DD: "SELECT",
    0x20DF02FD: "NAV_UP", 0x20DF827D: "NAV_DOWN",
    0x20DFE01F: "NAV_LEFT", 0x20DF609F: "NAV_RIGHT",
    0x20DF14EB: "BACK", 0x20DFDA25: "EXIT",
}
