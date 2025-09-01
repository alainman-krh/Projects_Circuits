#CouchVolumeAV_pc\main.py
#-------------------------------------------------------------------------------
import IncludeProjLibs
from SerialGlue.Base import PortManager
from MyState.Predefined.PySerial import SigCom_PySerial


#==Configuration
#===============================================================================
#WARN: COM port varies every time plugged in!
portid_uctrl = "COM4" #Microcontroller sending volume signals
log_appid = "CouchVolumeAV_pc"


#==Debug/show available com ports:
#===============================================================================
SEP = "="*80
print("COM ports detected on system (Candidates for volume control device):")
print(SEP)
portmgr = PortManager()
portmgr.portlist_diplay()


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


#==Initialization
#===============================================================================
log_section(f"connecting to volume control...")
COM_VOLCTRL = serial_open(portmgr, portid_uctrl)

def RdNPrn():
	l = COM_VOLCTRL.io.readline_noblock()
	print("RD")
	print(l)

#=Main loop
#===============================================================================
while False:
#while True:
#for i in range(10):
	RdNPrn()
while True:
	COM_VOLCTRL.signalqueue_processio()
	if not COM_VOLCTRL.signalqueue_isempty():
		sig = COM_VOLCTRL.signalqueue_popnext()
		print(sig.serialize())
#end program