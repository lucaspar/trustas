# TrustAS · Hyperledger Network

_An example network for running TrustAS_

> This network is derived from the [Fabric-SDK-Py E2E test / example](https://github.com/hyperledger/fabric-sdk-py/blob/v0.7.0/test/integration/e2e_test.py).

> All commands are executed from the `src/` directory, unless specified otherwise.

------------------------------------------------------------------

### <a name="preparing"></a>Preparing the environment

```sh
virtualenv --version        # 15.1.0 | sudo -H pip3 install virtualenv

virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
# try prepending "sudo -H " if you've got a permission error
```

### Setting up monitors (optional)

Terminal 1 - Containers live stream
```sh
docker stats
```

<a name="cc_out"></a>
Terminal 2 - Chaincode output watcher
```sh
# You can watch the logs in real time
#   An error is expected when executing before starting the network
watch docker logs -tf --tail 30 dev-peer0.org1.example.com-trustas_cc-1.0

# Alternatively, you can save the chaincode output to file after an execution
docker logs -tf dev-peer0.org1.example.com-trustas_cc-1.0 > logs/cc.$(date "%s").log
```

### Starting the network

```sh
./main.py
```

------------------------------------------------------------------

### Other operations

#### TrustAS usage
```sh
./main.py -h
```

#### Open an interactive shell
```sh
docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls-cli.yaml run --rm cli
```
Inside the container, explore the `scripts/` directory for commands to interact with fabric.

#### Monitor logs
You can check the files at `logs/`, or:
```sh
docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls-cli.yaml logs -f
```

#### Monitor blockchain size on disk
_Replace `businesschannel` with the channel name_
```sh
watch -n1 docker exec -it peer0.org1.example.com du -h /var/hyperledger/production/ledgersData/chains/chains/businesschannel

# OR

docker exec -it peer0.org1.example.com /bin/bash
cd /var/hyperledger/production/ledgersData/chains/chains
watch du -h businesschannel
```

#### Run a specific test
```sh
python test/integration/e2e_test.py
```

#### Generate channel artifacts
```sh
set -e
configtxgen --version   # v1.3.0
mkdir -p channel-artifacts

configtxgen -channelID businesschannel -profile TrustASChannel -outputBlock channel-artifacts/orderer.genesis.block -outputCreateChannelTx channel-artifacts/channel.tx
COUNTER=1
while [  $COUNTER -le 200 ]; do
    # echo $COUNTER
    configtxgen -outputAnchorPeersUpdate "channel-artifacts/Org"$COUNTER"MSPanchors.tx" -profile TrustASChannel -asOrg "Org"$COUNTER"MSP"
    let COUNTER=COUNTER+1
done
```

------------------------------------------------------------------

## Issues

If you've encountered any issues regarding the Hyperledger network:

0. If it was working before, check the **Common Error Messages** below.
1. **Follow this readme** and [prepare your environment](#preparing) first.
2. Eliminate the **"works on my machine"** scenarios:
    - **Race conditions** - try calling `time.sleep(5)` before a faulty chaincode operation.
    - **Divergent versions** - see the [root readme](../README.md) for dependencies.
3. Check the **logs** - in `logs/` (duh)
    - Look for `ERRO(R)` and `WARN(ING)`
    - Check the [chaincode output](#cc_out) if chaincode has been modified
4. Pray for a miracle

## Common Error Messages

> TypeError: '_Rendezvous' object does not support indexing

The chaincode may have returned an error. Could simply be an yet-to-be-created asset when it was queried. Try adding a sleep after creating it, so the orderer has some time to do its job.

For more insight, check the main log at `logs/main.log`. An error may look like this:
```log
DEBUG:hfc.util.utils:<_Rendezvous of RPC that terminated with:
	status = StatusCode.UNKNOWN
	details = "chaincode error (status: 500, message: {"Error":"Agreement aid_p1234567890 does not exist"})"
	debug_error_string = "{"created":"@1539665957.387897414","description":"Error received from peer","file":"src/core/lib/surface/call.cc","file_line":1099,"grpc_message":"chaincode error (status: 500, message: {"Error":"Agreement aid_p1234567890 does not exist"})","grpc_status":2}"
>
```

---

> raise Empty; queue.Empty

As of November 2018, the most recent release of the `fabric-sdk-py` -- the python HFC SDK `v0.7.0` -- had many hard-coded timeouts that may raise empty queue exceptions when expired. The timeouts are more likely to happen at the first execution because that is when the Docker images are first downloaded, thus increasing the preparation time for a first run.

A **temporary** solution is to modify the corresponding lines in the dependency source code.
For example, considering the following traceback:

```sh
Traceback (most recent call last):
  # [...]
  File "/home/user/trustas/src/venv/lib/python3.6/site-packages/hfc/util/utils.py", line 371, in build_tx_req
    res = q.get(timeout=10)
  File "/usr/lib/python3.6/queue.py", line 172, in get
    raise Empty
queue.Empty
```

Increase the timeout in the line 371 of the file in the traceback: `/home/user/trustas/src/venv/lib/python3.6/site-packages/hfc/util/utils.py`
```py
    res = q.get(timeout=3600)
```

You can probably modify it back after the first successful execution.
