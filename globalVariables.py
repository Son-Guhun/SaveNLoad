import sys
import os
import ctypes.wintypes

#Convert \ to /
def ConvertPath(path, directoriesFrom = 0, directoriesUntil = None, lastFowardSlash = True):
    """
    Recieves a string which should be a path to a file. If the directory separator
    is '\\', then it is converted to '/' and the path is returned. The return value
    is a path string with '/' as directory separators and with '/' at the end.
    
    Optional varaibles:
        directoriesFrom => Removes the specified number of directories from the start of the path.
        directoriesUntil => Removes the specified number of directories from the end of the path.
        lastFowardSlash => If false, remove the last foward slash from the return value.
    """
    if directoriesUntil:
        directoriesUntil = -directoriesUntil
        
    if '\\' in path: 
        pathList = path.split("\\")
    else: 
        pathList = path.split("/")
    
    if pathList[-1] == "":
        del pathList[-1]
    pathList = [x + "/" for x in pathList[directoriesFrom:directoriesUntil]]
    path = "".join(pathList)   
    
    if not lastFowardSlash:
        return path[:-1]
    return path

def SetConfigDefault(config):
	print config + " configuration file missing. Default will be set."
	with open(SCRIPT_PATH+'Settings/'+config+'.txt','w') as f:
		f.write(str(DEFAULTS[config]))
	return DEFAULTS[config]


#Get path for script if it is being run as an executable
SCRIPT_PATH = ConvertPath(sys.argv[0], directoriesUntil = 1)
print SCRIPT_PATH

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
"Typing-Speed" : 5000
}

try:    
	with open(SCRIPT_PATH+'Settings/Save-Directory.txt') as f:
		SAVE_PATH = ConvertPath(f.read())
except IOError:
	SAVE_PATH = SetConfigDefault("Save-Directory")

try:   
	with open(SCRIPT_PATH+'Settings/Wait-Time.txt') as f:
		WAIT_TIME = float(f.read())
		if WAIT_TIME < 2.:
			WAIT_TIME = 2.
except IOError:
	WAIT_TIME = SetConfigDefault("Wait-Time")
    
try:
	with open(SCRIPT_PATH+'Settings/Typing-Speed.txt') as f:
		SPEED = float(f.read())
except:
	SPEED = SetConfigDefault("Typing-Speed")
