import uuid
from hfc.fabric import Client

# encrypt and publish the SLA in the beginning of an agreement with a partner
def createAgreement(partner, SLA):
    agreementId = uuid.uuid4()
    print("\nSLA of Agreement {}\n".format(agreementId))
    SLA.print()
    sla_key, sla_data = SLA.encrypt()
    return agreementId, sla_key, sla_data

# encrypt and publish the measurements of an agreement
def publishMeasurements(agreementId, measurements, encryption_key):
    print("\nMeasurements of Agreement {}\n".format(agreementId))
    measurements.print()
    _, enc_data = measurements.encrypt(encryption_key)
    print("=====================")
    return enc_data

# retrieve the encrypted measurements and SLA
def retrieveASHistory(asn):
    # print("=====================")
    # query chaincode for history of asn:
    # history = cc.queryHistory(asn)
    # print(history)
    # print("=====================")
    history = None
    return history

# hyperledger fabric client setup (python SDK)
def hfcSetup():

    cli = Client(net_profile="test/fixtures/network.json")
    org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')

    print(org1_admin)
    print(cli.organizations)
    print(cli.peers)
    print(cli.orderers)
    print(cli.CAs)
