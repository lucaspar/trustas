#===================================================#
#                     Imports                       #
#===================================================#
import sys
import subprocess
from Crypto.PublicKey import RSA
#===================================================#
#                   Global config                   #
#===================================================#
# AS config
myUser = sys.argv[5]
#===================================================#
#                     Functions                     #
#===================================================#
# get AS' reputation as a customer or as a provider from the ledger
def getReputation(ASN, role):
    x=""

    while "address" not in x:
        # Query the ledger to get AS' information
        x = subprocess.check_output('node js/query.js show \''+ASN+'\''+' '+myUser, shell=True)
    # Get the reputation
    if role == "customer":
        return x.split(",")[1].split(':')[1]
    elif role == "provider":
        return x.split(",")[2].split(':')[1]

# get AS' address from the ledger
def getAddress(ASN):
    x=""

    while "address" not in x:
        # Query the ledger to get AS' information
        x = subprocess.check_output('node js/query.js show \''+ASN+'\''+' '+myUser, shell=True)
    # Get the address
    aux = x.split(",")[0]
    ip = aux.split(":")[1]
    port = aux.split(":")[2]

    # Return ip:port
    return ip.split("\"")[1]+":"+port.split("\"")[0]

# get AS' public key from the ledger
def getPubKey(ASN):
    x=""

    while "address" not in x:
        # Query the ledger to get AS' information
        x = subprocess.check_output('node js/query.js show \''+ASN+'\''+' '+myUser, shell=True)
    S = x.split(",")[3].split(":")[1]

    #transform pubKey String in a pubKey obj
    pubKeyString = S.split("\"")[1]
    pubKeyString = pubKeyString.replace('\\n','\n')
    pubKey = RSA.importKey(pubKeyString)

    return pubKey
