## TrustAS Experiments

**Experiments are organized in this directory as follows:**

```c
    EXPERIMENT_NAME / [Network Size]_[Connections]_[MPA] / Timestamp / <experiment files>
```

Where:

Metric          | Meaning
 -------------- | ---------------------------------
Network Size    | Number of ASes in the network
Connections     | Total number of agreements stored
MPA             | Metrics Per Agreement stored
Timestamp       | Time of execution

---

### Experiment A

#### Question

What is the **impact of privacy** (order-preserving encryption, secure commitments, and any other privacy-enhancing component) on TrustAS?

#### Metrics

 - Number of agreements
 - Query response time (s)
 - Blockchain size (MB)

#### Factors

 - With privacy enabled or disabled

#### Topology

 - Local execution only
 - Saving data to blockchain and to files

---

### Experiment B

#### Question
What is the **impact of the blockchain network** on TrustAS?

#### Metrics

 - Number of agreements
 - Query response time (s)
 - Data transferred (MB)

#### Topology

 - Distributed execution with privacy enabled
 - Blockchain with one orderer and a number of ASes
 - Each AS establishes a new connection periodically
 - Each AS queries the blockchain periodically

#### Factors

 - Number of ASes: `3, 25, 50, 75, 100`.
 - Time between new AS interconnections (writes)
 - Time between blockchain queries (reads)
 - Number of writes per agreement
