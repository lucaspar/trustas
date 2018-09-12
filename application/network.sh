docker pull hyperledger/fabric-peer:latest
docker pull hyperledger/fabric-orderer:latest
docker pull hyperledger/fabric-ca:latest
docker pull hyperledger/fabric-ccenv:latest
docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls.yaml up
