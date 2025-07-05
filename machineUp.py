#!/usr/bin/env python3

#This Program creates a backdoor to this computer Admin Manjunathan Sivakumar
#Development Started: 30 OCT 2023
#This Program is scheduled in Task Scheduler which triggers this event everytime when windows boots up or Cron job in linux env
#Version: 1.1.3
#Author: Manjunathan S


#01/15/24 Manjunathan - Removed log off functionality and added reboot limited parms s,k,r
#01/15/24 Manjunathan - Scheduled a cronjob which start when linux boots up. Igored os.system module as priviledges are required
#                       used subprocess instead
#05/07/25 Manjunathan - Added Operating Platform name indication
#cronjob input: @reboot sudo python3 /home/manjunathan/Root_Program/machineUp.py &


import smtplib
from datetime import datetime
from email.message import EmailMessage
import random
import imaplib
import email
import os
import sys
import time
import subprocess

_CODE = random.randint(1000,9999)

platform_name = sys.platform

msg = EmailMessage()
msg['Subject'] = 'Computer boot up activity detected'
msg['From'] = "nathanm6716@gmail.com"
msg['To'] = "manjunathsg407@gmail.com"
msg.set_content("Login Success\nSystem: "+str(platform_name)+"\nRemote Code = "+str(_CODE)+"\nParms = _shutdown = s, _kill = k, _reboot = r")

sender_email = "nathanm6716@gmail.com"
rec_email = "manjunathsg407@gmail.com"
password = "dfqagaljnaxstnzx"


def email_send_smtp():
    Email = 0
    while Email == 0:
        try:
            #STR_TIME_CODE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            #print("Login success")
            server.send_message(msg)
            Email = 1
        except:
            pass
email_send_smtp()

gmail_host= 'imap.gmail.com'

def imap_ack():
    mail.select("INBOX")
    _, selected_mails = mail.search(None, '(FROM "manjunathsg407@gmail.com")')
    for num in selected_mails[0].split():
        _, data = mail.fetch(num , '(RFC822)')
        _, bytes_data = data[0]

        #convert the byte data to message
        email_message = email.message_from_bytes(bytes_data)

        #print("Subject: ",email_message["subject"])

        if (email_message["subject"] == str(_CODE)+"_s"):
            #os.system("shutdown now -h")
            cmdCommand = "shutdown -h now"
            process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
        elif (email_message["subject"] == str(_CODE)+"_k"):
            sys.exit(0)
        elif (email_message["subject"] == str(_CODE)+"_r"):
            #os.system("reboot")
            cmdCommand = "reboot"
            process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)


try:
    mail = imaplib.IMAP4_SSL(gmail_host)
    ack = mail.login(sender_email, password)
    #print(ack[0])
    while 1:
        imap_ack()
except Exception as e:
    pass
