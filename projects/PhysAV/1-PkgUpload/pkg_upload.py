#pkg_upload.py: Upload project code to CircuitPython board
#-------------------------------------------------------------------------------
from ZIncludeRuntoolsPyLib import PKGINSTALLER

#User config
#-------------------------------------------------------------------------------
DEST_DRIVE = "E:\\"
#Update/activate to automatically install from Circuit Python library "bundle":
#os.environ["LIBPATH_CPYBUNDLE"] = r"C:\path\to\adafruit-circuitpython-bundle-9.x-mpy\lib"

#Choose package to upload:
pkg = "CouchVolumeAV_2040pico"

#Upload package defined in `..\$pkg\pydrv_install.toml`:
PKGINSTALLER.upload(pkg, DEST_DRIVE, refresh_libs=True)
r"""NOTE:
- `refresh_libs=True` uploads dependencies from `[modules]` section of pydrv_install.toml.
  (Change significantly less during project code development)
"""

#Last line