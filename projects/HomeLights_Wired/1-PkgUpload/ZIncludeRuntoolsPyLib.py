# ZIncludeRuntoolsPyLib.py: Import "runtools" library
#-------------------------------------------------------------------------------
from os.path import basename, dirname, abspath
from os.path import join as joinpath
import sys
_PATH_THIS_FILE = dirname(abspath(__file__))
_PATH_REPOROOT = abspath(joinpath(_PATH_THIS_FILE, *([".."]*3)))
_PATH_PKGROOT = abspath(joinpath(_PATH_THIS_FILE, *([".."]*1)))
sys.path.insert(0, joinpath(_PATH_REPOROOT, "runtools", "libpython"))

import UploadTools
#UploadTools.DEBUG_ONLY = True
PKGINSTALLER = UploadTools.PkgInstaller(_PATH_REPOROOT, _PATH_PKGROOT)
#Last line