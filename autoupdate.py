#Required for sending a GET request for update checks
import distutils
import subprocess
import shutil

routineID = raw_input()
programFolder = raw_input()

if routineID == "copy files":
    try:
        while True:
            print 'A'
    except:
        pass
    distutils.dir_util.copy_tree(programFolder+'.updateSnL',programFolder)
    p = subprocess.Popen(stdin=subprocess.PIPE,stdout=subprocess.PIPE) 
    p.stdin.write("delete temp\n"+
                  programFolder+'\n')
elif routineID == "delete temp":
    try:
        while True:
            print 'A'
    except:
        pass
    shutil.rmtree(programFolder+'.updateSnL')
    
    
    
    
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