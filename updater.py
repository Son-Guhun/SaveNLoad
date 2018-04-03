#Required for sending a GET request for update checks
from multiprocessing import Process, Manager,freeze_support
import requests

import traceback

from py2exeUtils import scriptDir as SCRIPT_PATH


def f(d):
    try:
        d['value'] = d['a']('https://api.github.com/repos/Son-Guhun/SaveNLoad/releases/latest', verify=d['b']+'cacert.pem')
    except KeyboardInterrupt:
        pass
def getNewestVersion():
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
        return check['tag_name']
    except Exception as error:
        print 'Error finding new version.'
        traceback.print_exc()
    except  KeyboardInterrupt:
        print '...Version retrieval interrupted by user.'
    return ''

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