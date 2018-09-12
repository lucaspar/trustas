import uuid

# encrypt and publish the SLA in the beginning of an agreement with a partner
def createAgreement(partner, SLA):
    agreementId = uuid.uuid4()
    sla_key, sla_data = SLA.encrypt()
    return agreementId, sla_key, sla_data

# encrypt and publish the measurements of an agreement
def publishMeasurements(agreementId, measurements, encryption_key):
    print("=====================")
    print("Publishing Measurements of Agreement {}\n".format(agreementId))
    measurements.print()
    _, enc_data = measurements.encrypt(encryption_key)
    print("=====================")
    return enc_data

# retrieve the encrypted measurements and SLA
def retrieveASHistory(asn):
    print("=====================")
    history = None
    # query chaincode for history of asn:
    # history = cc.queryHistory(asn)
    print(history)
    print("=====================")
    return history
