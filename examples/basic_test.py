# coding: utf-8
"""
Created on 28 June 2017
@author: N'DOYE Joachim
Examples of tests to illustrate the basic of VirtualTest 
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

##############################################################################
# Import modules
##############################################################################
import os, sys
testdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(testdir + "\\..")
from virtualPyTest import VirtualTestCase, VirtualTestSuite, VirtualTest

# Main
if __name__ == '__main__':
    #========================
    # TEST CREATION
    #========================
    print "-"*20 + "BEGIN TEST CREATION " + "-"*20
    virtualTest_1 = VirtualTest("virtualTest_1", "home_to_youtube").addStep("step1", "desc", 1, "home/home_to_youtube", "youtube/youtube_logo")
    virtualTest_2 = VirtualTest("virtualTest_2", "home_to_netflix")
    virtualTest_2.addStep("step1", "desc", 1, "vod_title", "vod/title")
    virtualTest_2.addStep("step1", "desc", 1, "barker_vod", "vod/barker")
    virtualTest_3 = VirtualTest("virtualTest_3", "zap").addStep("step1", "desc", 1, "zap_TF1", "live/tf1_logo", None, 2, True)
    virtualTest_1._print()
    virtualTest_2._print()
    virtualTest_3._print()
    print "-"*20 + " END TEST CREATION " + "-"*20
    #========================
    # TEST RUN
    #========================
    print "-"*20 + " BEGIN TEST RUN " + "-"*20
    virtualTest_1.run(False, 2)
    print "-"*20 + " END TEST RUN " + "-"*20
    #========================
    # TESTSUITE CREATION
    #========================
    print "-"*20 + " BEGIN TESTSUITE CREATION " + "-"*20
    # USE CASE 1: Create a VirtualTestSuite with a list of VirtualTest 
    virtualTestSuite_1 = VirtualTestSuite("virtualTestSuite_1", "List of VitualTest", [virtualTest_1, virtualTest_2])
    virtualTestSuite_1._print()
    # USE CASE 2: Create an empty VirtualTestSuite then add a VirtualTest
    virtualTestSuite_2 = VirtualTestSuite("virtualTestSuite_2", "List of VitualTest")
    virtualTestSuite_2.addTest(virtualTest_2)
    virtualTestSuite_2.addTest(virtualTest_1)
    virtualTestSuite_2._print()
    # USE CASE 3: Create a VirtualTestCase with a List of VirtualTest 
    virtualTestSuite_3 = VirtualTestSuite("virtualTestSuite_3", "List of VirtualTestSuite", [virtualTest_2, virtualTest_1])
    virtualTestSuite_3._print()
    print "-"*20 + " END TESTSUITE CREATION " + "-"*20
    #========================
    # TESTSUITE RUN
    #========================
    print "-"*20 + " BEGIN TESTSUITE RUN " + "-"*20
    virtualTestSuite_1.run(False, 2)
    print "-"*20 + " END TESTSUITE RUN " + "-"*20
    #========================
    # TESTCASE CREATION
    #========================
    print "-"*20 + " BEGIN TESTCASE CREATION " + "-"*20
    # USE CASE 1: Create Virtual Test Case without any TestCase
    virtualTestCase_1 = VirtualTestCase("virtualTestCase_1", "description", [virtualTestSuite_2])
    # USE CASE 2: Add test suite
    virtualTestCase_1.addVirtualTestSuite(virtualTestSuite_1) 
    # USE CASE 2: Add usecase
    virtualTestCase_1.addVirtualUseCase("usecase_1", virtualTest_3, None) 
    virtualTestCase_1._print()
    print "-"*20 + " END TESTCASE CREATION " + "-"*20
    #========================
    # TESTCASE RUN
    #========================
    print "-"*20 + " BEGIN TESTCASE RUN " + "-"*20
    virtualTestCase_1.run()
    print "-"*20 + " END TESTCASE RUN " + "-"*20