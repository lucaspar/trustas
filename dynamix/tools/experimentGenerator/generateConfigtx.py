#!/usr/bin/python
import sys

def profiles(numOrgs):

    print "Profiles:"
    print "  SingleOrgOrdererGenesis:"
    print "    Orderer:"
    print "      <<: *OrdererDefaults"
    print "      Organizations:"
    print "        - *OrdererOrg"
    print "    Consortiums:"        
    print "      SampleConsortium:"
    print "        Organizations:"
    for i in range(1, numOrgs+1):
        print "          - *Org"+str(i)
    print "  MultipleOrgChannel:"
    print "    Consortium: SampleConsortium"
    print "    Application:"
    print "      <<: *ApplicationDefaults"
    print "      Organizations:"
    for i in range(1, numOrgs+1):
        print "          - *Org"+str(i)

def organizations(numOrgs):

    print "Organizations:\n"
    print "  - &OrdererOrg"
    print "    Name: OrdererOrg"
    print "    ID: OrdererMSP"
    print "    MSPDir: crypto-config/ordererOrganizations/example.com/msp\n"
    for i in range(1, numOrgs+1):
        print "  - &Org"+str(i)
        print "    Name: Org"+str(i)+"MSP"
        print "    ID: Org"+str(i)+"MSP"
        print "    MSPDir: crypto-config/peerOrganizations/org"+str(i)+".example.com/msp"
        print "    AnchorPeers:"
        print "      - Host: peer0.org"+str(i)+".example.com"
        print "        Port: 7051\n"

def orderer():

    print "Orderer: &OrdererDefaults"
    print "  OrdererType: solo"
    print "  Addresses:"
    print "    - orderer.example.com:7050"
    print "  BatchTimeout: 2s"
    print "  BatchSize:"
    print "    MaxMessageCount: 10"
    print "    AbsoluteMaxBytes: 99 MB"
    print "    PreferredMaxBytes: 512 KB"
    print "  Kafka:"
    print "    Brokers:"
    print "      - 127.0.0.1:9092"
    print "  Organizations:"

def application():

    print "Application: &ApplicationDefaults"
    print "  Organizations:"

#Main function
if __name__ == "__main__":

    profiles(int(sys.argv[1]))
    organizations(int(sys.argv[1]))
    orderer()
    application()
