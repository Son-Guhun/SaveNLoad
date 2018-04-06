#Required for sending a GET request for update checks
import distutils
from distutils import dir_util
import subprocess
import shutil
import sys



#NOTICE: If you open a console window, the child processes will maintain the original
#folder where the console was open locked. To avoid this, the original program
#must be run from a distinct directory

#sys.stderr = open('err.txt','w')
print sys.argv
CREATE_NO_WINDOW = 0x00000008 #0x08000000 #subprocess.CREATE_NEW_CONSOLE 
try:
    routineID = sys.argv[1]
    programFolder = sys.argv[2]
except IndexError:
    routineID = None
    programFolder = './'
    pass

#if routineID == 'Test1':
#    try:
#        raw_input()
#        while True:
#            print 'A'
#    except:
#        pass
#    open('err2.txt','w').close()
#    while True:
#        pass
#else:
#    print sys.argv
#    raw_input('Start new program')
#    p = subprocess.Popen([programFolder+'autoupdate.exe','Test1','./'],
#                stdout = subprocess.PIPE,
#                #stdin=subprocess.PIPE,
#                creationflags = subprocess.CREATE_NEW_CONSOLE)
    

# =============================================================================
# Copy files from the temporary update folder into the original folder
# =============================================================================
if routineID == "copyFiles":
    try:
        raw_input()
#        while True:
#            print 'A'
    except:
        pass
    distutils.dir_util.copy_tree(programFolder+'.updateSnL/SaveNLoad',programFolder)
    p = subprocess.Popen([programFolder+'autoupdate.exe','deleteTemp',programFolder]
                              ,stdout = subprocess.PIPE, stdin=subprocess.PIPE,
                              creationflags = CREATE_NO_WINDOW)
# =============================================================================
# After updating the contents of the original folder, delete the temp. one
# =============================================================================
elif routineID == "deleteTemp":
    import os
    import time
    try:
        raw_input()
        while True:
            print 'A'
    except:
        pass
    i=0
    while os.path.isdir(programFolder+'.updateSnL') and i < 10:
        try:
            shutil.rmtree(programFolder+'.updateSnL',ignore_errors=True)
        except: pass
        time.sleep(1)
        i+=1
#    if os.path.isdir(programFolder+'.updateSnL'):
#        try:
#            shutil.rmtree(programFolder+'.updateSnL')
#        except:
#            p = subprocess.Popen(['START',programFolder+'autoupdate.exe','deleteTemp',programFolder],shell=True)
        
    
    
else:
    from py2exeUtils import scriptDir,ConvertPath
    print 'This program is not meant to be run as a stand-alone'
    raw_input('Please press ENTER to exit.')
#    distutils.dir_util.copy_tree(ConvertPath(scriptDir,0,2)+'.updateSnL/SaveNLoad',ConvertPath(scriptDir,0,2))
    p = subprocess.Popen([scriptDir+'.updateSnL/SaveNLoad/autoupdate.exe','copyFiles',ConvertPath(scriptDir,0,None)],
                              stdout = subprocess.PIPE, stdin=subprocess.PIPE,
                              creationflags = CREATE_NO_WINDOW)
    while True:
        print 'A'
    print p.pid()
    
    
    
#Read from PIPE:
    #Current SaveNLoad directory's path
    #Current SaveNLoad directory name
#Download ZIP file from the interwebs into a new folder in the same place as the SaveNLoad folder
#Open the executable in the new folder:
    #Try:
        #Write to Stdout
    #Except:
        #Paren is closed, we can proceed
    #Copy all files from the new directoy into the old directory
    #Open copied executable
        #Try:
            #Write to Stdout
        #Except:
            #Parent is closed, we can proceed
        #Delete old folder
    
#help(distutils.dir_util.copy_tree)
        
        
        #Try:
            #Remove executable in unzipped folder
        #Except:
            #Wait 1 second and try again