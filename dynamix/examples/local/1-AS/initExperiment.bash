#!/bin/bash

# Environment variables
export AS=$1               #1234
export ADDRESS=$2          #10.0.0.1:5000
export SERVICE=$3          #"Transit Provider"
export INTENT_FILE=$4      #/path/to/intent/file
export ORDERER_IP=$5       #192.168.1.130
export MODE=$6
export USER="org${AS}"
export COMPOSE_PROJECT_NAME="net"

# Exit in case of errors
#set -e

# Erase previous CA-Server DB
sudo rm ca-server-config/fabric-ca-server.db

# Getting KEYFILE
echo "Getting KEYFILE"
cd crypto-config/peerOrganizations/org${AS}.example.com/ca/
export KEYFILE=$(ls *_sk) 
cd ../../../../

# Cleaning any previous experiment
echo "Cleaning docker environment"
docker rm -f $(docker ps -aq)
docker rmi $(docker images dev-* -q)
docker network prune -f
docker-compose -f docker-compose-base.yml down

# Start Docker Containers
echo "Staring docker containers"
docker-compose -f docker-compose-base.yml up -d peer ca couchdb cli orderer

# Create channel
echo "Creating channel"
docker exec -e "CORE_PEER_LOCALMSPID=Org${AS}MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org${AS}.example.com/msp" peer0.org${AS}.example.com peer channel create -o orderer.example.com:7050 -c mychannel -f /etc/hyperledger/configtx/channel.tx

# Copy genesis block to shared area
echo "Copying block"
docker exec -e "CORE_PEER_LOCALMSPID=Org${AS}MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org${AS}.example.com/msp" peer0.org${AS}.example.com cp mychannel.block /etc/hyperledger/configtx/

# Do not forget to push the genesis block to the repository. You only need to do this on the first time

sleep 10

# Join channel
echo "Joining channel"
docker exec -e "CORE_PEER_LOCALMSPID=Org${AS}MSP" -e "CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/msp/users/Admin@org${AS}.example.com/msp" peer0.org${AS}.example.com peer channel join -b /etc/hyperledger/configtx/mychannel.block

# Install chaincode
echo "Installing chaincode"
docker exec -e "CORE_PEER_LOCALMSPID=Org${AS}MSP" -e "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org${AS}.example.com/users/Admin@org${AS}.example.com/msp" cli peer chaincode install -n dynamix -v 1.0 -p github.com/
# Instantiate chaincode
echo "Instantiating chaincode"
docker exec -e "CORE_PEER_LOCALMSPID=Org${AS}MSP" -e "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org${AS}.example.com/users/Admin@org${AS}.example.com/msp" cli peer chaincode instantiate -o orderer.example.com:7050 -C mychannel -n dynamix -v 1.0 -c '{"Args":[""]}'
# Init (Invoke) chaincode
sleep 10
echo "Invoking chaincode"
docker exec -e "CORE_PEER_LOCALMSPID=Org${AS}MSP" -e "CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org${AS}.example.com/users/Admin@org${AS}.example.com/msp" cli peer chaincode invoke -o orderer.example.com:7050 -C mychannel -n dynamix -c '{"function":"initLedger","Args":[""]}'

# Dynam-IX
echo "Entering Dynam-IX directory"
cd ../../../src

# Install node depencies
echo "Installing dependencies"
npm install

# Remove previous keys
echo "Cleaning previous keys"
rm -rf js/hfc-key-store/

# Enroll admin user
echo "Creating admin"
node js/enrollAdmin.js Org${AS}MSP

# Register regular user
echo "Registering user"
node js/registerUser.js org${AS} Org${AS}MSP

# Run Dynam-IX
echo "Starting Dynam-IX with $AS, $ADDRESS, $SERVICE, $INTENT_FILE, $USER, $ORDERER_IP $MODE"
python dynamix.py AS${AS} $ADDRESS $SERVICE $INTENT_FILE $USER $ORDERER_IP $MODE
