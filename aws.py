#!/usr/bin/python

############################################ 
# PROBLEM STATEMENT:
#
# This program will subscribe and show all the messages sent by its companion 
# aws_iot_pub.py using AWS IoT hub
#
############################################

############################################
# STEPS:
#
# 1. Sign in to AWS Amazon > Services > AWS IoT > Settings > copy Endpoint
#    This is your awshost
# 
# 2. Change following things in the below program:
#    a. awshost   (from step 1)
#    b. clientId  (Thing_Name)
#    c. thingName (Thing_Name)
#    d. caPath    (root-CA_certificate_Name)
#    e. certPath  (<Thing_Name>.cert.pem)
#    f. keyPath   (<Thing_Name>.private.key)
# 
# 3. Paste aws_iot_pub.py & aws_iot_sub.py python scripts in folder where all unzipped aws files are kept. 
# 4. Provide Executable permition for both the python scripts.
# 5. Run aws_iot_sub.py script
# 6. Run this aws_iot_pub.py python script
#
############################################

# importing libraries
import time
import datetime
import telepot
from telepot.loop import MessageLoop
import paho.mqtt.client as paho
import os
import sys
import socket
import ssl

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

sys.path.insert(0, "usr/bin/raspistill")
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#" , 1 )                              # Subscribe to all topics
 
chat_id=""
def handle(msg):
    print "checkpoint"
    chat_id = msg1['chat']['id']
    print chat_id

def on_message(client, userdata, msg):                      # Func for receiving msgs

    #print("payload: "+str(msg.payload))
    print "Checkpoint_1"
    
    os.system('raspistill -o /home/pi/image2.jpg')
    #bot.sendPhoto(chat_id, open('/home/pi/image2.jpg', 'rb'), caption= 'Screenshot taken!')
    sendemail()
    if os.path.exists('/home/pi/image2.jpg'):
        os.remove('/home/pi/image2.jpg')
       
         
def sendemail():
    fromaddr = "YOUR EMAIL HERE"
    toaddr = "THE EMAIL THAT YOU WANT TO SEND TO"
 
    msg = MIMEMultipart()
 
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Printer_Status"
 
    body = "Find the attached file "
 
    msg.attach(MIMEText(body, 'plain'))
 
    filename = "/home/pi/image2.jpg"
    attachment = open("/home/pi/image2.jpg", "rb")
 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    msg.attach(part)
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "ISWKpon1234")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))

bot = telepot.Bot('INSERT TOKEN HERE')

 
mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

#### Change following parameters ####  
awshost = "a2l9zo298nuyvu.iot.ap-southeast-1.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "MyRaspberryPi2"                                     # Thing_Name
thingName = "MyRaspberryPi2"                                    # Thing_Name
caPath = "/home/pi/Desktop/connect_device_package /root-CA.crt"                                      # Root_CA_Certificate_Name
certPath = "/home/pi/Desktop/connect_device_package /MyRaspberryPi2.cert.pem"                            # <Thing_Name>.cert.pem
keyPath = "/home/pi/Desktop/connect_device_package /MyRaspberryPi2.private.key"                          # <Thing_Name>.private.key
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)      # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_forever()                                        # Start receiving in loop
MessageLoop(bot, handle).run_as_thread()
