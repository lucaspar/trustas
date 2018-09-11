#===================================================#
#                     Imports                       #
#===================================================#
import sys
import subprocess
from datetime import datetime
from blockchain import getAddress, getPubKey
from intents import checkIntents
from offers import storeOffer
from LLF import sendContract
from dynamix import agreementsCust, agreementsProv
#===================================================#
#                   Global config                   #
#===================================================#
# AS config
myASN = sys.argv[1]
myUser = sys.argv[5]
ordererIP = 'grpc://'+sys.argv[6]+':7050'

# Evaluation log
logs = open(myASN+".log", "w")
#===================================================#
#                     Functions                     #
#===================================================#
# Receives a query action and send it to a potential provider
def sendQuery(action):
    from communication import sendMessage           # TODO fix import

    n = len(action.split(","))

    # query(AS2, 8.8.8.0/24, sla.latency == 10 && sla.repair < 0.5)
    # Get provider's ASN
    provider = action.split(",")[0]
    provider = provider[6:]

    # Query the ledger to get the provider's address
    address = ""
    while ":" not in address:
        address = getAddress(provider)

    # Split the address into IP and port
    IP = address.split(":")[0]
    port = int(address.split(":")[1])

    # Get the query
    if n == 3:
        properties = action.split(",")[2]
        properties = properties[1:-1]
        intent = action.split(",")[1]
        intent = intent[1:]
        query = intent + " " + properties
    else:
        #properties = "null"
        intent = action.split(",")[1]
        intent = intent[1:-1]
        query = intent

    # Query the ledger to get the provider's public key
    pubkey = getPubKey(provider)

    # Evaluation control
    # Generate the query/offer ID
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    ID = myASN+"-"+provider+"-"+timestamp

    # Create the message that is going to be sent
    msg = 'query;'+myASN+';'+query+";"+ID

    # logging
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    # Send the query to the provider
    sendMessage(msg, IP, port, pubkey, 0)

    # logging
    logs.write(timestamp+";SQ;"+ID+"\n")

# Receive a query from a customer, decide if it is going to answer, and compose and agreement offer
def sendOffer(query):
    from communication import sendMessage           # TODO fix import

    # queryFormat = query;customerASN;properties
    print "Received: "+query

    # Get customer's ASN
    customer = query.split(";")[1]
    # Verify customer's reputation
    reputation = 1 #getReputation(customer, "customer")
    # If AS is a good customer, send offer
    if int(reputation) >= 0:                # TODO Define reputation threshold
        # Check interconnection policy to compose and offer to the customer
        ID = query.split(";")[3]
        offer = composeOffer(query.split(";")[2], customer, ID)
        # If provider can offer something, send
        if offer != -1:
            # Get customer's address
            address = ""
            while ":" not in address:
                address = getAddress(customer)
            #print "Got address "+address+" for query "+query
            # Split address into IP and port
            IP = address.split(':')[0]
            port = int(address.split(':')[1])
            # Get customer's public key
            pubKey = getPubKey(customer)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            #Send offer
            sendMessage(offer+";"+ID, IP, port, pubKey, 0)

            # logging
            logs.write(timestamp+";SO;"+ID+"\n")

        # Provider is not able to offer an agreement with the desired properties
        else:
           print "I cannot offer an agreement!"
    # Customer has poor reputation
    else:
        print "Customer with poor reputation!"

# Check the interconnection policy and compose and offer to be sent to the customer
def composeOffer(query, customer, ID):
# Generate the offer ID
#    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#    ID = myASN+"-"+customer+"-"+timestamp

#    offer = "offer;"+ID+";"+query+";10$;"+expireDate
    properties = checkIntents(query)

    if properties != -1:
        # Store the offer on the list. This is important to verify if the offer is still valid when the customer sends the proposal message.
        storeOffer(ID+";"+properties, "sent")
        #return offer
        return "offer;"+ID+";"+properties
    else:
        return properties

# Send an interconnection proposal to an AS
def sendProposal(action):
    from communication import sendMessage           # TODO fix import

    # action = propose offerID
    # Get only the offerID
    offerID = action.split("propose ")[1]
    # Get the provider's ASN
    provider = offerID.split("-")[1]
    pubKey = getPubKey(provider)
    # If the offer is still valid, send interconnection proposal to the provider
    if checkValidity(offerID) == 1:
        # Get provider's address
        address = ""
        while ":" not in address:
            address = getAddress(provider)        # Split address into IP and port
        IP = address.split(':')[0]
        port = int(address.split(':')[1])
        # Send interconnection proposal
        msg = "propose"+";"+offerID
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        sendMessage(msg, IP, port, pubKey, 0)

        # logging
        logs.write(timestamp+";SP;"+offerID+"\n")

    # If the offer is not valid anymore, there is no reason to send the interconnection proposal
    else:
        print "Offer is not valid anymore!"

# Check if the offer is not expired
def checkValidity(offerID):

    # query offersSent[offerID]
    # get expireDate

    # if time.now() < expireDate:
    #    return 1
    # else:
    #   return -1

    return 1

# Receive a propose message and send the contract if the offer is still valid
def establishAgreement(propose, myPrivKey):
    from communication import sendMessage           # TODO fix import

    offerID = propose.split(";")[1]
    pubKey = getPubKey(propose.split("-")[1])

    print "Received: "+propose

    # If offer is still valid, send the contract
    if checkValidity(offerID) == 1:
        sendContract(offerID, myPrivKey)
    # Offer is no longer valid
    else:
        msg = "Offer is no longer valid"
        print msg
        # TODO get address
        # Send message
        sendMessage(msg, IP, port, pubKey, 0)

def executeAgreements():
    for agmnt in agreementsProv.keys():
        #if ended
        customer = agreementsProv[agmnt].split(";")[0]
        print customer
        # update customer's reputation
        x = subprocess.check_output('node js/update.js updateCustRep \''+customer+'\' \'1\''+' '+myUser+' '+ordererIP, shell=True)
        print x

        del agreementsProv[agmnt]

    for agmnt in agreementsCust.keys():
        #if ended
        provider = agreementsCust[agmnt].split(";")[1]
        print provider
        # update provider's reputation
        x = subprocess.check_output('node js/update.js updateProvRep \''+provider+'\' \'1\''+' '+myUser+' '+ordererIP, shell=True)
        print x

        del agreementsCust[agmnt]

    return
