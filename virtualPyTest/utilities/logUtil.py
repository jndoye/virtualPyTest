# coding: utf-8
"""
Created on 28 June 2017
@author: N'DOYE Joachim
VirtualTest is a generic hybrid automation testing framework
"""
#############################################################################
# VirtualPyTest - 2017 - AngelCorp.
# Attribution-NonCommercial-ShareAlike 3.0 France (CC BY-NC-SA 3.0 FR) 
# 
# You are free to:
#     Share — copy and redistribute the material in any medium or format
#     Adapt — remix, transform, and build upon the material
#     The licensor cannot revoke these freedoms as long as you follow the license terms.
# 
# Under the following terms:
#     Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
#     NonCommercial — You may not use the material for commercial purposes.
#     ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
#     No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.
# 
# Notices:
#     You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation.
#     No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.
# -----------------------------------------------------
# N'DOYE Joachim
# -----------------------------------------------------
#############################################################################
"""
This file contains the following classes:
    LogUtil
"""    
##############################################################################
# Import modules
##############################################################################
import os
import dominate
from dominate.tags import *
import stormtest.ClientAPI as stormtest  # @UnresolvedImport
#-------------       
# DataUtil
#--------------         
class LogUtil:
    def __init__(self):
        """ The Constructor """
        self.logs = {}
        
    def log(self, msg, newline=True, name=None):
        if not name:
            for _, v in self.logs.iteritems():
                v[2].add(msg)
                if newline:
                    v[2].add(br())
        elif isinstance(name, str):
            self.logs[name][2].add(msg)
            if newline:
                self.logs[name][2].add(br())
        else:
            for _, v in name:
                v[2].add(msg)
                if newline:
                    v[2].add(br())
    
    def initLog(self, name):
        _html = html()
        _head, _body = _html.add(head(title('VirtualPyTestPro')),body())
        self.logs[name] = _html, _head, _body
        
    def getLog(self, name):
        return self.logs[name][0].render()
    
    def saveLog(self, name):
        dirPath = stormtest.GetLogFileDirectory()
        logPath = os.path.join(dirPath, name+".html")
        logFile = open(logPath, 'w')
        logFile.write(self.getLog(name))
        logFile.flush()
        logFile.close()
        logFile = None  
    
    def saveLogs(self):
        for k, _ in self.logs.iteritems():
            self.saveLog(k)