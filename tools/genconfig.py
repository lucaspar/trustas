#!/usr/bin/env python3
import os
import json

docker_compose_base = """# SPDX-License-Identifier: Apache-2.0
# Docker Compose - TrustAS configuration

version: '2' # v3 does not support 'extends' yet

services:
    orderer.example.com: # There can be multiple orderers
        extends:
            file: orderer-base.yaml
            service: orderer-base
        container_name: orderer.example.com
        hostname: orderer.example.com
        ports:
            - '7050:7050'
        volumes:
            - ./e2e_cli/channel-artifacts/orderer.genesis.block:/var/hyperledger/orderer/orderer.genesis.block
            - ./e2e_cli/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/msp:/var/hyperledger/orderer/msp
            - ./e2e_cli/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/:/var/hyperledger/orderer/tls
        command: orderer start

    cli:
        container_name: cli
        image: hyperledger/fabric-tools
        stdin_open: true
        tty: true
        environment:
            - GOPATH=/opt/gopath
            - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock
            - CORE_LOGGING_LEVEL=DEBUG
            - CORE_PEER_ID=cli
            - CORE_PEER_ADDRESS=peer0.org1.example.com:7051
            - CORE_PEER_LOCALMSPID=Org1MSP
            - CORE_PEER_TLS_ENABLED=true
            - CORE_PEER_TLS_CERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.crt
            - CORE_PEER_TLS_KEY_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.key
            - CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
            - CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
        working_dir: /opt/gopath/src/github.com/hyperledger/fabric/peer
        command: /bin/bash
        volumes:
            - /var/run/:/host/var/run/
            - ./e2e_cli/examples/chaincode/go/:/opt/gopath/src/github.com/hyperledger/fabric/examples/chaincode/go
            - ./e2e_cli/crypto-config:/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/
            - ./scripts:/opt/gopath/src/github.com/hyperledger/fabric/peer/scripts/
            - ./e2e_cli/channel-artifacts:/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts
        depends_on:
            - orderer.example.com
            - peer0.org1.example.com
"""

def build_docker_service(peer_name, port, gossip_peer):

    return "\n    " + peer_name + """:
        extends:
            file: peer-base.yaml
            service: peer-base
        container_name: """ + peer_name + """
        hostname: """ + peer_name + """
        environment:
            - CORE_PEER_ID=""" + peer_name + """
            - CORE_PEER_ADDRESS=""" + peer_name + """:7051
            - CORE_PEER_CHAINCODELISTENADDRESS=""" + peer_name + """:7052
            - CORE_PEER_LOCALMSPID=Org1MSP
            - CORE_PEER_GOSSIP_EXTERNALENDPOINT=""" + peer_name + """:7051
            - CORE_PEER_GOSSIP_BOOTSTRAP=""" + gossip_peer + """:7051
        volumes:
            - ./e2e_cli/crypto-config/peerOrganizations/org1.example.com/peers/""" + peer_name + """/msp:/etc/hyperledger/fabric/msp
            - ./e2e_cli/crypto-config/peerOrganizations/org1.example.com/peers/""" + peer_name + """/tls:/etc/hyperledger/fabric/tls
        ports:
            - """ + str(port) + """:7051
            - """ + str(port + 1) + """:7052
            - """ + str(port + 2) + """:7053
        command: peer node start
        """


def build_peer_desc(peer_name, peer_hostname, port):
    return {
        "url": peer_hostname + ":" + str(port),
        "eventUrl": peer_hostname + ":" + str(port + 2),
        "grpcOptions": {
            "ssl-target-name-override": peer_name,
            "grpc.http2.keepalive_time": 15
        },
        "tlsCACerts": {
            "path":
            "test/fixtures/e2e_cli/crypto-config/peerOrganizations/org1.example.com/peers/"
            + peer_name + "/msp/tlscacerts/tlsca.org1.example.com-cert.pem"
        }
    }

def main():

    FILES               = [3, 5, 10, 15, 25, 50, 75, 100]
    NUM_PEERS           = 100
    port_increment      = 100
    network_basefile    = "./network_base.json"
    network_desc        = {}

    with open(network_basefile, "r") as fp:
        network_desc = json.load(fp)

    print(network_desc)

    for peer_file in FILES:

        port = 7051
        content = docker_compose_base
        network_desc["organizations"]["org1.example.com"]["peers"] = []
        network_desc["peers"] = {}

        NUM_PEERS = peer_file
        base_dir = "../src/test/fixtures"
        docker_filename = os.path.join(base_dir, "dc-local-" + str(NUM_PEERS) + "peers.yaml")
        network_filename = os.path.join(base_dir, "local-" + str(NUM_PEERS) + "peers.json")

        for pidx in range(0, NUM_PEERS):

            peer_name       = "peer" + str(pidx) + ".org1.example.com"
            # gossip_peer     = "peer" + str((pidx + 1) % NUM_PEERS) + ".org1.example.com"
            gossip_peer     = "peer7.org1.example.com"
            peer_hostname   = "localhost"
            peer_service    = build_docker_service(peer_name, port, gossip_peer)
            peer_desc       = build_peer_desc(peer_name, peer_hostname, port)

            # append and increment
            content = content + peer_service
            network_desc["organizations"]["org1.example.com"]["peers"].append(peer_name)
            network_desc["peers"][peer_name] = peer_desc
            port = port + port_increment

        # create docker compose file
        print(content)
        with open(docker_filename, "w+") as fp:
            fp.write(content)

        # create network description file
        with open(network_filename, "w+") as fp:
            json.dump(network_desc, fp)

main()
