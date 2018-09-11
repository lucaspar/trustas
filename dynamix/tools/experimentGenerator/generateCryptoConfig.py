#!/usr/bin/python
import sys

def orderer():

    print "OrdererOrgs:"
    print "  - Name: Orderer"
    print "    Domain: example.com"
    print "    Specs:"
    print "      - Hostname: orderer"

def orgs(i):

    print "  - Name: Org"+str(i)
    print "    Domain: org"+str(i)+".example.com"
    print "    Template:"
    print "      Count: 1"
    print "    Users:"
    print "      Count: 1"

#Main function
if __name__ == "__main__":
    orderer()
    print "PeerOrgs:"
    for i in range(1,int(sys.argv[1])+1):
        orgs(i)