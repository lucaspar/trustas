#===================================================#
#                     Imports                       #
#===================================================#
import sys
import hashlib
import subprocess
from datetime import datetime
from Crypto.PublicKey import RSA
from blockchain import getAddress, getPubKey
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
# Send the contract of the interconnection agreement to the customer
def sendContract(offerID, myPrivKey):
    from communication import sendMessage           # TODO fix import

    # Get customer's ASN
    customer = offerID.split("-")[0]
    provider = myASN

    # Get customer's pubKey
    pubKey = getPubKey(customer)

    # Get provider's address
    address = ""
    while ":" not in address:
        address = getAddress(customer)
    # Split address into IP and port
    IP = address.split(':')[0]
    port = int(address.split(':')[1])

    # Write the contract
    contract = "contract of the Interconnection agreement between "+provider+" and "+customer+offerID

    # Compute the contract hash
    hash_object = hashlib.md5(contract.encode())
    h = hash_object.hexdigest()

    # Provider signs the contract
    providerSignature = myPrivKey.sign(h,0)

    # Send the contract
    msg = "contract;"+offerID+";"+h+";"+customer+";"+provider+";"+str(providerSignature[0])

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    sendMessage(msg, IP, port, pubKey, 1)

    # logging
    logs.write(timestamp+";SC;"+offerID+"\n")

# Customer sign the contract
def signContract(contract, myPrivKey):
    from communication import sendMessage           # TODO fix import

    # Remove message header
    s = contract.split("contract;")[1]
    # Get the contract hash
    h = contract.split(";")[2]

    # Get provider's ASN
    provider = contract.split(";")[4]

    # Get the contract hash
    providerSignature = contract.split(";")[5]

    # Get provider's pubKey
    pubKey = getPubKey(provider)

    # Customer verify the provider signature
    if pubKey.verify(h, (long(providerSignature),0)) == False:
        print "Invalid signature!"
    else:
        # Customer signs the contract
        customerSignature = myPrivKey.sign(h,0)

        # Get provider's address
        address = ""
        while ":" not in address:
            address = getAddress(provider)    # Split address into IP and port
        IP = address.split(':')[0]
        port = int(address.split(':')[1])

        # Send message with the contract signed by the customer
        msg = "publish;"+s+";"+str(customerSignature[0])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        sendMessage(msg, IP, port, pubKey,2)

        # logging
        logs.write(timestamp+";SS;"+contract.split(";")[1]+"\n")

        key = "IA-"+h
        agreementsCust[key] = myASN+";"+provider

def publishAgreement(info):
    from communication import sendMessage           # TODO fix import

    # Get the parameters that will be registered on the ledger
    contractHash = info.split(";")[2]
    customer = info.split(";")[3]
    provider = myASN
    providerSignature = info.split(";")[5]
    customerSignature = info.split(";")[6]

    # Get customer's pubKey
    pubKey = getPubKey(customer)

    # Provider verify the customer signature
    if pubKey.verify(contractHash, (long(customerSignature),0)) == False:
        print "Invalid signature!"
    else:

        key = "IA-"+contractHash

        # Register the agreement on the ledger
        x = subprocess.check_output('node js/publish.js registerAgreement \''+key+'\' \''+contractHash+'\' \''+customer+'\' \''+provider+'\' \''+customerSignature+'\' \''+providerSignature+'\''+' '+myUser+' '+ordererIP, shell=True)
        agreementsProv[key] = customer+";"+provider
        print key+" Success! Updating routing configuration!"

        # Get customer's address
        address = ""
        while ":" not in address:
            address = getAddress(customer)
        # Split address into IP and port
        IP = address.split(':')[0]
        port = int(address.split(':')[1])

        offerID=info.split(";")[1]

        # Send message with the key
        msg = "ack;"+offerID+";"+key
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        sendMessage(msg, IP, port, pubKey, 0)

        # logging
        logs.write(timestamp+";SU;"+offerID+"\n")
