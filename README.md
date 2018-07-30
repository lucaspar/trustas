# Paillier Chaincode
> Proof of Concept of Hyperledger Fabric Chaincode with Homomorphic Encryption using the Paillier Cryptosystem.

- [Hyperledger Fabric](https://github.com/hyperledger/fabric)
- [Paillier implementation used](https://github.com/didiercrunch/paillier)

### Operations allowed:

- Ciphertexts addition
- Ciphertext-scalar multiplication

### Execution

##### All terminals:

```sh

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
peer chaincode install -p chaincodedev/chaincode/pacc -n mycc -v 0
peer chaincode instantiate -n mycc -v 0 -c '{"Args":["a","10"]}' -C myc
peer chaincode invoke -n mycc -c '{"Args":["set", "a", "20"]}' -C myc
peer chaincode query -n mycc -c '{"Args":["query","a"]}' -C myc

```

### Extended operations

#### Handle external chaincode dependencies by using `govendor`:

```sh

sudo apt install govendor
govendor init
govendor add +external                  # Add all external packages, or
govendor add github.com/external/pkg    # Add specific external package

```
