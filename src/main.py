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
#09/05/26 Manjunathan - Code Cleanup - Added Software Engineering Pratices along with Pytest
#cronjob input: @reboot sudo python3 /home/manjunathan/Root_Program/machineUp.py &


import smtplib
from email.message import EmailMessage
import random
import imaplib
import email
import os
from dotenv import load_dotenv
import sys
import subprocess
import configparser

def read_constants_file():
    """
    This function access the properties ini file and extracts
    sender's/receiver's email address, subject
    Exception handling is placed as well
    """
    try:
        config_path = 'properties.ini'
        cnf_parser = configparser.ConfigParser()
        cnf_parser.read(config_path)
        email_constants = cnf_parser['EMAIL_CONSTANTS']
        email_fields = {'sender_address' : email_constants.get('machine_sender_email'),
                        'receiver_address' : email_constants.get('human_receiver_email'),
                        'subject':  email_constants.get('subject'),
                        'smtp_addr': email_constants.get('smtp_addr'),
                        'imap_addr': email_constants.get('imap_addr')}
        return email_fields
    except Exception as err:
        print("Something went wrong", err)
        exit(1) #System exit - 1

constant_file_data = read_constants_file()

#Setting up things
def setup_email():
    """
    This function setups up the email fields and message content to be sent
    """
    global sender_email, rec_email, password, msg, _CODE, password
    _CODE = random.randint(1000,9999)
    platform_name = sys.platform
    sender_email = constant_file_data['sender_address']
    rec_email =  constant_file_data['receiver_address']
    load_dotenv()
    password = os.getenv('PASSWORD')
    msg = EmailMessage()
    msg['Subject'] = constant_file_data['subject']
    msg['From'] = sender_email
    msg['To'] = rec_email
    msg.set_content("Login Success\nSystem: "+str(platform_name)+"\nRemote Code = "+str(_CODE)+"\nParms = _shutdown = s, _kill = k, _reboot = r")

setup_email()

def email_send_smtp():
    """
    This function tried to establish the SMTP connection and 
    tries to send. If the system faces connection error this will keep on trying
    """
    Email = 0
    while Email == 0:
        try:
            smpt_addr_ = constant_file_data['smtp_addr']
            server = smtplib.SMTP(smpt_addr_, 587)
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            Email = 1
            print("Email has been sent")
        except:
            #Just keep on Trying
            pass       
email_send_smtp()

def imap_ack():
    "This function acknowledges and tried to take actions based on CMD command"
    mail.select("INBOX")
    _, selected_mails = mail.search(None, f'(FROM "{constant_file_data['receiver_address']}")')
    for num in selected_mails[0].split():
        _, data = mail.fetch(num , '(RFC822)')
        _, bytes_data = data[0]

        #convert the byte data to message
        email_message = email.message_from_bytes(bytes_data)

        if (email_message["subject"] == str(_CODE)+"_s"):
            #os.system("shutdown now -h")
            cmdCommand = "shutdown -h now"
            subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
        elif (email_message["subject"] == str(_CODE)+"_k"):
            sys.exit(0)
        elif (email_message["subject"] == str(_CODE)+"_r"):
            #os.system("reboot")
            cmdCommand = "reboot"
            subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)

def email_read_imap():
    """
    This function tried to establish the IMAP connection and 
    tries to read. If the system faces connection error this will keep on trying
    """
    try:
        global mail
        imap_addr = constant_file_data['imap_addr']
        mail = imaplib.IMAP4_SSL(imap_addr)
        mail.login(sender_email, password)
        while 1:
            imap_ack()
    except Exception as e:
        print(e)
        pass
email_read_imap()

