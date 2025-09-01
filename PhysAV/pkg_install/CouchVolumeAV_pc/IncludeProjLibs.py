#CouchVolumeAV_pc\IncludeProjLibs.py
#-------------------------------------------------------------------------------
from os.path import basename, dirname, abspath
from os.path import join as joinpath
import sys
_PATH_THIS_FILE = dirname(abspath(__file__))
_PATH_LIBROOT = abspath(joinpath(_PATH_THIS_FILE, "..", ".."))
print(_PATH_LIBROOT)

for libname in ["libpython"]:
    sys.path.insert(0, joinpath(_PATH_LIBROOT, libname))