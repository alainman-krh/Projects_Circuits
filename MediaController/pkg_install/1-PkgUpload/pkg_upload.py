#pkg_upload.py: Upload project code to CircuitPython board
#-------------------------------------------------------------------------------
from UploadTools import UploadPkg
from os.path import join as joinpath
import os

#User config
#-------------------------------------------------------------------------------
DEST_DRIVE = "E:\\"
#Update/activate to automatically install from Circuit Python library "bundle":
#os.environ["LIBPATH_CPYBUNDLE"] = r"C:\path\to\adafruit-circuitpython-bundle-9.x-mpy\lib"


#pkg = "MediaHub_AFMacropad"
#pkg = "MediaHub2p0_AFMacropad"
pkg = "MediaHub2p0_KB2040"
UploadPkg(pkg, DEST_DRIVE, refresh_libs=True)

#Last line