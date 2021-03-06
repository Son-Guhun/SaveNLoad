# Required for sending a GET request for update checks
import distutils
from distutils import dir_util
from distutils.errors import DistutilsFileError
import subprocess
import shutil
import sys


# NOTICE: If you open a console window, the child processes will maintain the original
# folder where the console was open locked. To avoid this, the original program
# must be run from a distinct directory
#
# sys.stderr = open('err.txt','w')
print sys.argv
DETACHED_PROCESS = 0x00000008
try:
    routine_id     = sys.argv[1]
    program_folder = sys.argv[2]
except IndexError:
    routine_id     = None
    program_folder = './'

# =============================================================================
# TESTING ROUTINES
# =============================================================================

# if routine_id == 'Test1':
#    try:
#        raw_input()
#        while True:
#            print 'A'
#    except:
#        pass
#    open('err2.txt','w').close()
#    while True:
#        pass
# else:
#    print sys.argv
#    raw_input('Start new program')
#    p = subprocess.Popen([program_folder+'autoupdate.exe','Test1','./'],
#                stdout = subprocess.PIPE,
#                #stdin=subprocess.PIPE,
#                creationflags = DETACHED_PROCESS)
    
# =============================================================================
# Copy files from the temporary update folder into the original folder
# =============================================================================
if routine_id == "copyFiles":
    try:
        raw_input()
#        while True:
#            print 'A'
    except:
        pass
    try:
        distutils.dir_util.copy_tree(program_folder+'.updateSnL/SaveNLoad', program_folder)
    except DistutilsFileError as error:
        import time
        time.sleep(1)  # Wait an arbitrary amount of time before trying again
        try:
            distutils.dir_util.copy_tree(program_folder+'.updateSnL/SaveNLoad', program_folder)
        except DistutilsFileError as error:
            with open(program_folder+'__AUTO_UPDATE_ERROR.txt', 'w') as f:
                f.write(error.message)
            p = subprocess.Popen([program_folder+'.updateSnL/SaveNLoad/autoupdate.exe',
                                  'error', program_folder],
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
            raise error

    p = subprocess.Popen([program_folder+'autoupdate.exe', 'deleteTemp', program_folder],
                         stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                         creationflags=DETACHED_PROCESS)
# =============================================================================
# After updating the contents of the original folder, delete the temp. one
# =============================================================================
elif routine_id == "deleteTemp":
    import os
    import time
    try:
        raw_input()
        while True:
            print 'A'
    except:
        pass
    i = 0
    while os.path.isdir(program_folder+'.updateSnL') and i < 10:
        try:
            shutil.rmtree(program_folder+'.updateSnL', ignore_errors=True)
        except:
            pass
        time.sleep(1)
        i += 1
    
    p = subprocess.Popen([program_folder+'SaveNLoad.exe'],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
# =============================================================================
# If an error occurs when copying the downloaded files, run this routine
# =============================================================================
elif routine_id == 'error':
    import time
    
    print 'An error occurred during automatic update.'
    with open(program_folder+'__AUTO_UPDATE_ERROR.txt', 'r') as f:
        print f.read()
    print 'Please attempt to manually move the files inside "' + program_folder + \
          '" to your preferred location, or manually download the software again.'
    
    raw_input('Press ENTER to go to download page, or close this window to exit.')   
    
    p = subprocess.call(['START', program_folder+'Updates.url'], shell=True)

# =============================================================================
# Run this routine if the program is directly run from the file explorer
# This can be used for testing, but warn the user they should know what they
# are doing.
# =============================================================================
else:
    from py2exeUtils import scriptDir, ConvertPath
    print 'This program is not meant to be run as a stand-alone'
    raw_input('Please press ENTER if you know what you are doing.')
#    distutils.dir_util.copy_tree(ConvertPath(scriptDir,0,2)+'.updateSnL/SaveNLoad',ConvertPath(scriptDir,0,2))
    p = subprocess.Popen([scriptDir+'.updateSnL/SaveNLoad/autoupdate.exe', 'copyFiles', ConvertPath(scriptDir, 0, None)],
                         stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                         stderr=None, creationflags=DETACHED_PROCESS)
    while True:
        print 'A'
