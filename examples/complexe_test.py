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
from virtualPyTestPro import VirtualTestPro
from virtualPyTest import VirtualTestCase, VirtualTestSuite

# Main
if __name__ == '__main__':
    #========================
    # TEST CREATION
    #========================
    print "-"*20 + "BEGIN TEST CREATION " + "-"*20
    virtualTest_2 = VirtualTestPro("virtualTest_2", "VirtualTest - home_to_netflix", None, 1, True)
    virtualTest_2.addIfStep("ifStep", "desc", 1, False, "home/home_to_netflix", "netflix/netflix_logo")
    virtualTest_2.addElifStep("elifStep", "desc",  1, False, "home/home_to_youtube", "youtube/youtube_logo") 
    virtualTest_2.addElseStep("elseStep", "desc", 1, "home/home_to_youtube", "youtube/youtube_logo")
    virtualTest_2._print()
    virtualTest_onFail = VirtualTestPro("virtualTest_onFail", "on Fail").addStep("screenshot", "desc", 1,  "screenshot")
    virtualTest_3 = VirtualTestPro("virtualTest_3", "VirtualTest - home_to_youtube", None, 1, True, virtualTest_onFail)
    virtualTest_3.addForStep("step1", "desc", 1, "home/home_to_youtube", 3, "youtube/youtube_logo", 0, 0, True)
    virtualTest_3._print()
    print "-"*20 + " END TEST CREATION " + "-"*20
    #========================
    # TEST RUN
    #========================
    print "-"*20 + " BEGIN TEST RUN " + "-"*20
    virtualTest_2.run()
    virtualTest_3.run()
    print "-"*20 + " END TEST RUN " + "-"*20
    
