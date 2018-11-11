#!/bin/bash

# Automatically creates instances in Google Cloud Platform.
# WARNING:  This script will operate on your GCP account and may
#           allocate resources that will incur expenses to your
#           billing account. Run it at your own risk.
#
# Prerequisites:
#   - Log in to gcloud cli
#   - Have an orderer snapshot named $SNAPSHOT_ORD
#   - Have an AS snapshot named $SNAPSHOT_ASN

# Minimal config:
# Orderer and CA + as000 + as001

# set -e

SNAPSHOT_ORD=orderer    # snapshot name for orderer instance
SNAPSHOT_ASN=asn        # snapshot name for AS instances
INSTANCE_ORD=orderer    # orderer instance name
NUMBER_OF_ASES=2        # quantity of AS instances in the network

id=0

# Create resources for the ASN provided
CreateAS () {
    arg_asn=$1
    arg_id=$2
    echo Creating $arg_asn

    # CREATE IP ADDRESS
    gcloud compute addresses create $arg_asn \
        --region us-east1 \
        --subnet default \
        --addresses 10.142.0.$((arg_id + 3))

    # CREATE DISK
    gcloud compute disks create $arg_asn-disk \
        --labels app=trustas,experiment=b \
        --size 10GB \
        --source-snapshot $SNAPSHOT_ASN \
        --type pd-ssd

    # CREATE INSTANCE
    gcloud compute instances create $arg_asn \
        --labels app=trustas,experiment=b \
        --zone us-east1-b \
        --machine-type g1-small \
        --private-network-ip $arg_asn \
        --disk name=$arg_asn-disk,boot=yes,auto-delete=yes

    # SET ENVIRONMENT VARIABLES
    gcloud compute instances add-metadata $arg_asn \
        --metadata asn=$arg_asn

    echo Successfully created $arg_asn

}

# Remove resources of the ASN provided
CleanResources () {
    arg_asn=$1
    gcloud compute instances delete $arg_asn
    gcloud compute disks delete $arg_asn-disk
    gcloud compute addresses delete $arg_asn
}

while [ $id -lt $NUMBER_OF_ASES ]; do

    asn=peer$id
    # CleanResources $asn
    CreateAS $asn $id &
    id=$((id + 1))

done
