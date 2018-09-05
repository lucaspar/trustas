# Paillier Chaincode
> Proof of Concept of Hyperledger Fabric Chaincode with Homomorphic Encryption using the Paillier Cryptosystem.

- [Hyperledger Fabric](https://github.com/hyperledger/fabric)
- [Paillier implementation used (Go)](https://github.com/didiercrunch/paillier)

### Operations allowed:

- Ciphertexts addition
- Ciphertext-scalar multiplication

### Versions

Tested with:

Software        | Version
--------------- | -----------
OS              | Ubuntu 18.04.1 LTS
Go              | 1.10.3
Hyperledger     | 1.2.0
Docker          | 18.06.0-ce
Docker Compose  | 1.21.2

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
git clone https://github.com/lucaspar/trustas
cd trustas
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
cd trustas
go build
CORE_PEER_ADDRESS=peer:7051 CORE_CHAINCODE_ID_NAME=mycc:0 ./trustas

```

##### Terminal 3 - Install, instantiate, invoke, and query chaincode

```sh

docker exec -it cli bash
cd /opt/gopath/src
peer chaincode install -p chaincodedev/chaincode/trustas -n mycc -v 0
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
vim Gomfile         # IMPORTANT: remove hyperledger deps from `Gomfile`
gom install         # install vendor dependencies
gom build           # and test it

```

### Common Issues

#### Package / library missing

Try removing the problematic dependency from `vendor` directory. If using Gom, comment it out in the Gom

Explanation: It forces Go to look for it in `$GOPATH` and `$GOROOT`.

### Integridade utilizando Pedersen commitments:

Sendo $ x $ um valor como latência observada, é desejado o valor de $ s_x = x_1 + x_2 + ... + x_n $ representando a latência de diversos contratos e/ou medições ao longo do tempo.

Considerando que a informação armazenada é cifrada com o Pedersen commitment:

$$ cm_i = g^x_i h^r_i $$

São conhecidos por todos os valores de $g$ e $h$.
$x$ representa a informação original e $r$ um valor aleatório do commitment.

Considerando que os textos cifrados são publicamente armazenados, um verificador pode calcular $ cm = cm_1 \cdot cm_2 \cdot \cdot \cdot cm_n $ sem depender do provador e posteriormente verificar que uma soma $ s_x = \sum_{i=1}^{n}{x_i} $ enviada pelo provador é verdadeiro quando este também lhe enviar $ s_r = \sum_{i=1}^{n}{r_i} $ mantendo a igualdade:

$$ cm = g^{sx} h^{sr} = \prod_{i=1}^{n}{cm_i} $$

Já que:
$ cm = cm_1 \cdot cm_2 \cdot \cdot \cdot cm_n $
$ cm = ( g^{x_1} h^{r_1} )( g^{x_2} h^{r_2} ) \cdot \cdot \cdot ( g^{x_n} h^{r_n} ) $
$ cm = g^{x_1 + ... + x_n} h^{r_1 + ... + r_n} $
$ cm = g^{sx} h^{sr} $
