# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 00:35:49 2018

@author: criow
"""

SOURCE_FILES=[
        #Python Files
        'Optimizer.py',
        'Converter.py',
		'compile.py',
		'setup.py'
		]

AUXILARY_FILES=[
        ]

import subprocess
import sys
import shutil
import os

	
SCRIPT_PATH = ''.join([x+'/' for x in sys.argv[0].split('/')[:-1]])

subprocess.call(['python','setup.py','py2exe'])
for fileName in AUXILARY_FILES:
    shutil.copy2(SCRIPT_PATH+fileName, SCRIPT_PATH+'dist/'+fileName)
if not os.path.exists("dist/src"):
    os.makedirs("dist/src")
for fileName in SOURCE_FILES:
    shutil.copy2(SCRIPT_PATH+fileName, SCRIPT_PATH+'dist/src/'+fileName)
    
print 'Done!'