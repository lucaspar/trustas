#!/bin/bash
# Based on byfn.sh:
# https://github.com/hyperledger/fabric-samples/blob/release/first-network/byfn.sh

echo "Cleaning docker environment"

function clearContainers () {
    CONTAINER_IDS=$(docker ps -aq)
    if [ -z "$CONTAINER_IDS" -o "$CONTAINER_IDS" == " " ]; then
        echo "---- No containers available for deletion ----"
    else
        docker rm -f $CONTAINER_IDS
    fi
}

function removeUnwantedImages() {
    DOCKER_IMAGE_IDS=$(docker images | grep "dev\|none\|test-vp\|peer[0-9]-" | awk '{print $3}')
    if [ -z "$DOCKER_IMAGE_IDS" -o "$DOCKER_IMAGE_IDS" == " " ]; then
        echo "---- No images available for deletion ----"
    else
        docker rmi -f $DOCKER_IMAGE_IDS
    fi
}

clearContainers
removeUnwantedImages
# remove orderer block and other channel configuration transactions and certs
# rm -rf channel-artifacts/*.block channel-artifacts/*.tx crypto-config

exit 0
