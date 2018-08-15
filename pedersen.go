package main

import (
	// "fmt"
	"github.com/xlab-si/emmy/crypto/commitments"
	"github.com/xlab-si/emmy/crypto/common"
	"github.com/xlab-si/emmy/crypto/groups"
)

func PedersenTest() {

	print("\n\t------------------------------\n\n\t",
		"Testing Pederson Commitment scheme\n\n")

	receiver := commitments.NewPedersenECReceiver(groups.P256)
	committer := commitments.NewPedersenECCommitter(receiver.Params)

	a := common.GetRandomInt(committer.Params.Group.Q)
	println("\tCommitting ", a.String())
	c, err := committer.GetCommitMsg(a)
	if err != nil {
		println("\tError in GetCommitMsg: %v", err)
	}

	receiver.SetCommitment(c)
	committedVal, r := committer.GetDecommitMsg()
	success := receiver.CheckDecommitment(r, committedVal)

	if success != true {
		println("\tPedersen EC commitment failed.")
	} else {
		println("\n\tPASSED:")
	}

	println("\n\tCommit:\n\t\tX: ", c.X.String(),
		"\n\t\tY: ", c.Y.String(),
		"\n\tCommittedVal: ", committedVal.String(),
		"\n\tRandom: ", r.String())

	print("\n\t------------------------------\n")

}
