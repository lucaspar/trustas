#===================================================#
#                     Imports                       #
#===================================================#
import sys
import json
import ipaddress
from datetime import datetime
from datetime import timedelta
#===================================================#
#                   Global config                   #
#===================================================#
# Read intent file
intents = json.load(open(sys.argv[4]))
#===================================================#
#                     Functions                     #
#===================================================#
def checkIntents(query):
    i = 0

    n = len(query.split(" "))
    customerIntent = query.split(" ")[0]

    if n > 1:
        customerProperties = query[len(customerIntent)+1:]
    else:
        customerProperties = "null"

    customerAddress,subnetCustomer = customerIntent.split("/")

    #turns a string into ipv4address
    customerAddress = ipaddress.ip_address(unicode(customerAddress))

    # iterate over provider's intents
    while i < len(intents.keys()):
        fileIntent = str(intents.keys()[i])
        fileAddress,subnetIntent = fileIntent.split("/")

        #turns a string into ipv4network
        fileIntent = ipaddress.ip_network(unicode(fileIntent))

        if subnetCustomer >= subnetIntent:
            if customerAddress in fileIntent:
                if checkproperties(customerProperties,i) == 1:
                    offer = fillOffer(i)
                    return offer

        i = i + 1

    # return -1 if the provider cannot offer an agreement with the desired propertiess
    return -1

def checkproperties(customerProperties,i):
    k = 0

    if customerProperties == "null":
        return 1
    else:
        try:
            properties = customerProperties.split("&& ")
        except ValueError:
            properties = customerProperties

        # iterate over customer's properties
        while k < len(properties):

            testProp = properties[k]

            #TODO assuming the same command line as shown in help: query(AS2, 8.8.8.0/24, sla.latency == 10 && sla.repair < 0.5)
            prop = testProp.split(" ")[0]
            value = testProp.split(" ")[2]

            if prop == "sla.bwidth" and float(value) > float(intents[intents.keys()[i]]["sla"]["bandwidth"]):
                return -1
            elif prop == "sla.latency" and float(value) < float(intents[intents.keys()[i]]["sla"]["latency"]):
                return -1
            elif prop == "sla.pkt_loss" and float(value) < float(intents[intents.keys()[i]]["sla"]["loss"]):
                return -1
            elif prop == "sla.jitter" and float(value) < float(intents[intents.keys()[i]]["sla"]["jitter"]):
                return -1
            elif prop == "sla.repair" and float(value) < float(intents[intents.keys()[i]]["sla"]["repair"]):
                return -1
            elif prop == "sla.guarantee" and float(value) > float(intents[intents.keys()[i]]["sla"]["guarantee"]):
                return -1
            elif testProp == "sla.availability" and float(value) > float(intents[intents.keys()[i]]["sla"]["availability"]):
                return -1
            elif prop == "pricing.egress" and float(value) < float(intents[intents.keys()[i]]["pricing"]["egress"]):
                return -1
            elif prop == "pricing.ingress" and float(value) < float(intents[intents.keys()[i]]["pricing"]["ingress"]):
                return -1
            elif prop == "pricing.billing" and str(value) != str(intents[intents.keys()[i]]["pricing"]["billing"]):
                return -1
            elif prop != "sla.bwidth" and prop != "sla.latency" and prop != "sla.pkt_loss" and prop != "sla.jitter" and prop != "sla.repair" and prop != "sla.guarantee" and prop != "sla.availability" and prop != "pricing.egress" and prop != "pricing.ingress" and prop != "pricing.billing":
                print "Invalid Propertie: ", prop
                return -1
            else:
                k = k+1

        return 1

def fillOffer(i):
    target = "target:"+str(intents.keys()[i])
    aspath = ",routing.aspath:"+str(intents[intents.keys()[i]]["routing"]["aspath"])
    bandwidth = ",sla.bandwidth:"+str(intents[intents.keys()[i]]["sla"]["bandwidth"])
    latency = ",sla.latency:"+str(intents[intents.keys()[i]]["sla"]["latency"])
    jitter = ",sla.jitter:"+str(intents[intents.keys()[i]]["sla"]["jitter"])
    loss = ",sla.loss:"+str(intents[intents.keys()[i]]["sla"]["loss"])
    repair = ",sla.repair:"+str(intents[intents.keys()[i]]["sla"]["repair"])
    availability = ",sla.availability:"+str(intents[intents.keys()[i]]["sla"]["availability"])
    guarantee = ",sla.guarantee:"+str(intents[intents.keys()[i]]["sla"]["guarantee"])
    egress = ",pricing.egress:"+str(intents[intents.keys()[i]]["pricing"]["egress"])
    ingress = ",pricing.ingress:"+str(intents[intents.keys()[i]]["pricing"]["ingress"])
    billing = ",pricing.billing:"+str(intents[intents.keys()[i]]["pricing"]["billing"])
    length = ",time.length:"+str(intents[intents.keys()[i]]["time"]["unit"])
    expireDate = ",time.expire:"+str(datetime.now() + timedelta(hours=6))

    offer = target+aspath+bandwidth+latency+jitter+loss+repair+availability+guarantee+egress+ingress+billing+length+expireDate

    return offer
