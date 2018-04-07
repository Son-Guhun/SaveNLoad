# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 00:42:48 2018

This module provides an API to read Save/Load saves and to send them as chat
messages in-game.

@author: criow
"""
# =============================================================================
# 3rd party modules
# =============================================================================
import time
from win32api import keybd_event
import random
import win32gui
import os
from urllib2 import URLError
from py2exeUtils import ConvertPath

# =============================================================================
# SaveNLoad modules
# =============================================================================
from globalVariables import GITHUB_USERREPO
import cloud


# =============================================================================
# File-like and Save classes
# =============================================================================
class FileName:
    """
    A file-like object that supports reading from local files.
    
    Stores a file name as a string, and the read/readlines methods work by
    opening the file, using the respective File class method and closing the
    file.
    """
    def __init__(self,file_path):
        if not os.path.isdir(file_path):
            self.path = file_path
        else:
            self.path = ''
    
    def read(self,*args):
        with open(self.path,'r') as f:
            content = f.read(*args)
        return content
    
    def readlines(self,*args):
        with open(self.path,'r') as f:
            content = f.readlines(*args)
        return content


class Folder:
    """
    A folder-like object that stores the contents of a local directory as a dict
    of FileName instances.
    
    Any folders
    """
    def __init__(self,folderPath):
        self.path = ConvertPath(folderPath)
        if os.path.exists(folderPath):
            contents = os.listdir(self.path)
            self.files ={}
            for file_ in contents:
                self.files[file_] = FileName(self.path+file_) 
        else:
            self.files = {}
            
    def __getitem__(self,file_name):
        return self.files[file_name]
            
class Save:
    """
    A class that represents a save folder. It supports opening folders using
    any of the folder-like classes, like Folder and GitHubFolder created for
    SaveNLoad.
    
    Member fields:
        name    : The name of the Save's folder in a saves directory
        folder  : A folder-like object representing the Save's folder
        type    : The type of the Save (how it is stored)
        size    : The number of numbered .txt files in the Save's folder
        version : The major version number with which the Save was made in wc3.
        
    The 'version' and 'size' members are initialized as 0. To retrieve the
    actual size and version number of the 
    """
    
    _TYPES_ORDERED = ['local', 'github']
    _TYPES = {'local' : Folder, 
              'github' : cloud.GitHubFolder if GITHUB_USERREPO else None}
    
    def __init__(self,savesPath,saveName):
        self.name = saveName       
        for saveType in Save._TYPES_ORDERED:
            if Save._TYPES[saveType]:
                self.folder = Save._TYPES[saveType](savesPath+saveName
                                         if saveType=='local' else saveName)
                if self.folder.files:
                    self.type = saveType
                    break
        if not self.folder.files:
            self.folder = None
            self.type = ''
                    
        self.size = 0
        self.version = 0
        
    def __getitem__(self,file_name):
        return self.folder[file_name]
        
    def getSize(self):
        """
        Reads 'size.txt' inside a save folder to retrieve its size. Once the size
        has been retrieved, it is stored in the 'size' member field.
        """
        try:
            self.size = int(self['size.txt'].read()[69:-43])
        except (IOError,URLError):
            self.size = 0
        return self.size
    
    def getVersion(self):
        """
        Reads 'version.txt' inside a save folder to retrieve its size. Once it
        has been retrieved, the version number is stored in the 'version' 
        member field. 
        
        If no 'version.txt' file is found, the Save is considered a version 1 
        Save.
        """
        try:
            self.version = int(self['version.txt'].read()[69:-43])
        except Exception as error:
            if isinstance(error,IOError) and error.errno == 2 or isinstance(error,URLError) and error.errno == 11001:
                self.version = 1
            else:
                self.version = 0
        return self.version
    
    def _readData(self,number):
        """
        Reads data from a numbered file .txt in a save directory.
        
        Returns a list with each line of the file, parsed to the format accepted by the in-game save/load.
        """
        if self.version == 2: 
            save_data = self[number+'.txt'].readlines()[2:-5]
            save_data = [ x[16:-4] for x in save_data]
        else:
            save_data = self[number+'.txt'].read()[69:-43]
            save_data = save_data.split("\\\\n")
        return save_data
    
    def loadData(self,speed,waitTime):
        """
        Retrives the Save's data from the saves directory. Then all the data is typed
        automatically and sent as chat messages to be parsed in-game.
        """
        time.sleep(waitTime)
        sendChatMessage('-load ini',speed=speed)
        time.sleep(0.5)
        for x in range(0,self.size):        
            try:
                if not typeSaveData(self._readData(str(x)),speed):
                    print 'Warcraft III window not in focus. Abort.'
                    return
            except (IOError,URLError) :
                print "SaveID:", self.name, "file number",x,"could not be read."
        time.sleep(0.5)
        sendChatMessage('-load end',speed=speed)


# =============================================================================
# Functions
# =============================================================================
def getCurWindowText():
    	return  win32gui.GetWindowText(win32gui.GetForegroundWindow());  

#Functions to Parse WC3 text files
def sendChatMessage(message,speed):
    """
    Send a chat message in Warcraft III by typing ENTER + MESSAGE + ENTER
    """
    press('ENTER')
    write(message,speed)
    press('ENTER')

def typeSaveData(saveData,speed):
    """
    Recieves a list of strings. Sends each string as a chat message in-game.
    
    Returns false if the WC3 window is not in focus while typing.
    Returns true upon successfully finishing the typing routine.
    """
    for unitData in saveData:
        if getCurWindowText() == "Warcraft III":
            sendChatMessage(unitData,speed=speed)
        else:
            return False
    return True

# =============================================================================
# Keypress Script
# Special Thanks to Piotr Dabkowski (stackoverflow user) for this script
# http://stackoverflow.com/questions/14076207/simulating-a-key-press-event-in-python-2-7
# =============================================================================
def keyUp(key):
    """Releases a key given an integer."""
    if getCurWindowText() != "Warcraft III":
        return
    keybd_event(key, 0, 2, 0)


def keyDown(key):
    """Presses down a key given an integer."""
    if getCurWindowText() != "Warcraft III":
        return
    keybd_event(key, 0, 1, 0)


def press(Key, speed=1):
    """Presses down then releases a key given a string"""
    rest_time = 0.05/speed
    if Key in Base:
        Key = Base[Key]
        keyDown(Key)
        time.sleep(rest_time)
        keyUp(Key)
        return True
    if Key in Combs:
        keyDown(Base[Combs[Key][0]])
        time.sleep(rest_time)
        keyDown(Base[Combs[Key][1]])
        time.sleep(rest_time)
        keyUp(Base[Combs[Key][1]])
        time.sleep(rest_time)
        keyUp(Base[Combs[Key][0]])
        return True
    return False


def write(Str, speed = 1):
    """Types a string of letters"""
    for s in Str:
        press(s, speed)
        time.sleep((0.1 + random.random()/10.0) / float(speed))

Combs = {
    'A': [
        'SHIFT',
        'a'],
    'B': [
        'SHIFT',
        'b'],
    'C': [
        'SHIFT',
        'c'],
    'D': [
        'SHIFT',
        'd'],
    'E': [
        'SHIFT',
        'e'],
    'F': [
        'SHIFT',
        'f'],
    'G': [
        'SHIFT',
        'g'],
    'H': [
        'SHIFT',
        'h'],
    'I': [
        'SHIFT',
        'i'],
    'J': [
        'SHIFT',
        'j'],
    'K': [
        'SHIFT',
        'k'],
    'L': [
        'SHIFT',
        'l'],
    'M': [
        'SHIFT',
        'm'],
    'N': [
        'SHIFT',
        'n'],
    'O': [
        'SHIFT',
        'o'],
    'P': [
        'SHIFT',
        'p'],
    'R': [
        'SHIFT',
        'r'],
    'S': [
        'SHIFT',
        's'],
    'T': [
        'SHIFT',
        't'],
    'U': [
        'SHIFT',
        'u'],
    'W': [
        'SHIFT',
        'w'],
    'X': [
        'SHIFT',
        'x'],
    'Y': [
        'SHIFT',
        'y'],
    'Z': [
        'SHIFT',
        'z'],
    'V': [
        'SHIFT',
        'v'],
    'Q': [
        'SHIFT',
        'q'],
    '?': [
        'SHIFT',
        '/'],
    '>': [
        'SHIFT',
        '.'],
    '<': [
        'SHIFT',
        ','],
    '"': [
        'SHIFT',
        "'"],
    ':': [
        'SHIFT',
        ';'],
    '|': [
        'SHIFT',
        '\\'],
    '}': [
        'SHIFT',
        ']'],
    '{': [
        'SHIFT',
        '['],
    '+': [
        'SHIFT',
        '='],
    '_': [
        'SHIFT',
        '-'],
    '!': [
        'SHIFT',
        '1'],
    '@': [
        'SHIFT',
        '2'],
    '#': [
        'SHIFT',
        '3'],
    '$': [
        'SHIFT',
        '4'],
    '%': [
        'SHIFT',
        '5'],
    '^': [
        'SHIFT',
        '6'],
    '&': [
        'SHIFT',
        '7'],
    '*': [
        'SHIFT',
        '8'],
    '(': [
        'SHIFT',
        '9'],
    ')': [
        'SHIFT',
        '0'] }
Base = {
    '0': 48,
    '1': 49,
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    '6': 54,
    '7': 55,
    '8': 56,
    '9': 57,
    'a': 65,
    'b': 66,
    'c': 67,
    'd': 68,
    'e': 69,
    'f': 70,
    'g': 71,
    'h': 72,
    'i': 73,
    'j': 74,
    'k': 75,
    'l': 76,
    'm': 77,
    'n': 78,
    'o': 79,
    'p': 80,
    'q': 81,
    'r': 82,
    's': 83,
    't': 84,
    'u': 85,
    'v': 86,
    'w': 87,
    'x': 88,
    'y': 89,
    'z': 90,
    '.': 190,
    '-': 189,
    ',': 188,
    '=': 187,
    '/': 191,
    ';': 186,
    '[': 219,
    ']': 221,
    '\\': 220,
    "'": 222,
    'ALT': 18,
    'TAB': 9,
    'CAPSLOCK': 20,
    'ENTER': 13,
    'BS': 8,
    'CTRL': 17,
    'ESC': 27,
    ' ': 32,
    'END': 35,
    'DOWN': 40,
    'LEFT': 37,
    'UP': 38,
    'RIGHT': 39,
    'SELECT': 41,
    'PRINTSCR': 44,
    'INS': 45,
    'DEL': 46,
    'LWIN': 91,
    'RWIN': 92,
    'LSHIFT': 160,
    'SHIFT': 161,
    'LCTRL': 162,
    'RCTRL': 163,
    'VOLUP': 175,
    'DOLDOWN': 174,
    'NUMLOCK': 144,
    'SCROLL': 145 }
#End of borrowed script