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
    ReportUtil
""" 
##############################################################################
# Import modules
##############################################################################
import stormtest.ClientAPI as stormtest  # @UnresolvedImport   
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import types
import os, sys
import zipfile
#-------------       
# DataUtil
#--------------         
class ReportUtil:
    
     def sendReportByMail(self, mSMTP, mFrom, mTo, mCc, mPort, mLogin, mPassword, mSubject, mBody, mAttachment=[]):
         exportResend(mSMTP, mFrom, mTo, mCc, mPort, mLogin, mPassword, mSubject, mBody)
         zipTestDir()
         sendMail(mSMTP, mFrom, mTo, mCc, mPort, mLogin, mPassword, mSubject, mBody)

def sendMail(mSMTP, mFrom, mTo, mCc, mPort, mLogin, mPassword, mSubject, mBody, mAttachment=None):
        # print "Conect to server"
        smtpserver = smtplib.SMTP(mSMTP, mPort, timeout=120)  # 587
        smtpserver.ehlo()
        
        if mLogin:
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(mLogin, mPassword)
        # print "Create mail"
        emailmultipart = MIMEMultipart()
        emailmultipart['From'] = mFrom
        emailmultipart['To'] = mTo
        emailmultipart['Cc'] = mCc
        emailmultipart['Subject'] = mSubject
        email = MIMEText(mBody, 'html', _charset='utf-8')
        emailmultipart.attach(email)
        # print "Add attachment"

        if mAttachment and len(mAttachment) > 0:
            if type(mAttachment) is types.ListType:
                for mFile in mAttachment:
                    part = MIMEApplication(open(mFile, "rb").read())
                    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(mFile))
                    emailmultipart.attach(part)
            else:
                part = MIMEApplication(open(mAttachment, "rb").read())
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(mAttachment))
                emailmultipart.attach(part)   
        # print "Send Mail"
        try:
            smtpserver.sendmail(mFrom, mTo.split(";") + mCc.split(";"), emailmultipart.as_string())
            print "Mail Envoye !"
        except smtplib.SMTPException:  # Didn't make an instance.
            print "Error - SMTPException: mailUtil: ", sys.exc_info()
            return [mFrom, mTo.split(";") + mCc.split(";"), emailmultipart.as_string()]
        except smtplib.socket.error:
            print "Error - socket.error: mailUtil: ", sys.exc_info()
            return [mFrom, mTo.split(";") + mCc.split(";"), emailmultipart.as_string()]
        except:
            print "Error: mailUtil: ", sys.exc_info()
            return [mFrom, mTo.split(";") + mCc.split(";"), emailmultipart.as_string()]
        finally:    
            # print "Return params"
            if smtpserver:
                smtpserver.quit()    
            return [mFrom, mTo.split(";") + mCc.split(";"), emailmultipart.as_string()]

def exportResend(mSMTP, mFrom, mTo, mCc, mPort, mLogin, mPassword, mSubject, mBody, mAttachment=[]):
        mBody = mBody.replace("\\", "\\\\")
        dirPath = stormtest.GetLogFileDirectory()
        srcDir = os.path.join(dirPath, "src")
        if not os.path.exists(srcDir):
            os.makedirs(srcDir)
        mail = os.path.join(srcDir, "sendMail.py")
        mail = open(mail, 'w')
        header = "#!/usr/bin/python\n# -*- coding: utf-8 -*-"
        lib = "from reportUtil import sendMail"
        main = "if __name__ == '__main__':"
        p1 = "   print \"Renvoi  du mail\""
        send = "   sendMail('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}',{9})".format(mSMTP, mFrom, mTo, mCc, mPort, mLogin, mPassword, mSubject, mBody, mAttachment)
        p2 = "   print \"Envoi  du mail reussi !\""
        mail.write(header + "\r\n")
        mail.write(lib + "\n")
        mail.write(main + "\n")
        mail.write(p1 + "\n")
        mail.write(send + "\n")
        mail.write(p2 + "\n")
        mail.close()
        print "Exportation sendMail.py reussie"

def zipTestDir():
    srcPath = stormtest.GetLogFileDirectory()
    dirName = os.path.basename(srcPath)
    dstPath = srcPath + ".zip"
    zipf = zipfile.ZipFile(dstPath, 'w', zipfile.ZIP_DEFLATED)
    zipdir(srcPath, zipf)
    zipf.close()
    newPath = srcPath + "\\" + dirName + ".zip"
    os.rename(dstPath, newPath)
    return newPath
         
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
