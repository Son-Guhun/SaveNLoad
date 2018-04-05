# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 00:42:48 2018

This module provides an API to read Save/Load saves and to send them as chat
messages in-game.

@author: criow
"""

import time
from win32api import keybd_event
import random
import win32gui

from urllib2 import URLError

from py2exeUtils import ConvertPath
from globalVariables import GITHUB_USERREPO

import cloud

import os

class FileName:
    def __init__(self,filePath):
        if not os.path.isdir(filePath):
            self.path = filePath
        else:
            self.path = ''
    
    def read(self,*args):
        with open(self.path,'r') as f:
            content = f.read(*args)
        return content
    
    def readlines(self):
        with open(self.path,'r') as f:
            content = f.readlines()
        return content
        

class Folder:
    def __init__(self,folderPath):
        self.path = ConvertPath(folderPath)
        if os.path.exists(folderPath):
            list_ = os.listdir(self.path)
            self.files ={}
            for file_ in list_:
                self.files[file_] = FileName(self.path+file_) 
        else:
            self.files = []
            
class Save:
    
    _TYPES = {'local' : Folder, 
              'github' : cloud.GitHubFolder if GITHUB_USERREPO else None}
    
    def __init__(self,savesPath,saveName):
        self.name = saveName       
        for saveType in Save._TYPES.keys():
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
        
    def getSize(self):
        try:
            self.size = int(self.folder.files['size.txt'].read()[69:-43])
        except (IOError,URLError):
            self.size = 0
        return self.size
    
    def getVersion(self):
        try:
            self.version = int(self.folder.files['version.txt'].read()[69:-43])
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
            saveData1 = self.folder.files[number+'.txt'].readlines()[2:-5]
            saveData = [ x[16:-4] for x in saveData1]
        else:
            saveData = self.folder.files[number+'.txt'].read()[69:-43]
            saveData = saveData.split("\\\\n")
        return saveData
    
    def loadData(self,speed,waitTime):
        """
        Retrives the Save's data from the saves directory. Then all the data is typed
        automatically and sent as chat messages to be parsed in-game.
        """
        time.sleep(waitTime)
        SendChatMessage('-load ini',speed=speed)
        time.sleep(0.5)
        for x in range(0,self.size):        
            try:
                if not TypeSaveData(self._readData(str(x)),speed):
                    print 'Warcraft III window not in focus. Abort.'
                    return
            except (IOError,URLError) :
                print "SaveID:", self.name, "file number",x,"could not be read."
        time.sleep(0.5)
        SendChatMessage('-load end',speed=speed)

def GetCurWindowText():
    	return  win32gui.GetWindowText(win32gui.GetForegroundWindow());  

#Functions to Parse WC3 text files
def SendChatMessage(message,speed):
    """
    Send a chat message in Warcraft III by typing ENTER + MESSAGE + ENTER
    """
    Press('ENTER')
    Write(message,speed)
    Press('ENTER')

def TypeSaveData(saveData,speed):
    """
    Recieves a list of strings. Sends each string as a chat message in-game.
    
    Returns false if the WC3 window is not in focus while typing.
    Returns true upon successfully finishing the typing routine.
    """
    for unitData in saveData:
        if GetCurWindowText() == "Warcraft III":
            SendChatMessage(unitData,speed=speed)
        else:
            return False
    return True

#Keypress Script
#Special Thanks to Piotr Dabkowski (stackoverflow user) for this script
#http://stackoverflow.com/questions/14076207/simulating-a-key-press-event-in-python-2-7
def KeyUp(Key):
    """Releases a key given an integer."""
    if GetCurWindowText() != "Warcraft III":
        return
    keybd_event(Key, 0, 2, 0)


def KeyDown(Key):
    """Presses down a key given an integer."""
    if GetCurWindowText() != "Warcraft III":
        return
    keybd_event(Key, 0, 1, 0)


def Press(Key, speed=1):
    """Presses down then releases a key given a string"""
    rest_time = 0.05/speed
    if Key in Base:
        Key = Base[Key]
        KeyDown(Key)
        time.sleep(rest_time)
        KeyUp(Key)
        return True
    if Key in Combs:
        KeyDown(Base[Combs[Key][0]])
        time.sleep(rest_time)
        KeyDown(Base[Combs[Key][1]])
        time.sleep(rest_time)
        KeyUp(Base[Combs[Key][1]])
        time.sleep(rest_time)
        KeyUp(Base[Combs[Key][0]])
        return True
    return False


def Write(Str, speed = 1):
    """Types a string of letters"""
    for s in Str:
        Press(s, speed)
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