package main

import (
	"fmt"

	"github.com/hyperledger/fabric/core/chaincode/shim"
	"github.com/hyperledger/fabric/protos/peer"

	"crypto/rand"
	"github.com/didiercrunch/paillier"
	"math/big"
	"reflect"
)

func b(i int) *big.Int {
	return big.NewInt(int64(i))
}

func n(i *big.Int) int {
	return int(i.Int64())
}

func TestPaillier(x, y, k int) {

	fmt.Print("\n\tTesting Paillier homomorphic encryption scheme.\n\tAddition and scalar multiplication\n\n")

	tkh := paillier.GetThresholdKeyGenerator(10, 2, 2, rand.Reader)
	tpks, _ := tkh.Generate()

	plainText1 := b(x)
	plainText2 := b(y)

	cypher1, _ := tpks[0].Encrypt(plainText1, rand.Reader)
	cypher2, _ := tpks[1].Encrypt(plainText2, rand.Reader)

	cypher3 := tpks[0].Add(cypher1, cypher2)
	cypher4 := tpks[0].Mul(cypher3, b(k))

	share1 := tpks[0].Decrypt(cypher4.C)
	share2 := tpks[1].Decrypt(cypher4.C)

	combined, _ := tpks[0].CombinePartialDecryptions([]*paillier.PartialDecryption{share1, share2})

	expected := b((x + y) * k)

	if reflect.DeepEqual(combined, expected) {
		fmt.Printf("\tPASSED: (%d + %d) * %d = %s = %s\n\n", x, y, k, combined.String(), expected.String())
	} else {
		fmt.Printf("\tFAILED: expected %s, got %s", expected.String(), combined.String())
	}

}

// SimpleAsset implements a simple chaincode to manage an asset
type SimpleAsset struct {
}

// Init is called during chaincode instantiation to initialize any
// data. Note that chaincode upgrade also calls this function to reset
// or to migrate data, so be careful to avoid a scenario where you
// inadvertently clobber your ledger's data!
func (t *SimpleAsset) Init(stub shim.ChaincodeStubInterface) peer.Response {

	// Get the args from the transaction proposal
	args := stub.GetStringArgs()
	if len(args) != 2 {
		return shim.Error("Incorrect arguments. Expecting a key and a value")
	}

	// We store the key and the value on the ledger
	err := stub.PutState(args[0], []byte(args[1]))
	if err != nil {
		return shim.Error(fmt.Sprintf("Failed to create asset: %s", args[0]))
	}

	return shim.Success(nil)

}

// Invoke is called per transaction on the chaincode. Each transaction is
// either a 'get' or a 'set' on the asset created by Init function. The Set
// method may create a new asset by specifying a new key-value pair.
func (t *SimpleAsset) Invoke(stub shim.ChaincodeStubInterface) peer.Response {

	// Extract the function and args from the transaction proposal
	fn, args := stub.GetFunctionAndParameters()

	var result string
	var err error
	if fn == "set" {
		result, err = set(stub, args)
	} else {
		result, err = get(stub, args)
	}

	if err != nil {
		return shim.Error(err.Error())
	}

	// Return the result as success payload
	return shim.Success([]byte(result))
}

// Set stores the asset (both key and value) on the ledger. If the key exists,
// it will override the value with the new one
func set(stub shim.ChaincodeStubInterface, args []string) (string, error) {
	if len(args) != 2 {
		return "", fmt.Errorf("Incorrect arguments. Expecting a key and a value")
	}

	err := stub.PutState(args[0], []byte(args[1]))
	if err != nil {
		return "", fmt.Errorf("Failed to set asset: %s", args[0])
	}

	return args[1], nil
}

// Get returns the value of the specified asset key
func get(stub shim.ChaincodeStubInterface, args []string) (string, error) {
	if len(args) != 1 {
		return "", fmt.Errorf("Incorrect arguments. Expecting a key")
	}

	value, err := stub.GetState(args[0])
	if err != nil {
		return "", fmt.Errorf("Failed to get asset: %s with error: %s", args[0], err)
	}
	if value == nil {
		return "", fmt.Errorf("Asset not found: %s", args[0])
	}

	return string(value), nil
}

// Main function starts up the chaincode in the container during instantiate
func main() {

	TestPaillier(13, 19, 2)

	if err := shim.Start(new(SimpleAsset)); err != nil {
		fmt.Printf("Error starting SimpleAsset chaincode: %s", err)
	}
}
