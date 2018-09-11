Multiple Dynam-IX peers with shared containers
---------------------
This example consists of multiple Dynam-IX peers using the same set of containers to establish interconnection agreements. In practice this means that there is only one Hyperledger Fabric node running. Independent of this, this example can be used to test and implement any feature on Dynam-IX.

** Starting shared components and first Dynam-IX peer**

`cd 1-AS/` <br/>
`bash initExperiment.bash ASN IP:PORT SERVICE_DESCRIPTION INTENT_FILE ORDERER_IP MODE`, where: <br/>

* ASN: contains the Autonomous System Number (in this case, 1)
* IP:PORT: contains the IP of host and the PORT that it is going to be used by the Dynam-IX peer (e.g., 7052)
* SERVICE_DESCRIPTION: describes the type of service being offered by the AS (e.g., Transit)
* INTENT_FILE: path (relative to the src/ folder) to the intent file
* ORDERER_IP: IP address of the host running the ordering system (in this case, the same IP of the AS)
* MODE: regular or autonomous. In this example, the mode is regular.

** Starting additional Dynam-IX peers**

Open a new terminal and type:

`cd $DYNAMIX_DIR/src/` <br/>
`python dynamix.py ASN IP:PORT SERVICE_DESCRIPTION INTENT_FILE USER ORDERER_IP MODE`, where: <br/>

* ASN: must be specified as `AS2`, `AS3`, etc.
* USER: must be `org1`

Multiple Dynam-IX peers with individual containers
---------------------
Under construction.
