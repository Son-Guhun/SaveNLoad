# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 00:34:46 2018

@author: criow
"""

from distutils.core import setup
import py2exe
 
setup(console=['SaveNLoad.py','autoupdate.py']
          #,options = {'py2exe': {'bundle_files': 1, 'compressed': True}}
          #,zipfile = None
#          ,options={
#                      'py2exe':{
#                              'packages': ['Carbon']}
#                  }
          );

#setup(console=['autoupdate.py']
#          #,options = {'py2exe': {'bundle_files': 1, 'compressed': True}}
#          #,zipfile = None
##          ,options={
##                      'py2exe':{
##                              'packages': ['Carbon']}
##                  }
#          );