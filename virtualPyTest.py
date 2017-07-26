# coding: utf-8
"""
Created on 28 June 2017
@author: N'DOYE Joachim
VirtualTest is a generic hybrid automation testing framework
"""
#############################################################################
#     VirtualPyTest - 2017 - AngelCorp.
#     Copyright (C) 2017  N'DOYE Joachim
#     GNU General Public License version 3
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################
# TODO: name must be unique to get elt from TestPlan dict
"""
This file contains the following classes:
    VirtualInterface
    VirtualUseCase
    VirtualTestCase
    VirtualTestSuite
    VirtualTest
    VirtualStep
    VirtualAction
    VirtualVerification
    VirtualCondition
"""    
#-------------       
# Virtual Interface
#--------------         
class VirtualInterface:
    def __init__(self, name):
        """Initialization of a VirtualInterface"""
        self.name = name
        self.isDefault = True
        
    def executeAction(self, action):
        print "Interface executeAction: {0}".format(action)
        return True
    
    def executeVerification(self, verification):
        print "Interface executeVerification: {0}".format(verification)
        verification.result = True
        return True
        
    def verifyCondition(self, condition):
        print "Interface verifyCondition: {0}".format(condition)
        condition.result = True
        return True
    
#-------------       
# Virtual Action
#--------------         
class VirtualUseCase:
    def __init__(self, name, startCase=None, endCase=None):
        """Initialization of a VirtualUseCase"""
        self.name = name
        self.startCase = startCase
        self.endCase = endCase
        
    def begin(self, debug=False, interface=None):
        if self.startCase:
            print "Begin usecase '{0}'".format(self.name)
            self.startCase.run(debug, 1, interface)
    
    def end(self, debug=False, interface=None):
        if self.endCase:
            print "End usecase '{0}'".format(self.name)
            self.endCase.run(debug, 1, interface)
    
    def  __str__(self):
        """Module called when converting the object to string"""
        if self.startCase:
            return "'{0}'".format(self.name)
        else:
            return "None"

#-------------       
# Virtual Action
#--------------         
class VirtualAction:
    def __init__(self, parent, action):
        """Initialization of a VirtualAction"""
        self.parent = parent  # Parent VirtualTest
        self.action = action
        self.action_type = None  # string or list representation of KEYPRESS or REBOOT
        
    def execute(self, debug=False, interface=None):
        if self.action and self.action != []:
            interface.executeAction(self.action)
            
    
    def  __str__(self):
        """Module called when converting the object to string"""
        return "{0}".format(self.action)
#-------------       
# Virtual Verification
#--------------         
class VirtualVerification():
    def __init__(self, parent, verification, wait_before_verification=0, retry_max=0, pass_on_no_match=False):
        """Initialization of a VirtualVerification"""
        self.parent = parent  # Parent VirtualTest
        self.verification = verification
        self.wait_before_verification = wait_before_verification
        self.pass_result = 0
        self.result = None
        self.retry = 0
        self.retry_max = int(retry_max)
        self.capture = []
        self.pass_on_no_match = bool(pass_on_no_match)
    
    def execute(self, debug=False, interface=None):
        if self.retry_max == 0:
            self.retry_max = 1
        self.result = None
        self.retry = 0
        while not self.result and self.retry < self.retry_max:
            interface = getInterface(interface)
            self.result = interface.executeVerification(self)
            if self.pass_on_no_match and not self.result:
                self.result = True
            print "Verification '{0}' executed".format(self.result)
            self.retry += 1
    
    def getVerificationResult(self, debug=False):
        if self.parent.status == "complete":
            return "Verification: {0} {1} after {2} retry".format(self.verification, getPassFail(self.result), self.pass_result)
        else:
            return "VirtualTest: '{0}' has not been run".format(self.parent.name)  
            
    def  __str__(self):
        """Module called when converting the objectto string"""
        if self.verification:
            return "wait {1}s then check '{0}'".format(self.verification, self.wait_before_verification)
        else:
            return None
#-------------       
# Virtual Condition
#--------------         
class VirtualCondition:
    def __init__(self, condition):
        """Initialization of a VirtualCondition"""
        self.condition = condition
        self.result = None

    def verify(self, debug=False, interface=None):
        interface = getInterface(interface)
        self.result = interface.verifyCondition(self.condition)
        return self.result
    
    def  __str__(self):
        """Module called when converting the object to string"""
        return "Condition: '{0}' , Result: '{1}'".format(self.condition, self.result)

#-------------       
# Virtual Step
# Action and Verification
#--------------         
class VirtualStep:
    def __init__(self, name, description, max_iteration, action, verification=None, wait_before_verification=0, verification_retry=0, pass_on_no_match=False):
        """Initialization of a VirtualSimpleTest"""
        self.name = name
        self.description = description
        self.max_iteration = max_iteration
        self.action = VirtualAction(self, action)
        self.verification = VirtualVerification(self, verification, wait_before_verification, verification_retry, pass_on_no_match)
        
    def execute(self, debug=False, interface=None):
        print "{0}:".format(self.name)
        for _ in range(0, self.max_iteration):
            if self.action.action and self.action.action != []:
                interface.executeAction(self.action)
            if self.verification.verification:
                interface.executeVerification(self.verification)
                self.result = self.verification.result
                
    def getVerificationCapture(self):
        return self.verification.capture
        
    def _print(self):
        """Print VirtualStep"""
        print "{0} (x{3}) - action: {1}, verification: {2}".format(self.name, self.action, self.verification, self.max_iteration)
        
    def  __str__(self):
        """Module called when converting the object to string"""
        return "{0} (x{3}) - action: {1}, verification: {2}".format(self.name, self.action, self.verification, self.max_iteration)
#-------------       
# Virtual Test
# Action and Verification
#--------------         
class VirtualTest:
    def __init__(self, name, description, max_iteration=1, retry=0, test_on_debug=True, onFail=[], stopTestOnStepFail=False, passIfAllStepsPass=True):
        """Initialization of a VirtualTest"""
        self.status = 'init'
        self.parent = None
        self.name = name
        self.description = description
        self.test_on_debug = test_on_debug
        self.pass_result = 0
        self.result = None
        self.onFail = onFail
        self.stopTestOnStepFail = stopTestOnStepFail
        self.report = ""
        self.step_list = []
        self.usecase = VirtualUseCase(None)
        self.step_by_step = 0
        self.max_iteration = max_iteration
        self.retry = retry
        self.passIfAllStepsPass = passIfAllStepsPass
    
    def addUseCase(self, usecase, max_iteration, action, verification=None, wait_before_verification=0, verification_retry=0, pass_on_no_match=False):
        if isinstance(usecase, VirtualUseCase):
            self.usecase = usecase
        else:
            self.usecase = VirtualUseCase(*list)
            return self
            
    def addStep(self, name, description, max_iteration, action, verification=None, wait_before_verification=0, verification_retry=0, pass_on_no_match=False):
        self.step_list.append(VirtualStep(name, description, max_iteration, action, verification, wait_before_verification, verification_retry, pass_on_no_match))
        return self

    def getStep(self, step_name):
        for step in self.step_list:
            if step.name == step_name:
                return step
        print "Step {0} not found".format(step_name)
        return None
    
    def addOnFail(self, on_fail):
        if isinstance(on_fail, (VirtualTest, VirtualStep)):
            self.onFail = on_fail
        else:
            raise "Error: addOnFail parameter must be a VirtualTest or VirtualStep "
        return self
                
    def checkVirtualTest(self, debug):
        # Check test_on_debug
        if debug and not self.test_on_debug:
            print "The test '{0}' will not be tested because test_on_debug is False".format(self.action)
            return False
        return True
    
    def updateTestResult(self, step):
        if isinstance(step, VirtualStep) and step.verification.result:
            self.pass_result += 1
        if self.iteration == self.max_iteration - 1:
            self.result = self.pass_result == self.max_iteration    
    
    def runNextStep(self, debug=False, max_iteration=None, interface=None):
        if self.step_by_step == len(self.step_list):
            print "Last step already executed.\n Starting back from first step."
            step_by_step = 0
        self.run(debug, max_iteration, interface, self.step_by_step)
        self.step_by_step += 1
            
    def run(self, debug=False, max_iteration=None, retry=0, interface=None, step_by_step=-1):
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
            print "* TEST RUN: {0} - {1} iteration(s)".format(self.name, self.max_iteration)
            for i in range(0, self.max_iteration):
                print "---------- {0} iteration ----------".format(i + 1)
                self.usecase.begin(debug, interface)
                if step_by_step >= 0:
                    step = self.step_list[step_by_step]
                    step.execute(debug, interface)
                    self.updateTestResult(step)
                else:
                    for step in self.step_list:
                        step.execute(debug, interface)
                        self.updateTestResult(step)
                        if step.result and not self.passIfAllStepsPass:
                            print "Test '{0}' pass since step {1} passed, following steps will be skipped".format(self.name, step.name)
                            break;
                        elif self.stopTestOnStepFail and not step.result:
                            print "Test '{0}' is stopped because step '{1}' failed".format(self.name, step.name)
                            break;
                
                if not self.result:
                    if retry == 0:
                        if self.onFail:
                            print "On Fail"
                            for onFail in self.onFail:
                                if isinstance(onFail, VirtualTest):
                                    for step in onFail.step_list:
                                        step.execute(debug, interface)
                                else:
                                    onFail.execute(debug, interface)
                    else:
                        if self.onFail:
                            print "On Fail"
                            onFail = self.onFail[(self.retry - retry) % len(self.onFail)]
                            if isinstance(onFail, VirtualTest):
                                for step in onFail.step_list:
                                    step.execute(debug, interface)
                            else:
                                onFail.execute(debug, interface)
                        print "retrying test '{0}'".format(self.name)
                        self.run(debug, max_iteration, retry - 1, interface, step_by_step)
                        
                self.usecase.end(debug, interface)
        self.max_iteration = tmp
        self.status = "complete"
        return self.result
    
    def getTestResult(self, debug=False):
        if self.status == "complete":
            return "VirtualTest: '{0}' - {1} with {2}/{3} iteration(s)".format(self.name, getPassFail(self.result), self.iteration, self.max_iteration)
        else:
            return "VirtualTest: '{0}' has not been run".format(self.name)
            
    def  __str__(self):
        """Module called when converting the objectto string"""
        return "VirtualTest '{0}'".format(self.name)
    
    def _print(self):
        """Print VirtualTest"""
        print "*" * 50
        print "VirtualTest: {0}".format(self.name)
        print "*" * 50
        print "description: {0}".format(self.description)
        print "usecase: {0}".format(self.usecase)
        print "Number of steps: {0}".format(len(self.step_list))
        self._printSteps()
        print "test_on_debug: {0}".format(self.test_on_debug)
    
    def _printSteps(self):
        """Print VirtualTest Steps"""
        for step in self.step_list:
            step._print()
#-------------
# Virtual Test List
# A list of Virtual Test
#-------------- 
class VirtualTestSuite:
    def __init__(self, name, description="description", test_list=None, usecase=None, max_iteration=1, test_on_debug=True, onFail=None):
        """Initialization of a VirtualTestSuite"""
        self.status = "init"
        self.parent = None
        self.name = name
        self.description = description
        self.result = None  
        self.test_on_debug = test_on_debug
        self.max_iteration = max_iteration
        self.onFail = onFail
        self.initTestList(test_list)
        self.initUseCase(usecase)
         
    def initTestList(self, test_list):
        if not test_list:
            self.test_list = []
        else:
            self.test_list = test_list
        
    def initUseCase(self, usecase):
        if not usecase:
            self.usecase = VirtualUseCase(None)
        elif isinstance(usecase, VirtualUseCase):
            self.usecase = usecase
        else:
            self.usecase = VirtualUseCase(*list)
        
    def addTest(self, virtualTest):
        # TODO append a clone 
        virtualTest.parent = self
        self.test_list.append(virtualTest)
    
    def run(self, debug=False, max_iteration=None, interface=None):
        self.status = "running"
        self.result = None 
        self.iteration = 0
        tmp = self.max_iteration
        if max_iteration:
            self.max_iteration = max_iteration
        print "** TESTSUITE RUN: {0}".format(self.name)
        self.usecase.begin(debug)
        for _ in range(0, self.max_iteration):
            for test in self.test_list:
                test.run(debug, test.max_iteration, interface)
            
            if self.onFail and not self.result:
                self.onFail.execute(debug, self.onFail.max_iteration, interface)
        self.usecase.end(debug)
        self.max_iteration = tmp
        self.status = "complete"

    def getTestSuiteResult(self, debug=False):
        if self.status == "complete":
            result = "VirtualTestSuite - '{0}':".format(self.name)
            for test in self.test_list:
                result += "\n" + test.getTestResult(debug) 
            return result
        else:
            return "VirtualTestSuite: '{0}' has not been run".format(self.name)
        
    def getTestNames(self):
        """Get the names of the VirtualTest in test_list"""
        test_names = []
        for test in self.test_list:
            test_names.append(test.name)
        return test_names
        
    def  __str__(self):
        """Module called when converting the objectto string"""
        return "VirtualTestSuite: {0}".format(self.name)
    
    def _print(self):
        """Print the arguments of VirtualTestSuite"""
        print "*" * 50
        print "VirtualTestSuite: " + self.name + "   "
        print "*" * 50
        print "description: ", self.description
        print "test_list: ", self.getTestNames()
        print "usecase: ", self.usecase
        print "test_on_debug: ", self.test_on_debug 
#-------------
# Virtual Test Case
# A list of Virtual Test Suite executed in several usecases
# For instance running some zapping with Recording and then with a Picture in Picture activated
#-------------- 
class VirtualTestCase:
    def __init__(self, name, description="description", test_suite_list=[], usecase_list=[], max_iteration=1, test_on_debug=True, onFail=None):
        """Initialization of a VirtualTestSuite"""
        self.status = "init"
        self.name = name
        self.description = description
        self.result = None  
        self.onFail = onFail
        self.max_iteration = int (max_iteration)
        self.test_on_debug = test_on_debug
        self.usecase_list = usecase_list
        self.test_suite_list = test_suite_list
         
    def addVirtualTestSuite(self, virtualTestSuite):
        virtualTestSuite.parent = self
        self.test_suite_list.append(virtualTestSuite)
    
    def addVirtualUseCase(self, name, begin, end):
        self.usecase_list.append(VirtualUseCase(name, begin, end))
    
    def run(self, debug=False, max_iteration=None , interface=None):
        self.status = "running"
        self.result = None  
        print "** TESTCASE RUN: {0}".format(self.name)
        tmp = self.max_iteration
        if max_iteration:
            self.max_iteration = max_iteration
        for _ in range(0, self.max_iteration):
            interface = getInterface(interface)
            if self.usecase_list:
                for usecase in self.usecase_list:
                    usecase.begin(debug, interface)
                    self.runTestSuite(debug, interface)
                    if self.onFail and not self.result:
                        self.onFail.execute(debug, interface)
                    usecase.end(debug, interface)
            else:
                self.runTestSuite(debug, interface)
                if self.onFail and not self.result:
                        self.onFail.execute(debug, interface)
        self.max_iteration = tmp
        self.status = "complete"
    
    def runTestSuite(self, debug=None, interface=None):
        for test_suite in self.test_suite_list:
            test_suite.run(debug)
        
    def getTestCaseResult(self, debug=False):
        if self.status == "complete":
            result = "VirtualTestCase - '{0}':".format(self.name)
            if self.usecase_list:
                for usecase in self.usecase_list:
                    usecase_name, test_before_usecase, test_after_usecase = usecase
                    result += "\n\n** UseCase '{0}': {1} - {2} **".format(usecase_name, test_before_usecase.name, test_after_usecase.name)
                    for test_suite in self.test_suite_list:
                        result += "\n" + test_suite.getTestSuiteResult(debug)
                
            else:
                for test_suite in self.test_suite_list:
                    result += "\n\n" + test_suite.getTestSuiteResult(debug)
            return result
        else:
            return "VirtualTestCase: '{0}' has not been run".format(self.name)
        
    def getTestSuiteNames(self):
        """Get the names of the TestSuite in test_suite_list"""
        test_suite_names = []
        for test_suite in self.test_suite_list:
            test_suite_names.append(test_suite.name)
        return test_suite_names
    
    def getUseCaseNames(self):
        """Get the names of the UseCase in usecase_list"""
        usecase_names = []
        for usecase in self.usecase_list:
            usecase_names.append(usecase.name)
        return usecase_names
        
    def  __str__(self):
        """Module called when converting the objectto string"""
        return "VirtualTestCase: {0}".format(self.name)
    
    def _print(self):
        """Print the arguments of VirtualTestCase"""
        print "*" * 50
        print "VirtualTestCase: " + self.name + "   "
        print "*" * 50
        print "description: ", self.description
        print "test_suite_list: ", self.getTestSuiteNames()
        print "test_case_list: ", self.getUseCaseNames()
        print "test_on_debug: ", self.test_on_debug        
#-------------       
# Get Interface
#-------------- 
def getInterface(interface):
    """
    Description:
        Return either the interface given or the default_interface
    """
    global default_interface
    if not interface:
        if default_interface.isDefault:
            print "-"*55
            print "!!! WARNING: YOU ARE USING THE DEFAULT INTERFACE !!!"
            print "-"*55
        return default_interface
    return interface
#-------------       
# Set Interface
#-------------- 
def setInterface(interface):
    """
    Description:
        Setthe default interface
    """
    global default_interface
    if interface:
        default_interface = interface
        default_interface.isDefault = False
    else:
       default_interface = VirtualInterface("default_interface")
    return default_interface

default_interface = setInterface(None)
