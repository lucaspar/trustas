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
pip install -r requirements.txt
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
#   You will see an error when executing before starting a network
watch docker logs -tf dev-peer0.org1.example.com-trustas_cc-1.0

# Alternatively, you can save the chaincode output to file after an execution
docker logs -tf dev-peer0.org1.example.com-trustas_cc-1.0 > logs/cc.$(date "%s").log
```

### Starting the network

```sh
./main.py
```

------------------------------------------------------------------


## Hyperledger Explorer for visualization (_deprecated_)

#### Hyperledger Explorer dependencies

```sh
# install postgres and create user for explorer
sudo apt install postgresql postgresql-contrib
sudo -u postgres createuser hypex
sudo -u postgres createdb fabricexplorer
sudo -u postgres psql
postgres=# alter user hypex with encrypted password 'password'
postgres-# grant all privileges on database fabricexplorer to hypex
postgres-# \q

```
#### Get and execute Hyperledger Explorer
```sh
git clone https://github.com/hyperledger/blockchain-explorer.git
cd blockchain-explorer/app/persistence/fabric/postgreSQL/db
sudo -u postgres psql -v dbname=fabricexplorer -v user=hypex -v passwd=8bfcd2f4a91e -f ./explorerpg.sql
sudo -u postgres psql -v dbname=fabricexplorer -v user=hypex -v passwd=8bfcd2f4a91e -f ./updatepg.sql
```

Follow the Hyperledger Explorer readme to:
- Configure the network
- Build and execute it

After that, visualize the network at [localhost:8080](http://localhost:8080) by default.

------------------------------------------------------------------

### Other operations


#### Open an interactive shell
```sh
docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls-cli.yaml run --rm cli
```
Inside the container, explore the `scripts/` directory for commands to interact with fabric.


#### Real time logs
You can check the files at `logs/`, or:
```sh
docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls-cli.yaml logs -f
```


#### Run a specific test
```sh
python test/integration/e2e_test.py
```

------------------------------------------------------------------

## Issues

If you've encountered any issues regarding the Hyperledger network:

1. **Follow this readme** and [prepare your environment](#preparing) first.
2. Eliminate the **"works on my machine"** scenarios:
    - **Race conditions** - try calling `time.sleep(5)` before a faulty chaincode operation.
    - **Divergent versions** - see the [root readme](../README.md) for dependencies.
3. Check the **logs** - in `logs/` (duh)
    - Look for `ERRO(R)` and `WARN(ING)`
    - Check the [chaincode output](#cc_out) if chaincode has been modified
4. Pray for a miracle
