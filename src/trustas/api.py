import uuid
import time
from hfc.fabric import Client

# encrypt and publish the SLA in the beginning of an agreement with a partner
def createAgreement(partner, SLA):
    agreementId = uuid.uuid4()
    sla_key, sla_data = SLA.encrypt()
    return agreementId, sla_key, sla_data

# encrypt and publish the measurements of an agreement
def publishMeasurements(agreementId, measurements, encryption_key):
    _, enc_data = measurements.encrypt(encryption_key)
    return enc_data

# retrieve the encrypted measurements and SLA
def retrieveASHistory(asn):
    # query chaincode for history of asn:
    # history = cc.queryHistory(asn)
    history = None
    return history
