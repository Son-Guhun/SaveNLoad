# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 00:35:49 2018

@author: criow
"""

SOURCE_FILES=[
        'SaveNLoad.py',
        'keypress.py',
        'globalVariables.py',
        'setup.py',
        'compile.py']

import subprocess
import shutil
import os
from globalVariables import SCRIPT_PATH



subprocess.call(['python','setup.py','py2exe'])
shutil.copy2(SCRIPT_PATH+'test.ps1', SCRIPT_PATH+'dist/test.ps1')
if not os.path.exists("dist/src"):
    os.makedirs("dist/src")
for fileName in SOURCE_FILES:
    shutil.copy2(SCRIPT_PATH+fileName, SCRIPT_PATH+'dist/src/'+fileName)
shutil.copy2(SCRIPT_PATH+'test.ps1', SCRIPT_PATH+'dist/src/test.ps1')
    
print 'Done!'
while True:
    pass