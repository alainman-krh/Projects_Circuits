#pkg_upload.py: Upload project code to CircuitPython board
#-------------------------------------------------------------------------------
from UploadTools import UploadPkg
from os.path import join as joinpath

#User config
#-------------------------------------------------------------------------------
DEST_DRIVE = "E:\\"
pkg = "MediaRemote_RP2040"

UploadPkg(pkg, DEST_DRIVE, refresh_libs=True)

#Last line