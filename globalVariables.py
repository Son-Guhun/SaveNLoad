import os
import ctypes.wintypes

from py2exeUtils import ConvertPath
from py2exeUtils import scriptDir as SCRIPT_PATH

def SetConfigDefault(config):
    print config + " configuration file missing. Default will be set."
    with open(SCRIPT_PATH+'Settings/'+config+'.txt','w') as f:
        f.write(str(DEFAULTS[config]))
    return DEFAULTS[config]


#Get path for script if it is being run as an executable

if not os.path.exists("Settings"):
    os.makedirs("Settings")

#SETTING GLOBAL VARIABLES
try:
    with open(SCRIPT_PATH+'Settings/Warcraft-Path.txt') as f:
        WC3_PATH = ConvertPath(f.read())
except IOError:
    print "Configuration file for Warcraft III Documents Path missing."
    print "Attempting to find the folder"
    
    CSIDL_PERSONAL = 5       # My Documents
    SHGFP_TYPE_CURRENT = 0   # Get current, not default value

    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    
    if os.path.isdir(buf.value + "/Warcraft III"):
                WC3_PATH = buf.value + "\\Warcraft III"
    else:
        print "Folder not found. Opening your documents folder for you."
        WC3_PATH = raw_input("Please insert the path to your Warcraft III Documents Folder")
        
    print "Saving your Configuration"
    with open(SCRIPT_PATH+'Settings/Warcraft-Path.txt','w') as f:
        f.write(WC3_PATH)
    WC3_PATH = ConvertPath(WC3_PATH)

DEFAULTS = {
"Save-Directory" : "CustomMapData/DataManager/",
"Wait-Time" : 5,
"Typing-Speed" : 5000,
"Change-Keybd" : True,
"Check-for-Updates" : True,
"GitHub-Repository" : '/None',
"Auto-Updates" : True
}

try:    
    with open(SCRIPT_PATH+'Settings/Save-Directory.txt') as f:
        SAVE_PATH = ConvertPath(f.read())
except IOError:
    SAVE_PATH = SetConfigDefault("Save-Directory")

try:   
    with open(SCRIPT_PATH+'Settings/Wait-Time.txt') as f:
        WAIT_TIME = float(f.read().replace('\n',''))
        if WAIT_TIME < 2.:
            WAIT_TIME = 2.
except IOError:
    WAIT_TIME = SetConfigDefault("Wait-Time")
    
try:
    with open(SCRIPT_PATH+'Settings/Typing-Speed.txt') as f:
        SPEED = float(f.read().replace('\n',''))
except:
    SPEED = SetConfigDefault("Typing-Speed")
    
try:
    with open(SCRIPT_PATH+'Settings/Change-Keybd.txt') as f:
        CHANGE_KEYBD = True if f.read().replace('\n','') == 'True' else False
except:
    CHANGE_KEYBD = SetConfigDefault("Change-Keybd")

try:
    with open(SCRIPT_PATH+'Settings/Check-for-Updates.txt') as f:
        CHECK_UPDATES = True if f.read().replace('\n','') == 'True' else False
except:
    CHECK_UPDATES = SetConfigDefault("Check-for-Updates")
    
try:
    with open(SCRIPT_PATH+'Settings/GitHub-Repository.txt') as f:
        GITHUB_USERREPO = f.read()
        if GITHUB_USERREPO[0] != '/': 
            GITHUB_USERREPO = '/'+GITHUB_USERREPO
        if GITHUB_USERREPO[-1] == '/':
            GITHUB_USERREPO = GITHUB_USERREPO[:-1]
except:
    GITHUB_USERREPO = SetConfigDefault("GitHub-Repository")
    
try:
    with open(SCRIPT_PATH+'Settings/Auto-Updates.txt') as f:
        AUTO_UPDATES = True if f.read().replace('\n','') == 'True' else False
except:
    AUTO_UPDATES = SetConfigDefault("Auto-Updates")

if GITHUB_USERREPO == DEFAULTS['GitHub-Repository']:
    GITHUB_USERREPO = ''