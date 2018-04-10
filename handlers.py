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
    
    
CONTINUE_FLAG = True


def exit_handler2(sig_num, b=None):
    global CONTINUE_FLAG
    # with open(SCRIPT_PATH+'lol.txt', 'w') as f:
    #     f.write(str(sig_num))
    if sig_num == 2:
        pass
        # sys.stderr = open(SCRIPT_PATH+'out.txt', 'w')
        # sys.stdout = open(SCRIPT_PATH+'err.txt', 'w')
        exit_handler()
    else:
        CONTINUE_FLAG = False
    return 0


def exit_handler():
    print separator
    for tup in processDict.values():
        process = tup[0]
        func = tup[1][0]
        args = tup[1][1]
        kargs = tup[1][2]

        func(process, *args, **kargs)
        print 'Waiting for child process to end'
        for t in xrange(1, 10):
            if process.poll() is not None:
                break
            time.sleep(1)
            print '...'+str(t)+' second(s)'
        if process.poll() is not None:
            print 'Child process sucessfully finished.'
        else:
            print 'Child process did not finish, killing it...'
            process.kill()
            process.wait()
        print separator
    print 'All Child processes have been closed.'
    processDict.clear()
    time.sleep(5)


def PopenWrapper(exit_func, exit_func_args, exit_func_kwargs, *args, **kwargs):
    p = subprocess.Popen(*args, **kwargs)
    processDict[id(p)] = (p, (exit_func, exit_func_args, exit_func_kwargs))
    return p


def initiateExitHandlers():
    print "Employing signal and exit handlers..."
    atexit.register(exit_handler)
    #
    for sign in (signal.SIGTERM, signal.SIGABRT, signal.SIGINT, signal.SIGBREAK):
        signal.signal(sign, signal.SIG_IGN)
        
    win32api.SetConsoleCtrlHandler(exit_handler2, 1)
    print "...program will now exit gracefully."
    print separator
