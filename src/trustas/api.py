import uuid
import time
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
    print("CAs:", cli.CAs)

    # ============================================================
    # ========================== SEC 2 ===========================

    print("Sleeping...", flush=True)
    time.sleep(5)
    print("Woke up!")

    # Create a New Channel, the response should be true if succeed
    response = cli.channel_create(
                orderer_name='orderer.example.com',
                channel_name='businesschannel',
                requestor=org1_admin,
                config_yaml='test/fixtures/e2e_cli/',
                channel_profile='TwoOrgsChannel'
                )
    print(response==True)

    # # Join Peers into Channel, the response should be true if succeed
    # response = cli.channel_join(
    #             requestor=org1_admin,
    #             channel_name='businesschannel',
    #             peer_names=['peer0.org1.example.com',
    #                         'peer1.org1.example.com'],
    #             orderer_name='orderer.example.com'
    #             )
    # print(response==True)


    # # Join Peers from a different MSP into Channel
    # org2_admin = cli.get_user(org_name='org2.example.com', name='Admin')

    # # For operations on peers from org2.example.com, org2_admin is required as requestor
    # response = cli.channel_join(
    #             requestor=org2_admin,
    #             channel_name='businesschannel',
    #             peer_names=['peer0.org2.example.com',
    #                         'peer1.org2.example.com'],
    #             orderer_name='orderer.example.com'
    #             )
    # print(response==True)

    # ============================================================

