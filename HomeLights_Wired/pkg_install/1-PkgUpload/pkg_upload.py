#pkg_upload.py: Upload project code to CircuitPython board
#-------------------------------------------------------------------------------
from UploadTools import UploadPkg
from os.path import join as joinpath

#User config
#-------------------------------------------------------------------------------
DEST_DRIVE = "E:\\"
pkg = "LightCtrl3Boards_2040pico"
#pkg = "LightCtrl3Boards_AFMacropad"
#pkg = "LightCtrl3Boards_CPbluefruit"

UploadPkg(pkg, DEST_DRIVE, refresh_libs=True)

#Last line