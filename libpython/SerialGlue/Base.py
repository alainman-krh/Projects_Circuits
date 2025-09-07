#SerialGlue/Base.py
#-------------------------------------------------------------------------------
import os
from copy import copy

if os.name == 'nt':  # sys.platform == 'win32':
	from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
	from serial.tools.list_ports_posix import comports
else:
	raise ImportError("OS not supported: {os.name}.")


#==PortManager
#===============================================================================
class PortManager:
	def __init__(self) -> None:
		self.port_list = [] #List of port_info=(port, desc, hwid)
	
	def portlist_refresh(self):
		#Copy port_info - just in case iterator doesn't return copies itself
		iterator = sorted(comports())
		self.port_list = tuple(copy(pinfo) for pinfo in iterator)

	def portlist_diplay(self, refresh=True):
		if refresh:
			self.portlist_refresh()
		for pinfo in self.port_list:
			print(f"{pinfo.name}")
			print(f"    desc: {pinfo.description}")
			print(f"    hwid: {pinfo.hwid}")

	def serialno_get(self, portid):
		for pinfo_i in self.port_list:
			if pinfo_i.name == portid:
				return pinfo_i.serial_number
		return None

	def portid_fromserialno(self, sn):
		sn = sn.lower()
		for pinfo_i in self.port_list:
			sn_i:str = pinfo_i.serial_number
			if sn_i.lower() == sn:
				return pinfo_i.name
		return None


#==Quick test
#===============================================================================
def _testcode():
	sn = "SOMESERIALNO"
	mgr = PortManager()
	mgr.portlist_diplay()
	portid = mgr.portid_fromserialno(sn)
	print(portid)

if __name__ == '__main__':
    _testcode()
#Last line