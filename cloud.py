from globalVariables import GITHUB_USERREPO
import requests

from py2exeUtils import scriptDir as SCRIPT_PATH
import urllib2
import string

GITHUB_API = 'https://api.github.com'

# GITHUB_USERREPO = '/Son-Guhun/SnL-Cloud-Test'


class GitHubFile:
    def __init__(self, file_as_dict):
        if file_as_dict[u'type'] == 'file':
            self.url = file_as_dict[u'download_url']
        else:
            self.url = ''

    def readlines(self):
        return ReadLinesGitHubFile(self.url)
    
    def read(self, *args):
        data = convert_line_endings(urllib2.urlopen(self.url).read(*args), 0)
        return data


class GitHubFolder:
    def __init__(self, url):
        self.url = url
        try:
            self.files = GetGitHubRepositoryContents(path=url)
        except requests.exceptions.ConnectionError:
            self.files = {}

    def __getitem__(self, file_name):
        return self.files[file_name]
        

def GetGitHubRepositoryContents(repository=GITHUB_USERREPO, path=''):
    contents_list = requests.get(GITHUB_API+'/repos'+repository+'/contents/'+path,
                                 verify=SCRIPT_PATH+'cacert.pem').json()
    print 
    print 'Searching ' + GITHUB_API+'/repos'+repository+'/contents/'+path
    try:
        if contents_list[u'message'] == u'Not Found':
            return {}
    except TypeError:  # Response should be a list, not a dict like for not-found messages
        pass
    contents_dict = {}
    for entry in contents_list:
        contents_dict[entry[u'name']] = GitHubFile(entry)
    return contents_dict


# http://code.activestate.com/recipes/66434-change-line-endings/
def convert_line_endings(temp, mode):
        # modes:  0 - Unix, 1 - Mac, 2 - DOS
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


def ReadLinesGitHubFile(file_as_dict):
    try:
        data = urllib2.urlopen(file_as_dict[u'download_url']).read(20000)  # read only 20 000 chars
    except TypeError:
        data = urllib2.urlopen(file_as_dict).read(20000)
    data = convert_line_endings(data, 0)
    if data[-1] == '\n':
        ends_in_new_line = True
    else:
        ends_in_new_line = False
    data = data.split("\n")
    
    data = [line+'\n' for line in data]
    
    if not ends_in_new_line:
        data[-1] = data[-1][:-1]
    else:
        del data[-1]
    
    return data

# https://developer.github.com/v3/repos/contents/
# ('https://api.github.com/repos/Son-Guhun/SaveNLoad/releases/latest', verify=d['b']+'cacert.pem')
