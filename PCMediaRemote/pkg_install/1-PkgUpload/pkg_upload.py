#pkg_upload.py: Upload project code to CircuitPython board
#-------------------------------------------------------------------------------
from UploadTools import UploadProj
from os.path import join as joinpath

#User config
#-------------------------------------------------------------------------------
DEST_DRIVE = "E:\\"
proj = "MediaRemote_RP2040"

proj = joinpath("pkg_install", proj)
UploadProj(proj, DEST_DRIVE, refresh_libs=True)

#Last line