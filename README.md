# TrustAS
> Establishing trust among autonomous systems

## Software versions

Software        | Version
--------------- | -----------
OS              | Ubuntu 18.04.1 LTS
[Go](https://golang.org/doc/install)                                | 1.10.3
[Hyperledger](https://hyperledger-fabric.readthedocs.io/en/release-1.2/getting_started.html)    | 1.2.0
[Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)   | 18.06.0-ce
[Docker Compose](https://docs.docker.com/compose/install/)          | 1.21.2
[Fabric-SDK-Py](https://github.com/hyperledger/fabric-sdk-py)       | 0.7.0

## Requirements

1. [Install Go](https://golang.org/doc/install)

2. Clone Hyperledger Fabric samples
```sh
git clone -b master https://github.com/hyperledger/fabric-samples.git
cd fabric-samples
```

3. Clone this repo and fetch all dependencies
```sh
cd ~/go/src     # or $GOPATH/src
git clone https://github.com/lucaspar/trustas
cd trustas
```

## Getting Started

```sh
cd application
./network.sh
```

In another terminal:
```sh
docker-compose up
```

## Getting Started [OLD]

#### All 3 terminals:

```sh
# from Hyperledger Fabric samples directory (see requirements above):
cd chaincode-docker-devmode

```

#### Terminal 1 - Start Fabric network

```sh

docker-compose -f docker-compose-simple.yaml up

```

#### Terminal 2 - Run chaincode

```sh

docker exec -it chaincode bash
cd trustas
go build
CORE_PEER_ADDRESS=peer:7051 CORE_CHAINCODE_ID_NAME=mycc:0 ./trustas

```

#### Terminal 3 - Install, instantiate, invoke, and query chaincode

```sh

docker exec -it cli bash
cd /opt/gopath/src
peer chaincode install -p chaincodedev/chaincode/trustas -n mycc -v 0
peer chaincode instantiate -n mycc -v 0 -c '{"Args":["a","10"]}' -C myc
peer chaincode invoke -n mycc -c '{"Args":["set", "a", "20"]}' -C myc
peer chaincode query -n mycc -c '{"Args":["query","a"]}' -C myc

```

## Extended operations

### Handling chaincode dependencies with `gom`:

```sh
# if gom is not installed:
go get github.com/mattn/gom

gom gen gomfile
vim Gomfile         # IMPORTANT: remove hyperledger deps from `Gomfile`
gom install         # install vendor dependencies
gom build           # and test it

```

## Common Issues

### Package / library missing

Try removing the problematic dependency from `vendor` directory. If using Gom, comment it out in the Gom

Explanation: It forces Go to look for it in `$GOPATH` and `$GOROOT`.
