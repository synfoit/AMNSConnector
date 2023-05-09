# import cx_Freeze
# import sys
# from cx_Freeze import setup, Executable
# import os
# base = None
#
#
# build_exe_options = {"packages": ["os"]}
# if sys.platform == 'win32':
#     base = "Win32GUI"
#
#
#
# setup(
#     name = "AMNSConnector",
#     version = "0.1",
#     description = "An AMNS Connector script",
#     options = {"build_exe":build_exe_options},
#     executables = [Executable("main.py")]
#     )


# coding: cp1252
import sys
import os

import cx_Freeze
from cx_Freeze import setup, Executable
base = None

os.environ['TCL_LIBRARY']=r'C:\Python310\tcl\tcl8.6'

os.environ['TK_LIBRARY']=r'C:/Python310/tcl/tk8.6'

if sys.platform=='win32':
    base='Win32GUI'

executables= [cx_Freeze.Executable("main.py",base=base)]
# build_exe_options = {"packages": ["os"]}
# if sys.platform == 'win32':
#     base = "Win32GUI"



setup(
    name="RPL",
    version="0.1",
    description="An example wxPython script",
    options={"build_exe": {"packages":["snap7","threading","time","datetime","json","os","opcua","numpy"]}},
    executables=executables
    )