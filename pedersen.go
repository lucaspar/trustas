package main

import (
	"fmt"
	// "fmt"
	"github.com/xlab-si/emmy/crypto/commitments"
	"github.com/xlab-si/emmy/crypto/groups"
	"math/big"
)

func makeCommit(message string) (*groups.ECGroupElement, *commitments.PedersenECReceiver, *commitments.PedersenECCommitter) {

	receiver := commitments.NewPedersenECReceiver(groups.P256)
	committer := commitments.NewPedersenECCommitter(receiver.Params)

	println("COMMITTING:\t", message)
	c, err := committer.GetCommitMsg(StringToBigint(message))
	if err != nil {
		println("Error in GetCommitMsg: %v", err)
	}

	return c, receiver, committer

}

func decommit(c *groups.ECGroupElement, receiver *commitments.PedersenECReceiver, committer *commitments.PedersenECCommitter) string {

	receiver.SetCommitment(c)
	committedVal, r := committer.GetDecommitMsg()
	success := receiver.CheckDecommitment(r, committedVal)

	if success != true {
		fmt.Println("\n\n\t>>> Pedersen EC commitment failed. <<< " + BigintToString(committedVal) + "\n\n")
		return ""
	} else {
		decodedMessage := BigintToString(committedVal)
		fmt.Println("DECODED:\t", decodedMessage)
		return decodedMessage
	}

}

func pedersenCommit(message string) {

	c, receiver, committer := makeCommit(message)
	decommit(c, receiver, committer)

}

func StringToBigint(str string) *big.Int {

	// string to byte array
	buffer := []byte(str)
	bigInteger := new(big.Int)

	// byte array to big integer
	bigInteger.SetBytes(buffer)

	return bigInteger

}

func BigintToString(bigInteger *big.Int) string {

	// big integer to byte array
	buffer := bigInteger.Bytes()

	// byte array to string
	return string(buffer[:])

}

func pedersenTest() {

	messages := []string{
		"just three words",
		"now a message of maximum 32bytes"}
	// "just byte longer than da previous",
	// "<<< SPECIAL CHARS >>> :;[]{}\\|?/\"'<>,. ~!@#$%^&*()_+ `1234567890-=",
	// "<<< PARAGRAPH >>> Go (often referred to as Golang) is message programming language created by Google[12] in 2009 by Robert Griesemer, Rob Pike, and Ken Thompson. Go is message statically typed, compiled language in the tradition of C, with memory safety, garbage collection, structural typing,[3] and CSP-style concurrency.[13] The compiler, tools, and source code are all free and open source.[14]",
	// "<<< LONG TEXT >>> The language was announced in November 2009. Version 1.0 was released in March 2012.[16][17] It is used in some of Google's production systems, as well as by many other companies and open source projects.[18].\n\nGo originated as an experiment by Griesemer, Pike, and Thompson to design message programming language that would resolve common criticisms of other languages while maintaining their positive characteristics. The developers envisioned the new language as:[19].\n\nStatically typed and scalable to large systems (like Java or C++). Productive and readable, without excessive boilerplate[20] (like dynamic languages such as Ruby or Python). Not requiring integrated development environments, but supporting them well.\n\nSupporting networking and multiprocessing. The designers cited their shared dislike of C++ as message primary motivation for designing message new language.[21][22][23] April 2018, the original logo (Gopher mascot) was replaced with message stylized GO slanting right with trailing streamlines. However, the mascot remained the same.\n<<< END OF LONG TEXT >>>"}

	println("\n\nTESTING PEDERSEN COMMITMENTS:\n")
	for idx, msg := range messages {
		println("INDEX:", idx)
		// println(BigintToString(StringToBigint(msg)))
		pedersenCommit(msg)
		println("\n ---------- \n")
	}

}
