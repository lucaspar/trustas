package experiments

import (
	// "bytes"
	"encoding/json"
	"fmt"
	"github.com/xlab-si/emmy/crypto/commitments"
	"github.com/xlab-si/emmy/crypto/groups"
	"math/big"
)

/*
 *  	Considering: c = g^x * h^r
 *
 *  	c is the ciphertext saved publicly (c = g^x * h^r)
 *  	x is the plaintext, or useful value (x)
 *  	p, from receiver.Params, has constants g and h
 *  	r is a random value and the key for revealing x
 */
func makeCommit(message string) (
	c *groups.ECGroupElement,
	p *commitments.PedersenECParams,
	x *big.Int,
	r *big.Int) {

	receiver := commitments.NewPedersenECReceiver(groups.P256)
	p = receiver.Params
	committer := commitments.NewPedersenECCommitter(p)

	println("COMMITTING:\t", message)
	c, err := committer.GetCommitMsg(StringToBigint(message))
	if err != nil {
		println("Error in GetCommitMsg: %v", err)
	}
	x, r = committer.GetDecommitMsg()

	return c, p, x, r

}

func verifyCommitment(
	c *groups.ECGroupElement,
	p *commitments.PedersenECParams,
	x *big.Int,
	r *big.Int) bool {

	receiver := commitments.NewPedersenECReceiverFromParams(p)
	receiver.SetCommitment(c)
	success := receiver.CheckDecommitment(r, x)

	if success != true {
		fmt.Println("\n\n\t>>> Pedersen EC commitment failed. <<< " + BigintToString(x) + "\n\n")
		return false
	}

	decodedMessage := BigintToString(x)
	fmt.Println("DECODED:\t", decodedMessage)
	return true

}

// converts interface into array of bytes
func desserialize(bytes []byte, x interface{}) {
	err := json.Unmarshal(bytes, &x)
	if err != nil {
		fmt.Println(err)
	}
}

// converts back an array of bytes
func serialize(x interface{}) []byte {
	xs, _ := json.Marshal(x)
	return xs
}

func serializeData(
	c *groups.ECGroupElement,
	p *commitments.PedersenECParams,
	x *big.Int,
	r *big.Int) (

	*groups.ECGroupElement,
	*commitments.PedersenECParams,
	*big.Int,
	*big.Int) {

	// serialize commit
	sc := serialize(c)
	sp := serialize(p)
	sx := serialize(x)
	sr := serialize(r)

	var dc *groups.ECGroupElement
	var dp *commitments.PedersenECParams
	var dx *big.Int
	var dr *big.Int

	// desserialize commit
	desserialize(sc, dc)
	desserialize(sp, dp)
	desserialize(sx, dx)
	desserialize(sr, dr)

	fmt.Println(c)
	fmt.Println(dc)

	return dc, dp, dx, dr

}

func pedersenCommit(message string) {

	const SERIALIZING = false
	c, p, x, r := makeCommit(message)
	if SERIALIZING {
		dc, dp, dx, dr := serializeData(c, p, x, r)
		verifyCommitment(dc, dp, dx, dr)
	} else {
		verifyCommitment(c, p, x, r)
	}

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

func PedersenTest() {

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
