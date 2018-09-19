package experiments

import (
	"crypto/rand"
	"fmt"
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

func PaillierTest(x, y, k int) {

	print("\n\t------------------------------\n\n",
		"\tTESTING PAILLIER HOMOMORPHIC ENCRYPTION SCHEME:\n",
		"\tAddition and scalar multiplication\n\n")

	tkh, _ := paillier.GetThresholdKeyGenerator(18, 2, 2, rand.Reader)
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

	print("\n\t------------------------------\n")

}
