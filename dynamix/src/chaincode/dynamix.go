/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

// Smart contract of the Dynam-IX project
// Based on the fabcar and marbles smart contracts from Hyperledger fabric-samples
package main

//=======================================================================================//
//										Imports											 //
//=======================================================================================//
import (
	"bytes"         // Handling bytes
	"encoding/json" // Reading and writing JSON
	"fmt"           // Formatting
	"strconv"       // String manipulation
	"time"          // Time manipulation

	"github.com/hyperledger/fabric/core/chaincode/shim" // Hyperledger Fabric specific
	sc "github.com/hyperledger/fabric/protos/peer"      // Hyperledger Fabric specific
)

//=======================================================================================//
//								Struct Definitions										 //
//=======================================================================================//

// SmartContract structure
type SmartContract struct {
}

// AS (Autonomous System) structure. Tags are used by encoding/json library
type AS struct {
	Address string `json:"address"` // IP:port
	Service string `json:"service"` // Description of the service being offered by the AS (e.g., Transit Provider)
	CustRep int    `json:"custrep"` // AS' reputation as a customer
	ProvRep int    `json:"provrep"` // AS' reputation as a provider
	PubKey  string `json:"pubkey"`  // AS' public key
}

// Interconnection agreement structure. Tags are used by encoding/json library
type agreement struct {
	ContractHash      string `json:"contracthash"`      // Hash of the agreement contract (terms)
	CustomerASN       string `json:"customerasn"`       // ASN of the customer
	ProviderASN       string `json:"providerasn"`       // ASN of the provider
	CustomerSignature string `json:"customersignature"` // Hash of the agreement contract (terms) encrypted with the customer's public key
	ProviderSignature string `json:"providersignature"` // Hash of the agreement contract (terms) encrypted with the provider's public key
}

//=======================================================================================//
//								Smart Contract functions								 //
//=======================================================================================//

// Init method is called when the Smart Contract "dynamix" is instantiated by the blockchain network
func (s *SmartContract) Init(APIstub shim.ChaincodeStubInterface) sc.Response {
	return shim.Success(nil)
}

// Invoke method is called as a result of an application request to run the Smart Contract "dynamix"
func (s *SmartContract) Invoke(APIstub shim.ChaincodeStubInterface) sc.Response {

	// Retrieve the requested Smart Contract function and arguments
	function, args := APIstub.GetFunctionAndParameters()
	// Route to the appropriate handler function to interact with the ledger appropriately
	if function == "initLedger" {
		return s.initLedger(APIstub)
	} else if function == "registerAS" {
		return s.registerAS(APIstub, args)
	} else if function == "listASes" {
		return s.listASes(APIstub)
	} else if function == "history" {
		return s.history(APIstub, args)
	} else if function == "delete" {
		return s.delete(APIstub, args)
	} else if function == "updateCustRep" {
		return s.updateCustRep(APIstub, args)
	} else if function == "updateProvRep" {
		return s.updateProvRep(APIstub, args)
	} else if function == "updateService" {
		return s.updateService(APIstub, args)
	} else if function == "updateAddress" {
		return s.updateAddress(APIstub, args)
	} else if function == "show" {
		return s.show(APIstub, args)
	} else if function == "findService" {
		return s.findService(APIstub, args)
	} else if function == "listAgreements" {
		return s.listAgreements(APIstub)
	} else if function == "registerAgreement" {
		return s.registerAgreement(APIstub, args)
	}

	return shim.Error("Invalid Smart Contract function name.")
}

// Initialize ledger
func (s *SmartContract) initLedger(APIstub shim.ChaincodeStubInterface) sc.Response {

	/*	ASes := []AS{
			AS{Address: "10.1.1.50:5000", Service: "DDoS Mitigation", CustRep: 10, ProvRep: 100, PubKey: "af671adebca7abdafd6152"},
			AS{Address: "10.1.1.60:5000", Service: "Transit Provider", CustRep: -1, ProvRep: 34, PubKey: "176abf1234567abdafd6152"},
			AS{Address: "10.1.1.70:5000", Service: "Cloud Provider", CustRep: 5, ProvRep: 12, PubKey: "abcdef1234567abdafd6152"},
		}

		i := 0
		for i < len(ASes) {
			fmt.Println("i is ", i)
			ASAsBytes, _ := json.Marshal(ASes[i])
			APIstub.PutState("AS"+strconv.Itoa(i), ASAsBytes)
			fmt.Println("Added", ASes[i])
			i = i + 1
		}

		Agreements := []agreement{
			agreement{ContractHash: "sagiiGUGidaGiudgas", CustomerASN: "AS1", ProviderASN: "AS7", CustomerSignature: "76atsd8ahd87asg", ProviderSignature: "yasudas78d9asdsa"},
		}

		i = 0
		for i < len(Agreements) {
			fmt.Println("i is ", i)
			AgreementAsBytes, _ := json.Marshal(Agreements[i])
			APIstub.PutState("IA-"+strconv.Itoa(i), AgreementAsBytes)
			fmt.Println("Added", Agreements[i])
			i = i + 1
		}
	*/
	return shim.Success(nil)
}

//=======================================================================================//
//								Autunomous System functions								 //
//=======================================================================================//

// Register a new AS on the ledger
func (s *SmartContract) registerAS(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 6 {
		fmt.Printf("\n%s\n%d\n", args, len(args))
		return shim.Error("Incorrect number of arguments. Expecting 6")
	}

	custRep, err := strconv.Atoi(args[3])
	if err != nil {
		return shim.Error(err.Error())
	}

	provRep, err := strconv.Atoi(args[4])
	if err != nil {
		return shim.Error(err.Error())
	}

	var as = AS{Address: args[1], Service: args[2], CustRep: custRep, ProvRep: provRep, PubKey: args[5]}

	ASAsBytes, _ := json.Marshal(as)
	APIstub.PutState(args[0], ASAsBytes)

	return shim.Success(nil)
}

// List all ASes on the ledger
func (s *SmartContract) listASes(APIstub shim.ChaincodeStubInterface) sc.Response {

	startKey := "AS0"
	endKey := "AS999"

	resultsIterator, err := APIstub.GetStateByRange(startKey, endKey)
	if err != nil {
		return shim.Error(err.Error())
	}
	defer resultsIterator.Close()

	// buffer is a JSON array containing QueryResults
	var buffer bytes.Buffer

	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return shim.Error(err.Error())
		}

		buffer.WriteString(queryResponse.Key)
		buffer.WriteString(": ")
		// Record is a JSON object, so we write as-is
		buffer.WriteString(string(queryResponse.Value))
		buffer.WriteString("\n")
	}

	fmt.Printf("- queryAllASes:\n%s\n", buffer.String())

	return shim.Success(buffer.Bytes())
}

// Update the customer reputation of an AS
func (s *SmartContract) updateCustRep(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 2 {
		return shim.Error("Incorrect number of arguments. Expecting 2")
	}

	ASAsBytes, _ := APIstub.GetState(args[0])
	as := AS{}

	json.Unmarshal(ASAsBytes, &as)
	rep, err := strconv.Atoi(args[1])
	if err != nil {
		return shim.Error(err.Error())
	}

	as.CustRep = as.CustRep + rep

	ASAsBytes, _ = json.Marshal(as)
	APIstub.PutState(args[0], ASAsBytes)

	return shim.Success(nil)
}

// Update the provider reputation of an AS
func (s *SmartContract) updateProvRep(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 2 {
		return shim.Error("Incorrect number of arguments. Expecting 2")
	}

	ASAsBytes, _ := APIstub.GetState(args[0])
	as := AS{}

	json.Unmarshal(ASAsBytes, &as)
	rep, err := strconv.Atoi(args[1])
	if err != nil {
		return shim.Error(err.Error())
	}

	as.ProvRep = as.ProvRep + rep

	ASAsBytes, _ = json.Marshal(as)
	APIstub.PutState(args[0], ASAsBytes)

	return shim.Success(nil)
}

// Update the service description of an AS
func (s *SmartContract) updateService(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 2 {
		return shim.Error("Incorrect number of arguments. Expecting 2")
	}

	ASAsBytes, _ := APIstub.GetState(args[0])
	as := AS{}

	json.Unmarshal(ASAsBytes, &as)
	as.Service = args[1]

	ASAsBytes, _ = json.Marshal(as)
	APIstub.PutState(args[0], ASAsBytes)

	return shim.Success(nil)
}

// Update the address of an AS
func (s *SmartContract) updateAddress(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 2 {
		return shim.Error("Incorrect number of arguments. Expecting 2")
	}

	ASAsBytes, _ := APIstub.GetState(args[0])
	as := AS{}

	json.Unmarshal(ASAsBytes, &as)
	as.Address = args[1]

	ASAsBytes, _ = json.Marshal(as)
	APIstub.PutState(args[0], ASAsBytes)

	return shim.Success(nil)
}

// List all ASes offering a specific service
func (s *SmartContract) findService(stub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) < 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}

	queryString := args[0]

	queryResults, err := getQueryResultForQueryString(stub, queryString)
	if err != nil {
		return shim.Error(err.Error())
	}
	return shim.Success(queryResults)
}

//=======================================================================================//
//								Agreements functions									 //
//=======================================================================================//

// List all agreements on the ledger
func (s *SmartContract) listAgreements(APIstub shim.ChaincodeStubInterface) sc.Response {

	startKey := "IA-"
	endKey := ""

	resultsIterator, err := APIstub.GetStateByRange(startKey, endKey)
	if err != nil {
		return shim.Error(err.Error())
	}
	defer resultsIterator.Close()

	// buffer is a JSON array containing QueryResults
	var buffer bytes.Buffer

	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return shim.Error(err.Error())
		}

		buffer.WriteString(queryResponse.Key)
		buffer.WriteString(": ")
		// Record is a JSON object, so we write as-is
		buffer.WriteString(string(queryResponse.Value))
		buffer.WriteString("\n")
	}

	fmt.Printf("- queryAllASes:\n%s\n", buffer.String())

	return shim.Success(buffer.Bytes())
}

// Register a new agreement on the ledger
func (s *SmartContract) registerAgreement(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 6 {
		fmt.Printf("\n%s\n%d\n", args, len(args))
		return shim.Error("Incorrect number of arguments. Expecting 6")
	}

	var agrmnt = agreement{ContractHash: args[1], CustomerASN: args[2], ProviderASN: args[3], CustomerSignature: args[4], ProviderSignature: args[5]}

	AgreementAsBytes, _ := json.Marshal(agrmnt)
	APIstub.PutState(args[0], AgreementAsBytes)

	return shim.Success(nil)
}

//=======================================================================================//
//								Shared functions										 //
//=======================================================================================//

// Show information about a specific key
func (s *SmartContract) show(APIstub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}

	ASAsBytes, _ := APIstub.GetState(args[0])
	return shim.Success(ASAsBytes)
}

// Delete a key from the ledger
func (s *SmartContract) delete(stub shim.ChaincodeStubInterface, args []string) sc.Response {

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

// Show the history of transactions involving an specific key
func (s *SmartContract) history(stub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) < 1 {
		return shim.Error("Incorrect number of arguments. Expecting 1")
	}

	asn := args[0]

	fmt.Printf("- history for asn: %s\n", asn)

	resultsIterator, err := stub.GetHistoryForKey(asn)
	if err != nil {
		return shim.Error(err.Error())
	}
	defer resultsIterator.Close()

	// buffer is a JSON array containing historic values for the AS
	var buffer bytes.Buffer

	for resultsIterator.HasNext() {
		response, err := resultsIterator.Next()
		if err != nil {
			return shim.Error(err.Error())
		}
		buffer.WriteString("{\"TxId\":")
		buffer.WriteString("\"")
		buffer.WriteString(response.TxId)
		buffer.WriteString("\"")

		buffer.WriteString(": ")
		// if it was a delete operation on given key, then we need to set the
		//corresponding value null. Else, we will write the response.Value
		//as-is (as the Value itself a JSON AS)
		if response.IsDelete {
			buffer.WriteString("null")
		} else {
			buffer.WriteString(string(response.Value))
		}

		buffer.WriteString(", \"Timestamp\":")
		buffer.WriteString("\"")
		buffer.WriteString(time.Unix(response.Timestamp.Seconds, int64(response.Timestamp.Nanos)).String())
		buffer.WriteString("\"")

		buffer.WriteString(", \"IsDelete\":")
		buffer.WriteString("\"")
		buffer.WriteString(strconv.FormatBool(response.IsDelete))
		buffer.WriteString("\"")

		buffer.WriteString("}\n")
	}

	fmt.Printf("\n%s\n", buffer.String())

	return shim.Success(buffer.Bytes())
}

// getQueryResultForQueryString executes the passed in query string.
// Result set is built and returned as a byte array containing the JSON results.
func getQueryResultForQueryString(stub shim.ChaincodeStubInterface, queryString string) ([]byte, error) {

	fmt.Printf("- getQueryResultForQueryString queryString:\n%s\n", queryString)

	resultsIterator, err := stub.GetQueryResult(queryString)
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	// buffer is a JSON array containing QueryRecords
	var buffer bytes.Buffer

	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		buffer.WriteString(queryResponse.Key)
		buffer.WriteString(": ")
		// Record is a JSON object, so we write as-is
		buffer.WriteString(string(queryResponse.Value))
		buffer.WriteString("\n")
	}

	fmt.Printf("- getQueryResultForQueryString queryResult:\n%s\n", buffer.String())

	return buffer.Bytes(), nil
}

//=======================================================================================//
//										Main											 //
//=======================================================================================//

// The main function is only relevant in unit test mode. Only included here for completeness.
func main() {

	// Create a new Smart Contract
	err := shim.Start(new(SmartContract))
	if err != nil {
		fmt.Printf("Error creating new Smart Contract: %s", err)
	}
}
