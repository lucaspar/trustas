# TrustAS · Hyperledger Network

*An example network for running TrustAS*

> This network is derived from the [Fabric-SDK-Py E2E test / example](https://github.com/hyperledger/fabric-sdk-py/blob/v0.7.0/test/integration/e2e_test.py).

### <a name="preparing"></a>Preparing the environment

```sh
virtualenv --version        # 15.1.0
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Starting the network

```sh
python network/start.py
```

### Testing

#### Running a specific test

```sh
python test/integration/e2e_test.py
```

### Issues

If you've encountered any issues regarding the Hyperledger network:
- Make sure `python -V` reports version `3.6.x`.
- Make sure you have [prepared your environment](#preparing).
- Evaluate if it could be a race condition. Try calling `time.sleep(5)` before a faulty chaincode operation.
