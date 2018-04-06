#Required for sending a GET request for update checks
from multiprocessing import Process, Manager,freeze_support
import requests
import os

from tqdmLite import tqdm
import zipfile
import traceback

from py2exeUtils import scriptDir as SCRIPT_PATH
import py2exeUtils as p2eU

import subprocess
#['assets'][0]['browser_download_url']

def itercontent(self, chunk_size=512, decode_unicode=False):
    return requests.Response.iter_content(self, chunk_size=chunk_size, decode_unicode=decode_unicode)

def f(d):
    try:
        d['value'] = d['a']('https://api.github.com/repos/Son-Guhun/SaveNLoad/releases/latest', verify=d['b']+'cacert.pem')
    except KeyboardInterrupt:
        pass

def getNewestVersionEx():    
    try:
        if __name__ == '__main__':
            freeze_support()
        manager = Manager()
    
        d = manager.dict()
        d['a'] = requests.get
        d['b'] = SCRIPT_PATH
        
        print "Attemtping to retrieve latest version..."
        print "...(Press Ctrl+C to cancel)..."
        p = Process(target=f, args=(d, ))
        p.start()
        i=0
        while p.is_alive() and i<334:
            p.join(0.03)
            i+=1
        
        if p.is_alive():
            p.terminate()
            raise Exception('Connection did not complete within timeout.')
    
        check = d['value'].json() 
    #        print
    #        if check['tag_name'] == version.asString:
    #            print 'SaveNLoad is up-to-date.'
    #        else:
    #            print 'New version is available: Check "Updates" shortcut.'
        return check
    except Exception as error:
        print 'Error finding new version.'
        traceback.print_exc()
    except  KeyboardInterrupt:
        print '...Version retrieval interrupted by user.'
    return {}

def getNewestVersion():
    a = getNewestVersionEx()
    return a['tag_name'] if a else ''
    
def makeDirSafe(*args,**kargs):
    try:
        os.mkdir(*args,**kargs)
    except WindowsError as error:
        if error.winerror == 183: pass #Windows error: cannot create an existing file
        else: raise error 
    

def extractUpdate():
    with zipfile.ZipFile(SCRIPT_PATH+'.updateZip/Update.zip','r') as zip_:
        makeDirSafe(SCRIPT_PATH+'.updateSnL')
        zip_.extractall(SCRIPT_PATH+'.updateSnL')

def downloadNewestVersion():
    releaseDict = getNewestVersionEx()
    downloadLink = releaseDict['assets'][0]['browser_download_url']
    makeDirSafe(SCRIPT_PATH+'.updateZip')
    
    response = requests.get(downloadLink, stream=True)
    length = int(response.headers['Content-Length'])

    with open(SCRIPT_PATH+'.updateZip/Update.zip', "wb") as handle:
        for data in tqdm(response.iter_content(chunk_size=1024*500),unit='kb',unit_scale=500,total=length/1024./500.):
            handle.write(data)
            
    print 'duh'
            
def autoUpdate():
    
    if not p2eU.frozen:
        print 'Auto Update is only supported when using the compiled executable.'
        return False
    
    downloadNewestVersion()
    extractUpdate()
    
    p = subprocess.popen([SCRIPT_PATH+'.updateSnL/SaveNLoad/autoupdate.exe'],
                              stdout = subprocess.PIPE, stdin=subprocess.PIPE,
                              creationflags = subprocess.CREATE_NEW_CONSOLE)
    
    

#def f(d):
#    try:
#        d['value'] = d['a']('https://api.github.com/repos/Son-Guhun/SaveNLoad/releases/latest', verify=d['b']+'cacert.pem')
#    except KeyboardInterrupt:
#        pass
#try:
#    if __name__ == '__main__':
#        freeze_support()
#        manager = Manager()
#    
#        d = manager.dict()
#        d['a'] = requests.get
#        d['b'] = SCRIPT_PATH
#        
#        print "Attemtping to retrieve latest version..."
#        print "...(Press Ctrl+C to cancel)..."
#        p = Process(target=f, args=(d, ))
#        p.start()
#        i=0
#        while p.is_alive() and i<334:
#            p.join(0.03)
#            i+=1
#        
#        if p.is_alive():
#            p.terminate()
#            raise Exception('Connection did not complete within timeout.')
#    
#        check = d['value'].json() 
#        print
#        if check['tag_name'] == version.asString:
#            print 'SaveNLoad is up-to-date.'
#        else:
#            print 'New version is available: Check "Updates" shortcut.'
#except Exception as error:
#    print 'Error finding new version.'
#    traceback.print_exc()
#except  KeyboardInterrupt:
#    print '...Version retrieval interrupted by user.'