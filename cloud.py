GITHUB_API = 'https://api.github.com'

#GITHUB_USERREPO = '/Son-Guhun/SnL-Cloud-Test'

'/repos/:owner/:repo/contents/:path'

from globalVariables import GITHUB_USERREPO

#TODO: Create necessary settings
#TODO: Test the program under conditions where there is no internet connection

import requests

from py2exeUtils import scriptDir as SCRIPT_PATH

class GitHubFile:
    def __init__(self,fileAsDict):
        if fileAsDict[u'type'] == 'file':
            self.url = fileAsDict[u'download_url']
        else:
            self.url = ''
        
    def readlines(self):
        return ReadLinesGitHubFile(self.url)
    
    def read(self,*args):
        data = convert_line_endings(urllib2.urlopen(self.url).read(*args),0)
        return data
 
class GitHubFolder:
    def __init__(self,url):
        print 
        print url
        self.url = url
        self.files = GetGitHubRepositoryContents(0,url)
        

def GetGitHubRepositoryContents(repository,path=''):
    contentsList = requests.get(GITHUB_API+'/repos'+GITHUB_USERREPO+'/contents/'+path, verify=SCRIPT_PATH+'cacert.pem').json()
    try:
        if contentsList[u'message'] == u'Not Found':
            return {}
    except: pass
    contentsDict = {}
    for entry in contentsList:
        contentsDict[entry[u'name']] = GitHubFile(entry)
    return contentsDict

def GetFileLink():
    return 0

import urllib2
import string

#http://code.activestate.com/recipes/66434-change-line-endings/
def convert_line_endings(temp, mode):
        #modes:  0 - Unix, 1 - Mac, 2 - DOS
        if mode == 0:
                temp = string.replace(temp, '\r\n', '\n')
                temp = string.replace(temp, '\r', '\n')
        elif mode == 1:
                temp = string.replace(temp, '\r\n', '\r')
                temp = string.replace(temp, '\n', '\r')
        elif mode == 2:
                import re
                temp = re.sub("\r(?!\n)|(?<!\r)\n", "\r\n", temp)
        return temp

def ReadLinesGitHubFile(fileAsDict):
    try:
        data = urllib2.urlopen(fileAsDict[u'download_url']).read(20000) # read only 20 000 chars
    except TypeError:
        data = urllib2.urlopen(fileAsDict).read(20000)
    data = convert_line_endings(data,0)
    if data[-1] == '\n':
        endsInNewline = True
    else:
        endsInNewline = False
    data = data.split("\n") # then split it into lines
    
    data = [line+'\n' for line in data]
    
    if not endsInNewline:
        data[-1] = data[-1][:-1]
    else:
        del data[-1]
    
    return data
    
#https://developer.github.com/v3/repos/contents/
#('https://api.github.com/repos/Son-Guhun/SaveNLoad/releases/latest', verify=d['b']+'cacert.pem')
