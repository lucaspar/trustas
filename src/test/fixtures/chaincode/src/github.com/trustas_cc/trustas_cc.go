/*
Copyright IBM Corp. 2016 All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

		 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package main

import (
	"encoding/json"
	"fmt"
	"strconv"
	// "strings"
	"time"

	"github.com/hyperledger/fabric/core/chaincode/shim"
	pb "github.com/hyperledger/fabric/protos/peer"
)

// SimpleChaincode : example of chaincode implementation.
// =============================================================================
type SimpleChaincode struct {
}

// Agreement : describes an agreement between two peers.
// =============================================================================
type Agreement struct {
	ID         string `json:"id"`        // unique agreement identifier
	ObjectType string `json:"docType"`   // docType is used to distinguish the various types of objects in state database
	SLA        string `json:"sla"`       // the service level agreement
	Asn1       int    `json:"asnOne"`    // one peer's ASN
	Asn2       int    `json:"asnTwo"`    // another peer's ASN
	Timestamp  int64  `json:"timestamp"` // UTC timestamp of creation
}

// Measurement : describes a set of metrics measured during an agreement.
// =============================================================================
type Measurement struct {
	MID        string `json:"id"`        // unique identifier of this measurement
	AID        string `json:"aid"`       // unique identifier of corresponding agreement
	ObjectType string `json:"docType"`   // docType is used to distinguish the various types of objects in state database
	Metrics    string `json:"metrics"`   // set of measured metrics
	Timestamp  int64  `json:"timestamp"` // UTC timestamp of creation
}

// Init : chaincode initialization / reset.
// =============================================================================
func (t *SimpleChaincode) Init(stub shim.ChaincodeStubInterface) pb.Response {
	fmt.Println("TrustAS Init")
	_, args := stub.GetFunctionAndParameters()
	var A, B string    // Entities
	var Aval, Bval int // Asset holdings
	var err error

	if len(args) != 4 {
		return shim.Error("Incorrect argument numbers. Expecting 4")
	}

	// Initialize the chaincode
	A = args[0]
	Aval, err = strconv.Atoi(args[1])
	if err != nil {
		return shim.Error("Expecting integer value for asset holding")
	}
	B = args[2]
	Bval, err = strconv.Atoi(args[3])
	if err != nil {
		return shim.Error("Expecting integer value for asset holding")
	}
	fmt.Printf("Aval = %d, Bval = %d\n", Aval, Bval)

	// Write the state to the ledger
	err = stub.PutState(A, []byte(strconv.Itoa(Aval)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(B, []byte(strconv.Itoa(Bval)))
	if err != nil {
		return shim.Error(err.Error())
	}

	return shim.Success(nil)
}

// Invoke : executed on chaincode invocations.
// =============================================================================
func (t *SimpleChaincode) Invoke(stub shim.ChaincodeStubInterface) pb.Response {
	fmt.Println("TrustAS Invoke")
	function, args := stub.GetFunctionAndParameters()
	if function == "invoke" {
		// Make payment of X units from A to B
		return t.invoke(stub, args)
	} else if function == "delete" {
		// Deletes an entity from its state
		return t.delete(stub, args)
	} else if function == "query" {
		// Queries chaincode
		return t.query(stub, args)
	} else if function == "createAgreement" {
		// Create an agreement in the chaincode
		return t.createAgreement(stub, args)
	} else if function == "queryAgreement" {
		// Create an agreement in the chaincode
		return t.queryAgreement(stub, args)
	} else if function == "publishMeasurement" {
		// Publish an agreement measurement to the chaincode
		return t.publishMeasurement(stub, args)
	}

	return shim.Error("Invalid invoke function name. Expecting \"invoke\", \"delete\", \"query\", \"createAgreement\", or \"queryAgreement\"")
}

// Represents a regular transaction of X units from A to B
// =============================================================================
func (t *SimpleChaincode) invoke(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var A, B string    // Entities
	var Aval, Bval int // Asset holdings
	var X int          // Transaction value
	var err error

	if len(args) != 3 {
		return shim.Error("Incorrect number of arguments. Expecting 3")
	}

	A = args[0]
	B = args[1]

	// Get the state from the ledger
	// TODO: will be nice to have a GetAllState call to ledger
	Avalbytes, err := stub.GetState(A)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Avalbytes == nil {
		return shim.Error("Entity not found")
	}
	Aval, _ = strconv.Atoi(string(Avalbytes))

	Bvalbytes, err := stub.GetState(B)
	if err != nil {
		return shim.Error("Failed to get state")
	}
	if Bvalbytes == nil {
		return shim.Error("Entity not found")
	}
	Bval, _ = strconv.Atoi(string(Bvalbytes))

	// Perform the execution
	X, err = strconv.Atoi(args[2])
	if err != nil {
		return shim.Error("Invalid transaction amount, expecting a integer value")
	}
	Aval = Aval - X
	Bval = Bval + X
	fmt.Printf("Aval = %d, Bval = %d\n", Aval, Bval)

	// Write the state back to the ledger
	err = stub.PutState(A, []byte(strconv.Itoa(Aval)))
	if err != nil {
		return shim.Error(err.Error())
	}

	err = stub.PutState(B, []byte(strconv.Itoa(Bval)))
	if err != nil {
		return shim.Error(err.Error())
	}

	return shim.Success(nil)
}

// Make Timestamp - creates a timestamp in ms
// ============================================================================================================================
func makeTimestamp() int64 {
	return time.Now().UnixNano() / (int64(time.Millisecond) / int64(time.Nanosecond))
}

// Creates an interconnection agreement between A and B
// =============================================================================
func (t *SimpleChaincode) createAgreement(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var AID string     // Agreement ID
	var Asn1, Asn2 int // ASes
	var SLA string     // Agreement SLA
	var err error

	// retrieve args
	if len(args) != 4 {
		return shim.Error("Incorrect number of arguments. Expecting 4")
	}
	AID = args[0]
	Asn1, err = strconv.Atoi(args[1])
	if err != nil {
		return shim.Error("2nd argument must be a numeric string (ASN)")
	}
	Asn2, err = strconv.Atoi(args[2])
	if err != nil {
		return shim.Error("3rd argument must be a numeric string (ASN)")
	}
	SLA = args[3]

	fmt.Println("Creating agreement", AID)

	var agreement Agreement
	agreement.ObjectType = "Peering"
	agreement.Timestamp = makeTimestamp()
	agreement.Asn1 = Asn1
	agreement.Asn2 = Asn2
	agreement.SLA = SLA
	agreement.ID = AID

	// Checks whether the agreement exists
	Agr, err := stub.GetState(AID)
	if err != nil {
		fmt.Println("Failed checking agreement")
		return shim.Error("Failed checking agreement")
	}
	if Agr != nil {
		fmt.Println("Agreement already exists: " + AID)
		return shim.Error("This agreement already exists")
	}

	// Write agreement to the ledger
	agrBytes, _ := json.Marshal(agreement)
	err = stub.PutState(AID, agrBytes)
	if err != nil {
		fmt.Println("Could not save new agreement to ledger: " + err.Error())
		return shim.Error(err.Error())
	}

	fmt.Println("Created agreement", AID)
	return shim.Success(nil)
}

// Publishes a measurement of an existing agreement
// =============================================================================
func (t *SimpleChaincode) publishMeasurement(stub shim.ChaincodeStubInterface, args []string) pb.Response {

	var AID string     // Agreement ID
	var MID string     // Measurement ID
	var metrics string // Agreement measurements
	var err error

	// retrieve args
	if len(args) != 3 {
		return shim.Error("Incorrect number of arguments. Expecting 3")
	}
	AID = args[0]
	MID = args[1]
	metrics = args[2]

	fmt.Println("Publishing measurement of agreement", AID)

	var measurement Measurement
	measurement.ObjectType = "Peering"
	measurement.Timestamp = makeTimestamp()
	measurement.Metrics = metrics
	measurement.AID = AID
	measurement.MID = MID

	// Agreement AID must exist before measurement creation
	Agr, err := stub.GetState(AID)
	if err != nil {
		fmt.Println("Failed checking agreement")
		return shim.Error("Failed checking agreement")
	}
	// Measurement MID must NOT exist before measurement creation
	Msr, err := stub.GetState(MID)
	if err != nil {
		fmt.Println("Failed checking measurement")
		return shim.Error("Failed checking measurement")
	}

	// Write measurement to the ledger
	if Agr != nil && Msr == nil {
		msrBytes, _ := json.Marshal(measurement)
		err = stub.PutState(AID, msrBytes)
		if err != nil {
			fmt.Println("Could not save new agreement to ledger: " + err.Error())
			return shim.Error(err.Error())
		}
		fmt.Println("Created measurement", MID, "- in agreement", AID)
		return shim.Success(nil)
	}

	errMsg := "ERROR: Either agreement " + AID + " does not exist, OR measurement " + MID + " already exists."
	fmt.Println(errMsg)
	return shim.Error(errMsg)

}

// Retrieve an agreement from the ledger
// =============================================================================
func (t *SimpleChaincode) queryAgreement(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var AID string // Agreement ID
	var err error

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting an agreement identifier.")
	}

	AID = args[0]
	fmt.Println("Querying for agreement", AID)

	// Get the state from the ledger
	agrBytes, err := stub.GetState(AID)
	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + AID + "\"}"
		return shim.Error(jsonResp)
	}

	if agrBytes == nil {
		jsonResp := "{\"Error\":\"Agreement " + AID + " does not exist\"}"
		return shim.Error(jsonResp)
	}

	// var agreement Agreement
	// json.Unmarshal(agrBytes, &agreement)
	fmt.Printf("Query Response:%s\n", agrBytes)
	return shim.Success(agrBytes)
}

// Deletes an entity from state
// =============================================================================
func (t *SimpleChaincode) delete(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}

	A := args[0]

	// Delete the key from the state in ledger
	err := stub.DelState(A)
	if err != nil {
		return shim.Error("Failed to delete state")
	}

	return shim.Success(nil)
}

// Represents the query of a chaincode
// =============================================================================
func (t *SimpleChaincode) query(stub shim.ChaincodeStubInterface, args []string) pb.Response {
	var A string // Entities
	var err error

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting name of the person to query")
	}

	A = args[0]

	// Get the state from the ledger
	Avalbytes, err := stub.GetState(A)
	if err != nil {
		jsonResp := "{\"Error\":\"Failed to get state for " + A + "\"}"
		return shim.Error(jsonResp)
	}

	if Avalbytes == nil {
		jsonResp := "{\"Error\":\"Nil amount for " + A + "\"}"
		return shim.Error(jsonResp)
	}

	jsonResp := "{\"Name\":\"" + A + "\",\"Amount\":\"" + string(Avalbytes) + "\"}"
	fmt.Printf("Query Response:%s\n", jsonResp)
	return shim.Success(Avalbytes)
}

func main() {
	err := shim.Start(new(SimpleChaincode))
	if err != nil {
		fmt.Printf("Error starting Simple chaincode: %s", err)
	}
}
