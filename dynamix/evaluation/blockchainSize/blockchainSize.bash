#!/bin/bash

TRANSACTIONS=0
SIZE=$(docker exec -it couchdb-1 du -b data/ | tail -n 1 | cut -f 1)
echo $TRANSACTIONS $SIZE
TRANSACTIONS=$((TRANSACTIONS+1))

for (( AS=1; AS <= 1500; AS++ )) do
    # Register N ASes
    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp" cli peer chaincode invoke -o orderer.example.com:7050 -C mychannel -n dynamix -c '{"function":"registerAS","Args":["AS'"${AS}"'", "200.132.227.120:50000", "Transit Provider", "0", "0", "asihd9asjd98asud0asid0asdsajd08as8hd98asj0djsa0djas"]}'

    SIZE=$(docker exec -it couchdb-1 du -b data/ | tail -n 1 | cut -f 1)
    echo $TRANSACTIONS $SIZE
    TRANSACTIONS=$((TRANSACTIONS+1))
done

for (( T=1; T <= 2750; T++ )) do
    # Generate agreement ID
    IA=$(date +%s%N |md5sum)

    # Register Agreement
    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp" cli peer chaincode invoke -o orderer.example.com:7050 -C mychannel -n dynamix -c '{"function":"registerAgreement","Args":["IA-'"${IA}"'", "usahdiashmdiuuhasiudhasiudhasiuhdiusauhdiuashdiuashdiuasssaudhas", "AS1", "AS2", "uisaduihasiudhasiudhiuasuhdiuashdashdsaiudhiuashdas", "uisaduihasiudhasuhd12345678iuashdashdsaiudhiuashdas"]}'

    SIZE=$(docker exec -it couchdb-1 du -b data/ | tail -n 1 | cut -f 1)
    echo $TRANSACTIONS $SIZE
    TRANSACTIONS=$((TRANSACTIONS+1))

    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp" cli peer chaincode invoke -o orderer.example.com:7050 -C mychannel -n dynamix -c '{"function":"updateCustRep","Args":["AS1", "1"]}'

    SIZE=$(docker exec -it couchdb-1 du -b data/ | tail -n 1 | cut -f 1)
    echo $TRANSACTIONS $SIZE
    TRANSACTIONS=$((TRANSACTIONS+1))

    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp" cli peer chaincode invoke -o orderer.example.com:7050 -C mychannel -n dynamix -c '{"function":"updateProvRep","Args":["AS2", "1"]}'

    SIZE=$(docker exec -it couchdb-1 du -b data/ | tail -n 1 | cut -f 1)
    echo $TRANSACTIONS $SIZE
    TRANSACTIONS=$((TRANSACTIONS+1))
done
for (( T=1; T <= 125; T++ )) do

    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp" cli peer chaincode invoke -o orderer.example.com:7050 -C mychannel -n dynamix -c '{"function":"updateService","Args":["AS1", "Cloud Provider"]}'

    SIZE=$(docker exec -it couchdb-1 du -b data/ | tail -n 1 | cut -f 1)
    echo $TRANSACTIONS $SIZE
    TRANSACTIONS=$((TRANSACTIONS+1))

    docker exec -e "CORE_PEER_LOCALMSPID=Org1MSP" -e "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp" cli peer chaincode invoke -o orderer.example.com:7050 -C mychannel -n dynamix -c '{"function":"updateService","Args":["AS1", "Transit Provider"]}'

    SIZE=$(docker exec -it couchdb-1 du -b data/ | tail -n 1 | cut -f 1)
    echo $TRANSACTIONS $SIZE
    TRANSACTIONS=$((TRANSACTIONS+1))

done


