# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 00:35:49 2018

@author: criow
"""

from py2exeUtils import Compiler

a= Compiler(
    [
        #Python Files
        'SaveNLoad.py',
        'keypress.py',
        'globalVariables.py',
        'updater.py',
        'handlers.py',
        'setup.py',
        'compile.py',
        #
        'tqdmLite/__init__.py',
        'tqdmLite/__main__.py',
        'tqdmLite/_main.py',
        'tqdmLite/_monitor.py',
        'tqdmLite/_tqdm.py',
        'tqdmLite/_utils.py',
        'tqdmLite/_version.py',
        #Powershell Files
        'ChangeLanguageList.ps1',
        #SSL Certification
        'cacert.pem',
        #URL Link
        'Updates.url'],
     [
        'ChangeLanguageList.ps1',
        'cacert.pem',
        'Updates.url']
)
a.changeFolderNames('SaveNLoad')
a.Compile()
print 'Done!'