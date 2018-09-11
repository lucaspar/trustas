#===================================================#
#                     Imports                       #
#===================================================#
from dynamix import offersSent, offersRecvd, agreementsCust, agreementsProv
#===================================================#
#                     Functions                     #
#===================================================#
# Receive an offer and store it on the appropriate dictionary
def collectOffer(offer):
    ID = offer.split(";")[1]
    properties = offer.split(";")[2]

    print "Received: "+ offer
    storeOffer(ID+";"+properties, "recvd")

# Store an offer on the appropriate dictionary
def storeOffer(offer, direction):
    ID = offer.split(";")[0]
    properties = offer.split(";")[1]

    if direction == "sent":
        offersSent[ID] = properties
    elif direction == "recvd":
        offersRecvd[ID] = properties

# Print all the offers that were sent to customers
def listOffersSent():
    for offer in offersSent:
        print offer, offersSent[offer]

# Print all the offers that were received from providers
def listOffersRecvd():
    for offer in offersRecvd:
        print offer, offersRecvd[offer]

# Delete expired offers
def cleanOffers():
    #if offer expired, remove
    return

def myAgreements():
    for agmnt in agreementsCust:
        print agmnt, agreementsCust[agmnt]
    for agmnt in agreementsProv:
        print agmnt, agreementsProv[agmnt]
