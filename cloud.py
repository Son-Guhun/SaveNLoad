GITHUB_API = 'https://api.github.com'

GITHUB_USERREPO = '/Son-Guhun/SaveNLoad'

'/repos/:owner/:repo/contents/:path'

class GitHubFile:
    def __init__(self,fileAsDict):
        self.url = fileAsDict[u'download_url']
        
    def readlines(self):
        return ReadLinesGitHubFile(self.url)
    
    def read(self,*args):
        data = urllib2.urlopen(self.url).read(*args)
        return data

class GitHubFolder:
    def __init__(self,url):
        self.url = url

def GetGitHubRepositoryContents(repository,path=''):
    contentsList = requests.get(GITHUB_API+'/repos'+GITHUB_USERREPO+'/contents').json()
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
    
    return data

def f(saveName):
    main = GetGitHubRepositoryContents(0)
    
    try:
        savePath = main[saveName][u'path']
    except KeyError:
        return None #Repos does not have that folder
    
    saveFiles = GetGitHubRepositoryContents(0,savePath)
    
    for file_ in saveFiles:
        saveFiles[file_[u'name']] = file_[u'download_url']
    
'https://developer.github.com/v3/repos/contents/'
#('https://api.github.com/repos/Son-Guhun/SaveNLoad/releases/latest', verify=d['b']+'cacert.pem')

import requests