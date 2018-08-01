# Paillier Chaincode
> Proof of Concept of Hyperledger Fabric Chaincode with Homomorphic Encryption using the Paillier Cryptosystem.

- [Hyperledger Fabric](https://github.com/hyperledger/fabric)
- [Paillier implementation used (Go)](https://github.com/didiercrunch/paillier)

### Operations allowed:

- Ciphertexts addition
- Ciphertext-scalar multiplication

### Requirements

1. [Install Go](https://golang.org/doc/install)

2. Clone Hyperledger Fabric samples
```sh
git clone -b master https://github.com/hyperledger/fabric-samples.git
cd fabric-samples
```

3. Clone this repo and fetch all dependencies
```sh
cd ~/go/src     # or $GOPATH/src
git clone https://github.com/lucaspar/pacc
cd pacc
govendor fetch +outside
```

### Execution

##### All 3 terminals:

```sh
# from Hyperledger Fabric samples directory (see requirements above):
cd chaincode-docker-devmode

```

##### Terminal 1 - Start Fabric network

```sh

docker-compose -f docker-compose-simple.yaml up

```

##### Terminal 2 - Run chaincode

```sh

docker exec -it chaincode bash
cd pacc
go build
CORE_PEER_ADDRESS=peer:7051 CORE_CHAINCODE_ID_NAME=mycc:0 ./pacc

```

##### Terminal 3 - Install, instantiate, invoke, and query chaincode

```sh

docker exec -it cli bash
cd /opt/gopath/src
peer chaincode install -p chaincodedev/chaincode/pacc -n mycc -v 0
peer chaincode instantiate -n mycc -v 0 -c '{"Args":["a","10"]}' -C myc
peer chaincode invoke -n mycc -c '{"Args":["set", "a", "20"]}' -C myc
peer chaincode query -n mycc -c '{"Args":["query","a"]}' -C myc

```

### Extended operations

#### Handling external chaincode dependencies

##### Using `govendor`:

```sh
# if govendor is not installed:
sudo apt install govendor

govendor init
govendor add +external                  # Add all external packages, or
govendor add github.com/external/pkg    # Add specific external package

```

#####  Using `gom`:

```sh
# if gom is not installed:
go get github.com/mattn/gom

gom gen gomfile
vim Gomfile         # remove hyperledger deps from `Gomfile`
gom install         # install vendor dependencies
gom build           # and test it

```

### Common Issues

#### "Cannot find package 'plugin' in any of:"

**Temporary solution:**

> Rename 'vendor' directory to something else (this won't work with external deps, a permanent solution is still needed).
