# coding: utf-8
"""
Created on 28 June 2017
@author: N'DOYE Joachim
VirtualTest is a generic hybrid automation testing framework
"""
#############################################################################
#     VirtualPyTest - 2017 - AngelCorp.
#     Copyright (C) 2017  N'DOYE Joachim
#     Attribution-NonCommercial-ShareAlike 3.0 France (CC BY-NC-SA 3.0 FR) 
# 
#     You are free to:
#     Share — copy and redistribute the material in any medium or format
#     Adapt — remix, transform, and build upon the material
#     The licensor cannot revoke these freedoms as long as you follow the license terms.
# 
#     Under the following terms:
#     Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
#     NonCommercial — You may not use the material for commercial purposes.
#     ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
#     No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.
# 
#     Notices:
#     You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation.
#     No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.
#############################################################################
"""
This file contains the following classes:
    VirtualInterfacePro
    VirtualForStepPro
    VirtualIfStepPro
"""    
##############################################################################
# Import modules
##############################################################################
from virtualPyTest import VirtualTest, VirtualStep, VirtualCondition, VirtualAction, VirtualVerification, VirtualInterface
from utilities.dataUtil import DataUtil
from utilities.logUtil import LogUtil
from utilities.reportUtil import ReportUtil
from virtualPyTest import setInterface, getInterface
#-------------       
# Virtual Interface
#--------------         
class VirtualInterfacePro(VirtualInterface):
    def __init__(self, name, stb, resource_dir):
        """Initialization of a VirtualInterfacePro"""
        VirtualInterface.__init__(self, name)
        self.logUtil = LogUtil()
        self.dataUtil = DataUtil()
        self.reportUtil = ReportUtil()
        self.stb = stb
        self.resource_dir = resource_dir
    
    def log(self, msg, newline=True, log_name=None):
        self.logUtil.log(msg, newline, log_name)
    
    def initLog(self, name):
        return self.logUtil.initLog(name)
        
    def getLog(self, name):
        return self.logUtil.getLog(name)
        
    def saveLog(self, name):
        self.logUtil.saveLog(name)

    def saveLogs(self):
        self.logUtil.saveLogs()
#-------------       
# Virtual Test Plan
# A TestPlan contains the integrality of the steps, tests, test suites, test cases and usecases  
#--------------         
class VirtualTestPlanPro:
    def __init__(self, name, interface, src=None):
        """Initialization of a VirtualTestPlan"""
        self.name = name
        self.src = src
        self.data = None
        self.dataUtil = interface.dataUtil
        self.step_list = {}
        self.test_list = {}
        self.usecase_list = {}
        self.testsuite_list = {}
        self.testcase_list = {}
        self.spy_list = None
        setInterface(interface)
        if src:
            self.initTestPlan()
    
    def createTestPlan(self):
        pass
            
    def initTestPlan(self):
        if ".txt" in self.src:
            self.getTestPlanFromTXT(self.src)
            self.createTestPlan()
        elif ".csv" in self.src:
            self.getTestPlanFromCSV(self.src)
            self.createTestPlan()
        elif "://" in self.src:
            self.getTestPlanFromREST(self.src)
            self.createTestPlan()
            
    def getTestPlanFromCSV(self, path):
        self.data = self.dataUtil.loadFile(path)
    
    def getTestPlanFromTXT(self, path):
        self.data = self.dataUtil.loadFile(path)
        
    def getTestPlanFromREST(self, url):
        pass
    
    def add(self, object):
        if isinstance(object, (VirtualStep, VirtualIfStepPro, VirtualForStepPro)):
            self.step_list[object.name] = object
        elif isinstance(object, VirtualTest):
            self.test_list[object.name] = object
        elif isinstance(object, VirtualTestSuite):
            self.testsuite_list[object.name] = object
        elif isinstance(object, VirtualTestCase):
            self.testcase_list[object.name] = object
        return object
    
    def getStep(self, name):
        return self.step_list[name]
    
    def getTest(self, name):
        return self.test_list[name]
    
    def getTestSuite(self, name):
        return self.testsuite_list[name]
    
    def getTestCase(self, name):
        return self.testcase_list[name]
    
    def run(self, debug=False, max_iteration=None, interface=None, spy_list=None):
        if not spy_list and self.spy_list:
            spy_list = self.spy_list
        for k, v in self.test_list.iteritems():
            v.run(debug, max_iteration, interface, spy_list)
        for k, v in self.testsuite_list.iteritems():
            v.run(debug, max_iteration, interface, spy_list)
        for k, v in self.testcase_list.iteritems():
            v.run(debug, max_iteration, interface, spy_list)

    def runWithTags(self, tags, debug=False, max_iteration=None, interface=None, spy_list=None):
        # Run test, testsuite or testase with tags
        if not spy_list and self.spy_list:
            spy_list = self.spy_list
        for k, v in self.test_list.iteritems():
            if [i for i in v.tags if i in tags]!=[]:
                v.run(debug, max_iteration, interface, spy_list)
        for k, v in self.testsuite_list.iteritems():
            if [i for i in v.tags if i in tags]!=[]:
                v.run(debug, max_iteration, interface, spy_list)
        for k, v in self.testcase_list.iteritems():
            if [i for i in v.tags if i in tags]!=[]:
                v.run(debug, max_iteration, interface, spy_list)

    
#-------------       
# Virtual If Step
# If condition Then Action and Verification Elif Else  
#--------------         
class VirtualIfStepPro:
    def __init__(self, if_type, parent, name, description, max_iteration, condition, action, verification, wait_before_verification=0, verification_retry=0, pass_on_no_match=False):
        """Initialization of a VirtualIfTest"""
        self.if_type = if_type  # if, elif or else
        self.parent = parent
        self.name = name
        self.description = description
        self.max_iteration = max_iteration
        self.condition = None 
        if condition != None:
            # condition isNone for else case
            self.condition = VirtualCondition(condition)
        self.step = VirtualStep(name, description, max_iteration, action, verification, wait_before_verification, verification_retry, pass_on_no_match)
    
    def execute(self, debug=False, interface=None):
            if self.parent == None or self.parent.condition != None and not self.parent.condition.result == None and not self.parent.condition.result:     
                if self.condition == None or interface.verifyCondition(self.condition):
                    print self.step
                    for i in range(0, self.max_iteration):
                        self.step.execute(debug, interface)
                
    def _print(self):
        """Print VirtualIfStepPro"""
        print "{1}, {0}".format(self.condition, self.step)
    
#-------------       
# Virtual For Step
# Action repeatedx times then Verification
#--------------         
class VirtualForStepPro(VirtualStep):
    def __init__(self, name, description, max_iteration, action, action_max_iteration, verification, wait_before_verification=0, verification_retry=0, pass_on_no_match=False):
        """Initialization of a VirtualSimpleTest"""
        self.name = name
        self.description = description
        self.max_iteration = max_iteration
        self.action_max_iteration = action_max_iteration
        self.action = VirtualAction(self, action)
        self.verification = VirtualVerification(self, verification, wait_before_verification, verification_retry, pass_on_no_match)
        
    def execute(self, debug=False, interface=None):
        for i in range(0, self.max_iteration):
            for _ in range(0, self.action_max_iteration):
                interface.executeAction(self.action)
            if self.verification.verification:
                interface.executeVerification(self.verification)
    
    def _print(self):
        """Print VirtualStep"""
        print "{0} - action: {1} repeated {2}, verification: {3}".format(self.name, self.action, self.action_max_iteration, self.verification)
        
    def  __str__(self):
        """Module called when converting the object to string"""
        return "{0} - action: {1} repeated {2}, verification: {2}".format(self.name, self.action, self.action_max_iteration, self.verification)
#-------------       
# Virtual Test
# Action and Verification
#--------------         
class VirtualTestPro(VirtualTest):
    def __init__(self, name, description, usecase=None, max_iteration=1, test_on_debug=True, onFail=None, tags=[]):
        VirtualTest.__init__(self, name, description, usecase, max_iteration, test_on_debug, onFail)
        self.tags = tags
        
    def run(self, debug=False, max_iteration=None, interface=None, spy_list=None):
        self.status = "running"
        self.pass_result = 0
        self.result = None
        self.iteration = 0
        if self.step_list == []:
            raise "Error: This test has no step to run !"
        tmp = self.max_iteration
        if max_iteration:
            self.max_iteration = max_iteration
        if self.checkVirtualTest(debug):
            interface = getInterface(interface)
            spy(self, "running", spy_list)
            print "* TEST RUN: {0} - {1} iteration(s)".format(self.name, self.max_iteration)
            for i in range(0, self.max_iteration):
                print "---------- {0} iteration ----------".format(i + 1)
                self.usecase.begin(debug, interface)
                for step in self.step_list:
                    step.execute(debug, interface)
                    self.updateTestResult(step)
                if self.onFail and not self.result:
                    print "On Fail:"
                    spy(self, "on_fail", spy_list)
                    self.onFail.run(debug, interface)
                self.usecase.end(debug, interface)
        self.max_iteration = tmp
        self.status = "complete"
        spy(self, "complete", spy_list)
       
    def add(self, object):
         if isinstance(object, (VirtualStep, VirtualIfStepPro, VirtualForStepPro)):
            self.step_list.append(object)
         elif isinstance(object, VirtualUseCase):
            self.usecase_list.append(object)
         return self
      
    def addTags(self, tags):
        if isinstance(tags, str):
            self.tags.append(tags)
        else:
            self.tags = self.tags + tags
            
    def addForStep(self, name, description, max_iteration, action, action_max_iteration, verification, wait_before_verification=0, verification_retry=0, pass_on_no_match=False):
        self.step_list.append(VirtualForStepPro(name, description, max_iteration, action, action_max_iteration, verification, wait_before_verification, verification_retry, pass_on_no_match))
        return self
    
    def addIfStep(self, name, description, max_iteration, condition, action, verification, wait_before_verification=0, verification_retry=0, pass_on_no_match=False):
        self.step_list.append(VirtualIfStepPro("if", None, name, description, max_iteration, condition, action, verification, wait_before_verification, verification_retry, pass_on_no_match))
        return self
    
    def addElifStep(self, name, description, max_iteration, condition, action, verification, wait_before_verification=0, verification_retry=0, pass_on_no_match=False):
        if not isinstance(self.step_list[-1], VirtualIfStepPro):
            raise "Error: Elif step must follow if Step"
        self.step_list.append(VirtualIfStepPro("elif", self.step_list[-1], name, description, max_iteration, condition, action, verification, wait_before_verification, verification_retry, pass_on_no_match))
        return self
    
    def addElseStep(self, name, description, max_iteration, action, verification, wait_before_verification=0, verification_retry=0, pass_on_no_match=False):
        condition = None
        if not isinstance(self.step_list[-1], VirtualIfStepPro):
            raise "Error: Else step must follow if Step"
        self.step_list.append(VirtualIfStepPro("else", self.step_list[-1], name, description, max_iteration, condition, action, verification, wait_before_verification, verification_retry, pass_on_no_match))
        return self
    
    def updateTestResult(self, step):
        if isinstance(step, VirtualIfStepPro) and step.step.verification.result or isinstance(step, VirtualStep) and step.verification.result:
            self.pass_result += 1
        if self.iteration == self.max_iteration - 1:
            self.result = self.pass_result == self.max_iteration  
            
def spy(self, status, spy_list):
    # spy_list contains tuple with a log to write and a function to spy
    if spy_list:
        if isinstance(spy_list, tuple):  # To handle single spy tuple
            spy_list = [spy_list]
        for log_name, spy in spy_list:
            spy(self, status, log_name)
         
