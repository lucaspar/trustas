#!/bin/bash

# Environment variables
NUM_ORGS=$1
EXPERIMENT=${NUM_ORGS}-ASes

# Exit in case of errors
set -e

# Create directory for the experiment
mkdir -p ../../experiments/

# Create directory for the experiment
echo "Creating directory ${DYNAMIX_DIR}/experiments/${EXPERIMENT}"
mkdir -p ../../experiments/${EXPERIMENT}

# Enter experiment directory
#echo "Entering directory ../../experiments/${EXPERIMENT}"
#cd ../../experiments/${EXPERIMENT}

# Generate crypto-config.yaml
echo "Generating cryto-config.yaml file"
python generateCryptoConfig.py $NUM_ORGS > ../../experiments/${EXPERIMENT}/crypto-config.yaml
# Generate configtx.yaml
echo "Generating configtx.yaml file"
python generateConfigtx.py $NUM_ORGS > ../../experiments/${EXPERIMENT}/configtx.yaml

# Configure FABRIC_CFG_PATH
export FABRIC_CFG_PATH=../../experiments/${EXPERIMENT}/

# Generate certifactes
echo "Generating certificates"
HLFConfig/cryptogen generate --config=./../../experiments/${EXPERIMENT}/crypto-config.yaml 
mv crypto-config/ ../../experiments/${EXPERIMENT}/

echo "Generating channel artifacts"
mkdir -p ../../experiments/${EXPERIMENT}/config
# Genesis block
echo "Generating genesis block"
HLFConfig/configtxgen -profile SingleOrgOrdererGenesis -outputBlock ./../../experiments/${EXPERIMENT}/config/genesis.block
# Channnel
echo "Creating channel"
HLFConfig/configtxgen -profile MultipleOrgChannel -outputCreateChannelTx ./../../experiments/${EXPERIMENT}/config/channel.tx -channelID mychannel
# Anchor peer update for each org
for (( ASN=1; ASN <= $NUM_ORGS; ASN++ )) do
    echo "Updating anchor peer for org $ASN" # TODO Repeat for all peers
    HLFConfig/configtxgen -profile MultipleOrgChannel -outputAnchorPeersUpdate ./../../experiments/${EXPERIMENT}/config/Org${ASN}MSPanchors.tx -channelID mychannel -asOrg Org${ASN}MSP
done

# Generate ca-file
echo "Generating CA config file"
mkdir -p ../../experiments/${EXPERIMENT}/ca-server-config
python generateCAConfig.py $NUM_ORGS > ../../experiments/${EXPERIMENT}/ca-server-config/fabric-ca-server-config.yaml

# Copy base files
echo "Copying experiment base files"
cp base/docker-compose-base.yml ../../experiments/${EXPERIMENT}
cp base/initExperiment.bash ../../experiments/${EXPERIMENT}
cp base/initPeer.bash ../../experiments/${EXPERIMENT}
cp base/initOrderer.bash ../../experiments/${EXPERIMENT}

# Print instructions
echo "Configuration files generated successfully!!!"
echo "Do not forget the commit the files to the repository!"
echo "To run the experiment, go to ../../experiments/${EXPERIMENT} and run ./initExperiment.bash ASN IP:PORT SERVICE INTENTFILE ORDERER_IP MODE"
echo "Then, on the (remote) peers, pull the git repository, go to ../../experiments/${EXPERIMENT} and run ./initPeer.bash ASN SERVICE INTENTFILE ORDERER_IP MODE REQUESTS INTERVAL"