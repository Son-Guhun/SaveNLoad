# -*- coding: utf-8 -*-
"""
This script is used to automatically type the contents of WC3 saves made using
Guhun's save system for RP maps.
===========
Created on Thu Oct 20 19:51:07 2016

@author: SonGuhun

v2.1.1
"""
# =============================================================================
# Define version variables
# =============================================================================
SCRIPT_VERSION_LIST = [2,1,0]
SCRIPT_VERSION_DICT = {'MAJOR' : SCRIPT_VERSION_LIST[0], 
                       'MINOR' : SCRIPT_VERSION_LIST[1], 
                       'PATCH' : SCRIPT_VERSION_LIST[2]}
SCRIPT_VERSION =   'v' + ''.join([str(x)+'.' if x != 0 else '' for x in SCRIPT_VERSION_LIST])[:-1]

# =============================================================================
# Import Python modules
# =============================================================================
import os
import platform
import subprocess
import time

# =============================================================================
# Import other SaveNLoadModules
# =============================================================================
from keypress import LoadSave
from globalVariables import WC3_PATH,SAVE_PATH,SPEED,WAIT_TIME,SCRIPT_PATH

# =============================================================================
# Functions
# =============================================================================
def ValidateWindowsVersion(validVersions, printMessage = True):
    version = platform.win32_ver()[0]
    if  version in validVersions:
        if printMessage: print "Windows",version,"Detected"
        return True
    else:
        if printMessage: print "Windows",version,"Detected - Auto Keyboard Change Unsupported"
        return False

# =============================================================================
# Main
# =============================================================================
if __name__ == '__main__':       
    #Print Version
    print "Save/Load Typing Script",SCRIPT_VERSION
    print "By: Guhun"
    
    #Check for Windows 8 or newer
    #TODO: Allow config to disable keyboard setting feature even if user has windows 8+
    windowsVersion = ValidateWindowsVersion(('8','10','8.1'))
    fullPath = WC3_PATH+SAVE_PATH
    
    #Clear leftover load requests
    try:
        os.remove(fullPath+'load.txt')
        print 'Unexpected Load Request File. Deleting File'
    except:
        pass
    
    #MAIN LOOP
    while True:
        time.sleep(1)
        try:
            with open(fullPath+'load.txt') as f:
                saveName = f.read()[69:-43]
            print 'Load call issued: ' + saveName
            LEGACY = True
            os.remove(fullPath+'load.txt')            
        except: 
            continue
        try:
            with open(fullPath+saveName+'/version.txt') as f:
                if int(f.read()[69:-43]) <= SCRIPT_VERSION['MAJOR']:
                    LEGACY = False
                else:
                    print "Incompatible save information. Please update SaveNLoad"
                    continue
        except:
                LEGACY = True
                print "Legacy save information detected"
        try: 
            with open(fullPath+saveName+'/size.txt') as f: pass
        except: 
            print 'Invalid save name'
            continue
        
        if  windowsVersion: #Execute powershell to change keyboard layout
            subprocess.Popen(['powershell','-ExecutionPolicy', 'ByPass', '-File', (SCRIPT_PATH + 'test.ps1').encode('ascii')])
    	 
        try:
            LoadSave(saveName, fullPath, SPEED, WAIT_TIME, LEGACY)
        except Exception as error:
            print error
    
        print 'Load process finished'
        #Save file for powershell to read and set user layout back to normal
        #TODO: Actually do this in a smarter way
        with open(SCRIPT_PATH + "me.txt","w") as f:
            f.write("0")
