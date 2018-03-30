# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 00:35:49 2018

@author: criow
"""

SOURCE_FILES=[
        #Python Files
        'SaveNLoad.py',
        'keypress.py',
        'globalVariables.py',
        'setup.py',
        'compile.py',
        #Powershell Files
        'test.ps1']

AUXILARY_FILES=[
        'test.ps1']

import subprocess
import shutil
import os
from globalVariables import SCRIPT_PATH



subprocess.call(['python','setup.py','py2exe'])
for fileName in AUXILARY_FILES:
    shutil.copy2(SCRIPT_PATH+fileName, SCRIPT_PATH+'dist/'+fileName)
if not os.path.exists("dist/src"):
    os.makedirs("dist/src")
for fileName in SOURCE_FILES:
    shutil.copy2(SCRIPT_PATH+fileName, SCRIPT_PATH+'dist/src/'+fileName)
    
print 'Done!'
