# TrustAS · Hyperledger Network

*An example network for running TrustAS*

> This network is derived from the [Fabric-SDK-Py E2E test / example](https://github.com/hyperledger/fabric-sdk-py/blob/v0.7.0/test/integration/e2e_test.py).

> All commands are executed from the `src/` directory, unless specified otherwise.

------------------------------------------------------------------

### 0. <a name="preparing"></a>Preparing the environment

```sh
virtualenv --version        # 15.1.0

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### 1. Starting the network

```sh
./main.py
```

------------------------------------------------------------------

### Other operations

#### Open an interactive shell

```sh
docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls-cli.yaml run --rm cli
```


#### Real time logs
```sh
docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls-cli.yaml logs -f
```
Inside the container, explore the `scripts/` directory for commands to interact with fabric.


#### Run a specific test
```sh
python test/integration/e2e_test.py
```

------------------------------------------------------------------

### Issues

If you've encountered any issues regarding the Hyperledger network:
- Make sure `python -V` reports version `3.6.x`.
- Make sure you have [prepared your environment](#preparing).
- Evaluate if it could be a race condition. Try calling `time.sleep(5)` before a faulty chaincode operation.
