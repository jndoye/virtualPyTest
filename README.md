# virtualPyTest an AWESOMATION TOOL
N'DOYE JOACHIM

### Introduction
VirtualPyTest is a Generic Test Automation Framework in python distributed under the GNU_V3 license.
VirtualPyTest is a Hybrid framework, usig data driven and keyword mechanisms.
With VirtualPyTest you will reduce the time you spend managing, executing and maintaining your code. 


### Philosophy
VirtualPyTest was built to meet test automation needs according to a philosophy outlined by the following three tenets:
   * Test automation must be simple and elegant.
   * You should be able to use the same code regardless of the    
     system under test.
   * Do not reinvent the wheel! Use what is already there.


### Design
VirtualPyTest is simply a one file python library. It organizes your code with Step, Test, Test Suite, Test Case and Use Case objects. After defining a Test Plan in a separate file, you can run a Test, a Test Suite or a Test Case statically or dynamically. All of your specific code logic is managed within an interface that will configure your testing tool, specify how to interpret Action and Verification, instantiate your log, reporting and data process.
With VirtualPyTest you framework can be as light as 5 python files! 


### Concepts
  * A “Step” is an “Action” and a “Verification”.
  * A “Test” is a list of “Step”.
  * A “Use Case” is a combination of “Test”
  * A “Test Suite” is a list of “Test”.
  * A “Test Case” is a list of “Test Suite”.
  * A “Test Plan” represents your entire test strategy.
  * “Step”, “Test”, “Test Suite” and “Test Case” can be   
   iterated multiple times.
  * “Test”, “Test Suite” and “Test Case” can be run with 
   different “Use Case”.


### Why VirtualPyTest?
Everybody dreams to automate its testing but very few succeed!
VirtualPyTest helps you to outsource your test creation and maintenance to tiers companies and keep you core code internally by:
  * Separating your code from your data.
  * Diminishing the number of files to code and maintain.
  * By being Easy and Simple to use.


### Example of code

##### YourTest.py
```sh
virtualTest_1 = VirtualTest("Channel+", "Tune to next channel")
virtualTest_1.addStep("step1", "Tune to channel 1", 1, "home/home_to_channel_1", "live/logo/channe_1")
virtualTest_1.addStep("step2", "Channel+", 5, "Channel+, "live/logo/channe_6")
virtualTest.run()
```

##### VirtualPyTest.py
```sh
VirtualTest(self, name, description, usecase=None, max_iteration=1, test_on_debug=True, onFail=None)
addStep(self, name, description, max_iteration, action, verification=None, wait_before_verification=0, verification_retry=0, pass_on_no_match=False)
```

##### Interface.py
```sh
def executeAction(self, action):
 print "Interface executeAction: {0}".format(action)
 return True
    
def executeVerification(self, verification):
 print "Interface executeVerification: {0}".format(verification)
 verification.result = True
 return True
```