#CouchVolumeAV_pc\main.py: Relay volume messages using "YNCA" protocol
#-------------------------------------------------------------------------------
import IncludeProjLibs
from SerialGlue.Base import PortManager
from MyState.Predefined.PySerial import SigCom_PySerial
from MyState.SigTools import SignalAwareStateIF, Signal_Deserialize
import socket
import os

r"""Background
## SOURCE: AI search (can't find official docs - so relying on this)
- YNCA: Yamaha Network Control Architecture
  - YNCA => older serial and network ASCII command protocol using simple messages.
  - Can be sent over TCP connections as well as RS232
- YXC/YEC: Yamaha Extended Control Protocol (sometimes called Yamaha Network Control Protocol)
  - YXC/YEC => newer RESTful HTTP API control protocol used on recent Yamaha MusicCast and AV devices.
"""


#==Configuration
#===============================================================================
HOST = '192.168.1.10'
PORT = 50000 #Think this is standard port for 
portid_uctrl = None #COM/tty port of microcontroller sending volume signals
#WARN: COM/tty port potentially varies every time plugged in!
if os.name == 'nt':  # sys.platform == 'win32':
	portid_uctrl = "COM4"
elif os.name == 'posix': #Linux
	portid_uctrl = "/dev/ttyACM0"
else:
	raise ImportError("OS not supported: {os.name}.")
log_appid = "CouchVolumeAV_pc"


#==Debug/show available com ports:
#===============================================================================
DEBUGONLY = True
SEP = "="*80
print("COM ports detected on system (Candidates for volume control device):")
print(SEP)
portmgr = PortManager()
portmgr.portlist_diplay() #Show available ports to user


#==Helper functions
#===============================================================================
def log_section(id):
	print(f"\n{log_appid}: ", end=""); print(id); print(SEP)
def serial_open(portmgr:PortManager, portid):
	#TODO: find a way to get serial number from open com port instead.
	portmgr.portlist_refresh()
	ctrlserialno = portmgr.serialno_get(portid)
	com = SigCom_PySerial(portid)
	print(f"Using SN={ctrlserialno} on {portid}")
	return com
def volmain_buildmsg(voldb):
	if voldb < -80:
		return "@MAIN:MUTE=On\r\n"
	return f"@MAIN:VOL={voldb:0.1f}\r\n"    

#==Initialization
#===============================================================================
log_section(f"connecting to volume control...")
COM_VOLCTRL = serial_open(portmgr, portid_uctrl)
SOCK_RX = None #Initialize
if not DEBUGONLY: SOCK_RX = socket.create_connection((HOST, PORT), timeout=1)
siglist = []


#=Main loop
#===============================================================================
while True:
	msgstr = COM_VOLCTRL.io.com.readline().decode("utf-8")
	siglist.extend(Signal_Deserialize(msgstr.strip()))
	while len(siglist)>0:
		sig = siglist.pop(0)
		print(sig.serialize())
		msg = volmain_buildmsg(sig.val/10)
		if DEBUGONLY:
			print(msg)
		else:
			SOCK_RX.sendall(msg.encode())
#end program