Orderer running in conjunction with a peer
-------------
This examples consists of a scenario with 3 ASes running in different hosts. In this example, one of the ASes is also running the Hyperledger Fabric ordering system.

**AS 1 (will also run the ordering system)**

`cd 3-ASes-joint-orderer/` <br/>
`bash initExperiment.bash ASN IP:PORT SERVICE_DESCRIPTION INTENT_FILE ORDERER_IP MODE`, where: <br/>

* ASN: contains the Autonomous System Number (in this case, 1)
* IP:PORT: contains the IP of host and the PORT that it is going to be used by the Dynam-IX peer (e.g., 7052)
* SERVICE_DESCRIPTION: describes the type of service being offered by the AS (e.g., Transit)
* INTENT_FILE: path (relative to the src/ folder) to the intent file
* ORDERER_IP: IP address of the host running the ordering system (in this case, the same IP of the AS)
* MODE: regular or autonomous. In this example, the mode is regular.

**ASes 2 and 3**

`cd 3-ASes-joint-orderer/` <br/>
`bash initPeer.bash ASN SERVICE_DESCRIPTION INTENT_FILE ORDERER_IP MODE`<br/>

Orderer running in a separeted host
---------------------

This examples consists of a scenario with 3 ASes, running in different hosts and an additional host running the Hyperledger Fabric ordering system.

**Ordering system host**

`cd 3-ASes-independent-orderer/` <br/>
`bash initOrderer.bash` <br/>

**AS 1**

`cd distributed/3-ASes-independent-orderer/` <br/>
`bash initExperiment.bash ASN IP:PORT SERVICE_DESCRIPTION INTENT_FILE ORDERER_IP MODE`, where: <br/>

* ASN: contains the Autonomous System Number (in this case, 1)
* IP:PORT: contains the IP of host and the PORT that it is going to be used by the Dynam-IX peer (e.g., 7052)
* SERVICE_DESCRIPTION: describes the type of service being offered by the AS (e.g., Transit)
* INTENT_FILE: path (relative to the src/ folder) to the intent file
* ORDERER_IP: IP address of the host running the ordering system (in this case, the same IP of the AS)
* MODE: regular or autonomous. In this example, the mode is regular.

**ASes 2 and 3**

`cd 3-ASes-independent-orderer/` <br/>
`bash initPeer.bash ASN SERVICE_DESCRIPTION INTENT_FILE ORDERER_IP MODE`<br/>
