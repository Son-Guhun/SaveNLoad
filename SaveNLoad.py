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
import traceback #Error reporting/printing
import subprocess #Used to execute powershell script
import platform #Used to retrieve windows version

#Required for sending a GET request for update checks
import updater
from multiprocessing import Process, Manager,freeze_support

#Required for signal and exit handling
import sys
import win32api
import atexit
import signal

# =============================================================================
# Import other SaveNLoadModules
# =============================================================================
from keypress import LoadSave
from globalVariables import WC3_PATH,SAVE_PATH,SPEED,WAIT_TIME,CHANGE_KEYBD,SCRIPT_PATH


# =============================================================================
# Define version variables
# =============================================================================
class version:
    major = 2
    minor = 2
    patch = 0
    asList = [major,minor,patch]
    asDict = {'MAJOR' : major, 
              'MINOR' : minor, 
              'PATCH' : patch}
    asString =   'v' + ''.join([str(x)+'.' if x != 0 else '' for x in asList])[:-1]


if __name__ == '__main__':
    freeze_support()

    separator = '\n' + "="*10

# =============================================================================
# Check for updates
# =============================================================================
if __name__ == '__main__':
    newestVersion = updater.getNewestVersion()
    if newestVersion:
        if newestVersion == version.asString:
            print 'SaveNLoad is up-to-date.'
        else:
            print 'New version is available: Check "Updates" shortcut.'
    
    print separator
    
#a =   requests.get('https://api.github.com/repos/Son-Guhun/SaveNLoad/releases/latest', verify=SCRIPT_PATH+'cacert.pem')
#check = a.json()
#print check['tag_name']


# =============================================================================
# SIGNAL AND EXIT HANDLING
# =============================================================================
processDict = {}
CREATE_NO_WINDOW = 0x08000000
def KillPowershell(process):
    process.communicate('Anything')
    
    
a = True
def exit_handler2(sigNo,b=None):
    global a
    with open(SCRIPT_PATH+'lol.txt','w') as f:
        f.write(str(sigNo))
    if sigNo == 2:
        pass
        sys.stderr = open(SCRIPT_PATH+'out.txt','w')
        sys.stdout = open(SCRIPT_PATH+'err.txt','w')
        exit_handler()
    else:
        a = False
    return 0

def exit_handler():
    print separator
    for tup in processDict.values():
        process = tup[0]
        func = tup[1][0]
        args = tup[1][1]
        kargs = tup[1][2]
        
        
        
        func(process,*args,**kargs)
        print 'Waiting for child process to end'
        for t in xrange(1,10):
            if process.poll() != None: break
            time.sleep(1)
            print '...'+str(t)+' second(s)'
        if process.poll() != None:
            print 'Child process sucessfully finished.'
        else:
            print 'Child process did not finish, killing it...'
            process.kill()
            process.wait()
        print separator
    print 'All Child processes have been closed.'
    processDict.clear()
    time.sleep(5)
    
def PopenWrapper(exitFunc,exitFunc_args,exitFunc_kargs,*args,**kargs):        
    p = subprocess.Popen(*args,**kargs)
    processDict[id(p)] = (p,(exitFunc,exitFunc_args,exitFunc_kargs))
    return p
   
    
print "Employing signal and exit handlers..."
atexit.register(exit_handler)

#
for sign in (signal.SIGTERM,signal.SIGABRT,signal.SIGINT,signal.SIGBREAK ):
    signal.signal(sign,signal.SIG_IGN)
    
win32api.SetConsoleCtrlHandler(exit_handler2,1)
print "...program will now exit gracefully."
print separator


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
            p = PopenWrapper(KillPowershell,[],{},
                             ['powershell','-windowstyle','hidden',
                              '-ExecutionPolicy', 'ByPass', '-File', 
                              ('ChangeLanguageList.ps1').encode('ascii')],
                              stdout = subprocess.PIPE, stdin=subprocess.PIPE,
                              creationflags = CREATE_NO_WINDOW)
            print p.stdout.readline()[:-1]
            
        LoadSave(saveName, fullPath, SPEED, WAIT_TIME, LEGACY)

        #Save file for powershell to read and set user layout back to normal
        #TODO: Actually do this in a smarter way
        if windowsVersion and CHANGE_KEYBD:
            print ("Restoring user's language list...")
            p.communicate("Anything")
            del processDict[id(p)]
            if p.returncode:
                print("Error upon restoring user's language list. Code: "+str(p.returncode))
            else:
                print("Sucessfully restored user's language list.")
    except Exception as error:
        return error
    
    return None
    
    
if __name__ == '__main__':       
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
    
    #MAIN LOOP
    print
    print 'Executable directory: ' + SCRIPT_PATH
    print 'Save files directory: ' + fullPath
    print separator[1:]
    while a:
        time.sleep(1)
        requestedSave = PollRequest()
        if isinstance(requestedSave, Exception): print requestedSave
        elif not requestedSave: pass
        else:
            ERROR = Main(requestedSave)
            if ERROR: print ERROR
            print 'Load Process Finished'
            print separator
        
