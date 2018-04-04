# -*- coding: utf-8 -*-
"""
This script is used to automatically type the contents of WC3 saves made using
Guhun's save system for RP maps.
===========
Created on Thu Oct 20 19:51:07 2016

@author: SonGuhun

v2.2
"""
# =============================================================================
# Import Python and 3rd party modules
# =============================================================================
import os #Used to delete files
import time
#import traceback #Error reporting/printing
import subprocess #Used to execute powershell script
import platform #Used to retrieve windows version

#Required for sending a GET request for update checks
from multiprocessing import freeze_support

# =============================================================================
# Import other SaveNLoadModules
# =============================================================================
from keypress import LoadSave
from globalVariables import WC3_PATH,SAVE_PATH,SPEED,WAIT_TIME,CHANGE_KEYBD,SCRIPT_PATH
import updater
import handlers

# =============================================================================
# Define version class
# =============================================================================
class version:
    major = 2
    minor = 3
    patch = 0
    asList = [major,minor,patch]
    asDict = {'MAJOR' : major, 
              'MINOR' : minor, 
              'PATCH' : patch}
    asString =   'v' + ''.join([str(x)+'.' if x != 0 else '' for x in asList])[:-1]

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
    
def PollRequest():
    try:
        with open(fullPath+'load.txt') as f:
            saveName = f.read()[69:-43]
        print 'Load call issued: ' + saveName
        os.remove(fullPath+'load.txt')
        return saveName            
    except Exception as error:
        if isinstance(error,IOError):
            if error.errno == 2:
                return None
            elif error.errno == 32:
                print "Warcraft III is still processing the request file."
                #If this continues, then the program might not have permission to access the file
                return None
            else:
                return error
        else:
            return error
    
def Main(saveName):
    try:
        with open(fullPath+saveName+'/version.txt') as f:
            if int(f.read()[69:-43]) <= version.major:
                LEGACY = False
            else:
                print "Incompatible save information. Please update SaveNLoad"
                return None
    except Exception as error:
        if isinstance(error,IOError) and error.errno == 2:
            LEGACY = True
            print "Legacy save information detected"
        else:
            return error
    try: 
        with open(fullPath+saveName+'/size.txt') as f: pass
    except Exception as error: 
        if isinstance(error,IOError) and error.errno == 2:
            print 'Save data not found under requested name'
            return None
        else:
            return error
    
    try:
        if  windowsVersion and CHANGE_KEYBD: #Execute powershell to change keyboard layout
            print("Attempting to change user's language list...")
            #p = subprocess.Popen(['powershell','-ExecutionPolicy', 'ByPass', '-File', ('ChangeLanguageList.ps1').encode('ascii')],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
            p = handlers.PopenWrapper(handlers.KillPowershell,[],{},
                             ['powershell','-windowstyle','hidden',
                              '-ExecutionPolicy', 'ByPass', '-File', 
                              ('ChangeLanguageList.ps1').encode('ascii')],
                              stdout = subprocess.PIPE, stdin=subprocess.PIPE,
                              creationflags = CREATE_NO_WINDOW)
            print p.stdout.readline()[:-1]
            
        LoadSave(saveName, fullPath, SPEED, WAIT_TIME, LEGACY)

        #Send input to subprocess stdin to reset user language list
        if windowsVersion and CHANGE_KEYBD:
            print ("Restoring user's language list...")
            p.communicate("Anything")
            del handlers.processDict[id(p)]
            if p.returncode:
                print("Error upon restoring user's language list. Code: "+str(p.returncode))
            else:
                print("Sucessfully restored user's language list.")
    except Exception as error:
        return error
    
    return None
    

# =============================================================================
# Main
# =============================================================================
    
if __name__ == '__main__':
    freeze_support()
    separator = '\n' + "="*10
    CREATE_NO_WINDOW = 0x08000000

# =============================================================================
# ==Check for updates
# =============================================================================
    newestVersion = updater.getNewestVersion()
    if newestVersion:
        if newestVersion == version.asString:
            print 'SaveNLoad is up-to-date.'
        else:
            print 'New version is available: Check "Updates" shortcut.'
    
    print separator
    

# =============================================================================
# ==SIGNAL AND EXIT HANDLING
# =============================================================================
    handlers.initiateExitHandlers()
    print separator   

# =============================================================================
# ==CHECK WINDOWS VERSION AND CLEAR EXISTING REQUESTS
# =============================================================================
    #Print Version
    print "Save/Load Typing Script", version.asString
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
    
# =============================================================================
# ==MAIN LOOP
# =============================================================================
    print
    print 'Executable directory: ' + SCRIPT_PATH
    print 'Save files directory: ' + fullPath
    print separator[1:]
    while handlers.a:
        time.sleep(1)
        requestedSave = PollRequest()
        if isinstance(requestedSave, Exception): print requestedSave
        elif not requestedSave: pass
        else:
            ERROR = Main(requestedSave)
            if ERROR: print ERROR
            print 'Load Process Finished'
            print separator
  
# =============================================================================
#       
# =============================================================================
#a =   requests.get('https://api.github.com/repos/Son-Guhun/SaveNLoad/releases/latest', verify=SCRIPT_PATH+'cacert.pem')
#check = a.json()
#print check['tag_name']