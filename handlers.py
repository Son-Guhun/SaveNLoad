from py2exeUtils import scriptDir as SCRIPT_PATH
import subprocess
import sys
import win32api
import time
import signal
import atexit


separator = '\n' + "="*10
processDict = {}

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
   
def initiateExitHandlers():
    print "Employing signal and exit handlers..."
    atexit.register(exit_handler)
    
    #
    for sign in (signal.SIGTERM,signal.SIGABRT,signal.SIGINT,signal.SIGBREAK ):
        signal.signal(sign,signal.SIG_IGN)
        
    win32api.SetConsoleCtrlHandler(exit_handler2,1)
    print "...program will now exit gracefully."
    print separator
