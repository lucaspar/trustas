#===================================================#
#                     Imports                       #
#===================================================#
import os
import sys
import json
import threading
import subprocess
from Crypto import Random
from Crypto.PublicKey import RSA
from communication import *
from autonomous import *
from protocol import *
from offers import *
#===================================================#
#                   Global config                   #
#===================================================#
# AS config
myASN = sys.argv[1]
myAddress = sys.argv[2]
myIP = sys.argv[2].split(":")[0]
myPort = sys.argv[2].split(":")[1]
myService = sys.argv[3]
myUser = sys.argv[5]
ordererIP = 'grpc://'+sys.argv[6]+':7050'

# Dictionaries contanining the offers that the AS have sent and received
offersSent = {}
offersRecvd = {}

# Dictionary containing the AS' interconnetion agreements
agreementsCust = {}
agreementsProv = {}

# Evaluation log
logs = open(myASN+".log", "w")
#===================================================#
#                     Functions                     #
#===================================================#
# Command line interface. Reads an instructions and call the appropriate function.
def cli():
    while True:
        action = raw_input("Dynam-IX: ")
        if len(action) > 0:
            if "registerAS" in action: # registerAS 'ASN' 'address' 'service' 'custRep' 'provRep' 'pubKey'
                x = subprocess.check_output('node js/register.js '+action+' '+myUser+' '+ordererIP, shell=True)
                print x
            elif "listASes" in action:  # listASes
                x = subprocess.check_output('node js/list.js'+' '+myUser, shell=True)
                print x
            elif "findService" in action: # findService service         # TODO fix this function when string has space
                #queryString = "{\"selector\":{\"service\":\"Transit\"}}"
                service = action.split("- ")[1]
                print service
                x = subprocess.check_output('node js/query.js findService \'{\"selector\":{\"service\":\"'+service+'\"}}\''+' '+myUser, shell=True)
                print x
            elif "show" in action: #show 'key'
                x = subprocess.check_output('node js/query.js '+action+' '+myUser, shell=True)
                print x
            elif "history" in action: #history 'key'
                x = subprocess.check_output('node js/query.js '+action+' '+myUser, shell=True)
                print x
            elif "delete" in action: #delete 'key'
                x = subprocess.check_output('node js/delete.js '+action+' '+myUser+' '+ordererIP, shell=True)
                print x
            elif "updateService" in action: #updateService 'ASN' 'newService'
                x = subprocess.check_output('node js/update.js '+action+' '+myUser+' '+ordererIP, shell=True)
                print x
            elif "updateAddress" in action: #updateAddress 'ASN' 'newAddress'
                x = subprocess.check_output('node js/update.js '+action+' '+myUser+' '+ordererIP, shell=True)
                print x
            elif "query" in action: #query providerASN request
                sendQuery(action)
            elif "propose" in action: #propose ID
                sendProposal(action)
            elif "listAgreements" in action:
                x = subprocess.check_output('node js/listAgreements.js'+' '+myUser, shell=True)
                print x
            elif "listOffersSent" in action:
                listOffersSent()
            elif "listOffersRecvd" in action:
                listOffersRecvd()
            elif "myAgreements" in action:
                myAgreements()
            elif "executeAgreements" in action:
                executeAgreements()
            elif "autonomous" in action:
                autonomous()
            elif "updateIntents" in action:
                intents = json.load(open(action.split(" ")[1]))
            elif "help" in action:
                help()
            elif "quit" in action:
                print "Quiting Dynam-IX"
                logs.close()
                os._exit(1)
            else:
                print "Invalid command. Type \'help\' to list the available commands.\n"
    return

def help():
    print("List of Dynam-IX commands")
    print("listASes - lists the ASes connected to the Dynam-IX blockchain")
    print("listAgreements - lists the interconnection agreements registered on Dynam-IX")
    print("query(ASx, TARGET, PROPERTIES) - sends a query to ASx for an interconnection agreement to reach prefix")
    print("\t\t example: query(AS2, 8.8.8.0/24, sla.latency == 15 && sla.bwidth >= 1000)")
    print("propose PROPOSAL_ID - sends an interconnection proposal request to the AS that offered the PROPOSAL_ID")
    print("\t\t example: propose AS2-AS1-123414121251")
    print("listOffersRecvd - lists the offeres that were received")
    print("listOffersSent - lists the offers that were sent")
    print("updateIntents PATH/TO/FILE - loads a new intent file")
    print("\t\t example: updateIntents newIntents.json")
    print("executeAgreements - updates the reputation of the ASes connected to me")
    print("myAgreements - lists my interconnection agreements")
    print("quit - quits Dynam-IX")

#Main function
if __name__ == "__main__":
    # Generate public and private keys
    #basePhrase = myASN+myASN+"Dynam-IX"
    baseNumber = Random.new().read
    myPrivKey = RSA.generate(4096, baseNumber)
    myPubKey = myPrivKey.publickey()
    myPubKeyString = myPubKey.exportKey('PEM')

    # Read intent file
    intents = json.load(open(sys.argv[4]))

    # TODO optimize to not query the blockchain
    # If AS is not registered
    if '{' not in subprocess.check_output('node js/query.js show \''+myASN+'\''+' '+myUser, shell=True):
        print "Registering new AS", myASN, myAddress, myService
        x = subprocess.check_output('node js/register.js registerAS \''+myASN+'\' \''+myAddress+'\' \''+myService+'\' \'0\' \'0\' \''+myPubKeyString+'\''+' '+myUser+' '+ordererIP, shell=True)
        print x
    # else, update address
    else:
        print "Updating AS address", myASN, myAddress, myService
        x = subprocess.check_output('node js/update.js updateAddress \''+myASN+'\' \''+myAddress+'\''+' '+myUser+' '+ordererIP, shell=True)

    mode = sys.argv[7]

    # Start threads
    threads = []
    if mode == "autonomous":
        t = threading.Thread(target=autonomous)
        threads.append(t)
        t.start()
        #t = threading.Thread(target=end)
        #threads.append(t)
        #t.start()
    else:
        t = threading.Thread(target=cli)
        threads.append(t)
        t.start()
    t = threading.Thread(target=processMessages, args=(myPrivKey,))
    threads.append(t)
    t.start()
