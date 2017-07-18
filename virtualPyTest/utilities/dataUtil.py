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
This file contains the following method:
    connectToMongoDb
    loadFile
"""    
#-------------       
# DataUtil
#--------------         
class DataUtil:
    #-------------       
    # Connect To MongoDb
    #-------------- 
    def connectToMongoDb(self, url, login, password):
        print "Connect to mongo db - url:{0}, login:{1}, password:{2}".format(url, login, password)
    #-------------       
    # Load File
    #--------------         
    def loadFile(self, path):
        file = open(path, "r") 
        content = file.readlines()
        file.close()
        return content
        