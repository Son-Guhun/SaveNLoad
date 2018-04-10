# -*- coding: utf-8 -*-
"""
This script is used to automatically type the contents of WC3 saves made using
Guhun's save system for RP maps.
===========
Created on Thu Oct 20 19:51:07 2016

@author: SonGuhun

v2.3.0
"""
# =============================================================================
# Import Python and 3rd party modules
# =============================================================================
import os  # Used to delete files
import time
import traceback  # Error reporting/printing
import subprocess  # Used to execute powershell script
import platform  # Used to retrieve windows version

# Required for sending a GET request for update checks
from multiprocessing import freeze_support
from requests import exceptions as req_error


# =============================================================================
# Import other SaveNLoadModules
# =============================================================================
from keypress import Save
from globalVariables import WC3_PATH, SAVE_PATH, SPEED, WAIT_TIME, CHANGE_KEYBD, \
                            SCRIPT_PATH, CHECK_UPDATES, AUTO_UPDATES
import updater
import handlers


# =============================================================================
# Define version class
# =============================================================================
class version:
    major = 2
    minor = 3
    patch = 0
    suffix = ''
    asList = [major, minor, patch]
    asDict = {'MAJOR': major,
              'MINOR': minor,
              'PATCH': patch}
    asString = 'v' + '.'.join([str(x) for x in asList]) + suffix


# =============================================================================
# Functions
# =============================================================================
def validateWindowsVersion(valid_versions, print_message=True):
    win_version = platform.win32_ver()[0]
    if win_version in valid_versions:
        if print_message:
            print "Windows", win_version, "Detected"
        return True
    else:
        if print_message:
            print "Windows", win_version, "Detected - Auto Keyboard Change Unsupported"
        return False


def pollRequest():
    try:
        with open(PATH_TO_SAVES+'load.txt') as f:
            save_name = f.read()[69:-43]
        print 'Load call issued: ' + save_name
        os.remove(PATH_TO_SAVES+'load.txt')
        return save_name            
    except Exception as err:
        if isinstance(err, IOError):
            if err.errno == 2:
                return None
            elif err.errno == 32:
                print "Warcraft III is still processing the request file."
                # If this continues, then the program might not have permission to access the file
                return None
            else:
                return err
        else:
            return err


def main(save_name):
    save = Save(PATH_TO_SAVES, save_name)
    
    if not save.type:
        return 'Could not find specified save folder under any directory'
    
    if not save.getSize():
        return 'Save data not found under requested name'
    
    if not save.getVersion():
        return 'Error when retrieving save data'
    elif save.version < version.major:
        print "Legacy save information detected"
    elif save.version > version.major:
        return "Incompatible save information. Please update SaveNLoad"

    try:
        if WINDOWS_VERSION and CHANGE_KEYBD:  # Execute powershell to change keyboard layout
            print("Attempting to change user's language list...")
            p = handlers.PopenWrapper(handlers.KillPowershell, [], {},
                                      ['powershell', '-windowstyle', 'hidden',
                                       '-ExecutionPolicy', 'ByPass', '-File',
                                       'ChangeLanguageList.ps1'.encode('ascii')],
                                      stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                      creationflags=CREATE_NO_WINDOW)
            print p.stdout.readline()[:-1]
            
        save.loadData(SPEED, WAIT_TIME)

        # Send input to subprocess stdin to reset user language list
        if WINDOWS_VERSION and CHANGE_KEYBD:
            print ("Restoring user's language list...")
            p.communicate("Anything")
            del handlers.processDict[id(p)]
            if p.returncode:
                print("Error upon restoring user's language list. Code: "+str(p.returncode))
            else:
                print("Sucessfully restored user's language list.")
    except Exception as err:
        traceback.print_exc()
        return err
    
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
    try:
        if CHECK_UPDATES:
            print "Attemtping to retrieve latest version..."
            print "...(Press Ctrl+C to cancel)..."
            newestVersion = updater.getNewestVersion()
            if newestVersion:
                print
                if newestVersion == version.asString:
                    print 'SaveNLoad is up-to-date.'
                else:
                    if AUTO_UPDATES:
                        updater.autoUpdate()
                    else:
                        print 'New version is available: Check "Updates" shortcut.'
                        print
                        if raw_input("Would you like to download the newest version now? y/n: ") in ('Y', 'y'):
                            if not subprocess.call(['START', SCRIPT_PATH+'Updates.url'], shell=True):
                                print "Could not find Updates.url file"
        else:
            print 'Automatic update checks are disabled.'
    except req_error.ConnectionError:
        print '...Could not connect to the host server.'
        traceback.print_exc()
    except KeyboardInterrupt:
        print '...Version retrieval interrupted by user.'
        try:
            if AUTO_UPDATES and os.path.exists(updater.ZIP_DOWNLOAD_PATH+'/Update.zip'):
                os.remove(updater.ZIP_DOWNLOAD_PATH+'/Update.zip')
                os.rmdir(updater.ZIP_DOWNLOAD_PATH)
        except WindowsError:
            traceback.print_exc()
            print
            print 'Failed to remove temporary update files'

    print separator

# =============================================================================
# ==SIGNAL AND EXIT HANDLING
# =============================================================================
    handlers.initiateExitHandlers()
    print separator   

# =============================================================================
# ==CHECK WINDOWS VERSION AND CLEAR EXISTING REQUESTS
# =============================================================================
#     Print Version
    print "Save/Load Typing Script", version.asString
    print "By: Guhun"
    
    # Check for Windows 8 or newer
    WINDOWS_VERSION = validateWindowsVersion(('8', '10', '8.1'))
    PATH_TO_SAVES = WC3_PATH+SAVE_PATH

    # Clear leftover load requests
    try:
        os.remove(PATH_TO_SAVES+'load.txt')
        print 'Unexpected Load Request File. Deleting File'
    except WindowsError as error:
        if error.winerror == 2:  # file not found
            pass
        else:
            print 'Unexpected Load Request File was present, but there was an error deleting it.'
    
# =============================================================================
# ==MAIN LOOP
# =============================================================================
    print
    print 'Executable directory: ' + SCRIPT_PATH
    print 'Save files directory: ' + PATH_TO_SAVES
    print separator[1:]
    while handlers.CONTINUE_FLAG:
        time.sleep(1)
        requested_save = pollRequest()
        if isinstance(requested_save, Exception):
            print requested_save
        elif not requested_save:
            pass
        else:
            exception = main(requested_save)
            if exception:
                print exception
            print 'Load Process Finished'
            print separator
            
# =============================================================================
#       
# =============================================================================
# a =   requests.get('https://api.github.com/repos/Son-Guhun/SaveNLoad/releases/latest',
#                    verify=SCRIPT_PATH+'cacert.pem')
# check = a.json()
# print check['tag_name']
