#===================================================#
#                     Imports                       #
#===================================================#
import os
import sys
import time
import subprocess
from datetime import datetime
from protocol import sendQuery, sendProposal
from dynamix import offersRecvd
from offers import listOffersRecvd
#===================================================#
#                   Global config                   #
#===================================================#
# AS config
myASN = sys.argv[1]
myUser = sys.argv[5]

# Evaluation log
logs = open(myASN+".log", "w")
#===================================================#
#                     Functions                     #
#===================================================#
def autonomous():
    print "Entering autonomous mode!"
    time.sleep(5)  # Be sure to wait the necessary time to start

    AS = "AS1"
    num = int(sys.argv[8])
    sleepTime = int(sys.argv[9])

    print "Going to interact with "+AS+" doing "+str(num)+" queries/proposals every "+str(sleepTime)+" seconds"

    #global offersRecvd

    total = 0
    while total < 5:
        #offersRecvd = {}

        for i in range(0,num):
            #query AS prefix
            query = "query("+AS+", 8.8.8.0/24)"
            sendQuery(query)

        while len(offersRecvd) < num:
            #print "Number of offers: "+str(len(offersRecvd))
            time.sleep(0.5)

        #listOffersRecvd()

        for offer in offersRecvd.keys():
            offerID = offer
            proposal = "propose "+offerID
            #propose offerID
            sendProposal(proposal)

        total = total + num
        #print "Sleeping"
        #time.sleep(1)
        #print "Waking up"

    time.sleep(30)  # Be sure of getting all agreements answers
    print "Leaving autonomous mode!"
    time.sleep(5)
    print "Quiting Dynam-IX"

    logs.close()
    os._exit(1)

def verifyUpdate(ack):
    offerID = ack.split(";")[1]
    IA = ack.split(";")[2]

    out = ""

    while "hash" not in out:
        out = subprocess.check_output('node js/query.js show '+IA+' '+myUser, shell=True)
        time.sleep(1)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    logs.write(timestamp+";VU;"+offerID+"\n")

def end():
    time.sleep(1200)
    print "Quiting Dynam-IX"
    logs.close()
    os._exit(1)
