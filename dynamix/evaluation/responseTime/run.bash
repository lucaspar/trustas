#!/bin/bash

export HOST_FILE=$1
export KEY_PATH=$2
export ORDERER_IP=$3
export REQUESTS=$4
export SLEEP=$5

# AS 1 is manually initialized
AS=2

# Read files containing one IP per line
while IFS='' read -r line || [[ -n "$line" ]]; do

    # Verify if the system is using eth0 as primary network interface (Dynam-IX gets the peer IP from this interface)
    #rsh  -i "${KEY_PATH}" ubuntu@${line} "ifconfig eth0 | grep \"inet addr\" | cut -d ':' -f 2 | cut -d ' ' -f 1" &
    # Kill any dynamix instance
    #rsh -i "${KEY_PATH}" ubuntu@${line} "pkill -f dynamix.py" &
    # Verify if Dynam-IX is running
    #rsh  -i "${KEY_PATH}" ubuntu@${line} "ps aux |grep dynamix" &
    # Update the repository
    #rsh -i "${KEY_PATH}" ubuntu@${line} "cd dynam-ix ; git pull" &
    # Remove logs from previous experiments
    #rsh -i "${KEY_PATH}" ubuntu@${line} "cd dynam-ix/src ; rm  *.log" &
    # Start Dynam-IX
    rsh -i "${KEY_PATH}" ubuntu@${line} "cd dynam-ix/evaluation/responseTime/200-ASes-60-tpb-15s-timeout ; ./initPeer.bash ${AS} Transit intents.json ${ORDERER_IP} autonomous ${REQUESTS} ${SLEEP}" &
    # Copy the execution logs
    #scp -i "${KEY_PATH}" ubuntu@${line}:/home/ubuntu/dynam-ix/src/AS*.log .

    AS=$((AS+1))

done < $HOST_FILE