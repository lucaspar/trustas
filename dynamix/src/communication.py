#===================================================#
#                     Imports                       #
#===================================================#
import os
import sys
import socket
import threading
from datetime import datetime
from Crypto.PublicKey import RSA
from autonomous import verifyUpdate
from protocol import sendOffer, establishAgreement
from offers import collectOffer
from LLF import signContract, publishAgreement
#===================================================#
#                   Global config                   #
#===================================================#
# AS config
myASN = sys.argv[1]
myIP = sys.argv[2].split(":")[0]
myPort = sys.argv[2].split(":")[1]

# Evaluation log
logs = open(myASN+".log", "w")
#===================================================#
#                     Functions                     #
#===================================================#
# Receive messages and create threads to process them
def processMessages(myPrivKey):
    messageThreads = []

    # Open socket to accept connections
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((myIP, int(myPort)))
    serversocket.listen(256) # NOTE We may need to increase the number simultaneous requests

    while True:
        connection, address = serversocket.accept()
        msg = ''
        msg = connection.recv(4096)     # NOTE We may need to change the amount of received bytes

        try:
            encryptMsg = msg.split('signatures')[0]
        except ValueError:
            encryptMsg = msg
        try:
            signatures = msg.split('signatures')[1]
        except IndexError:
            signatures = ''

        msg = myPrivKey.decrypt(encryptMsg) + signatures

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        if len(msg) > 0:
            if "query" in msg:  # Customer is asking for an offer
                # logging
#                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                logs.write(timestamp+";RQ;"+msg.split(";")[3]+"\n")
                t = threading.Thread(target=sendOffer, args=(msg,))
                messageThreads.append(t)
                t.start()
            elif "offer" in msg: # Provider have sent an offer
                # logging
#                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                logs.write(timestamp+";RO;"+msg.split(";")[3]+"\n")
                t = threading.Thread(target=collectOffer, args=(msg,))
                messageThreads.append(t)
                t.start()
            elif "propose" in msg: # Customer is asking to establish an interconnection agreement
                # logging
#                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                logs.write(timestamp+";RP;"+msg.split(";")[1]+"\n")
                t = threading.Thread(target=establishAgreement, args=(msg,myPrivKey,))
                messageThreads.append(t)
                t.start()
            elif "contract" in msg: # Provider have sent the contract to be signed
                # logging
#                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                logs.write(timestamp+";RC;"+msg.split(";")[1]+"\n")
                t = threading.Thread(target=signContract, args=(msg,myPrivKey,))
                messageThreads.append(t)
                t.start()
            elif "publish" in msg:  # Customer is sending the signed contract to be registered on the ledger
                # logging
#                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                logs.write(timestamp+";RS;"+msg.split(";")[1]+"\n")
                t = threading.Thread(target=publishAgreement, args=(msg,))
                messageThreads.append(t)
                t.start()
            elif "ack" in msg:  # Customer is sending the signed contract to be registered on the ledger
                print "Success! Updating routing configuration!"
                # logging
#                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                logs.write(timestamp+";RU;"+msg.split(";")[1]+"\n")
                t = threading.Thread(target=verifyUpdate, args=(msg,))
                messageThreads.append(t)
                t.start()
            else:
                print "Invalid message\n"
                #print msg

def sendMessage(msg, ip, port, pubKey, flag):
    # Encrypt message with the pubKey
    if flag == 1:           # contract MSG
        signature = msg.split(';')[5]
        msg = msg.split(';')[0]+';'+msg.split(';')[1]+';'+msg.split(';')[2]+';'+msg.split(';')[3]+';'+msg.split(';')[4]+';'
        encryptMSG = pubKey.encrypt(msg, 0)[0]+'signatures'+signature
    elif flag == 2 :        # publish MSG
        signature1 = msg.split(';')[5]
        signature2 = msg.split(';')[6]
        msg = msg.split(';')[0]+';'+msg.split(';')[1]+';'+msg.split(';')[2]+';'+msg.split(';')[3]+';'+msg.split(';')[4]+';'
        encryptMSG = pubKey.encrypt(msg, 0)[0]+'signatures'+signature1+';'+signature2
    else:
        encryptMSG = pubKey.encrypt(msg, 0)[0]

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((ip, port))
    clientsocket.send(encryptMSG)
    clientsocket.close()
