# TrustAS
> Establishing trust among autonomous systems

## What is this

**A novel way of establishing trust among Autonomous Systems on the Internet.**

TrustAS uses Order Preserving Encryption to create **confidence** among ASes based on their interconnection history, which is stored in a permissioned blockchain. The usage of cryptography delivers **privacy by design** when handling SLAs. A distributed ledger guarantees the history is both **immutable** and **verifiable**.

TrustAS enables **anyone** in the permissioned network to verify whether an agreed SLA was respected or not, for each of its properties (e.g. latency, bandwidth, jitter). Hence, potentially increasing the amount of **confidence** on a third party before any new agreement takes place.

## Software versions

>   Please, follow the provided URLs for installing dependencies.
    Some of the software used may have multiple origins (e.g. from different package managers) that could yield inconsistencies in the execution. This is valid for Docker and pip for example.


Software        | Version
--------------- | -----------
OS              | Ubuntu 18.04.1 LTS
[Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)   | 18.06.1-ce
[Docker Compose](https://docs.docker.com/compose/install/)          | 1.21.2
[Python](https://www.python.org/downloads/)                         | 3.6.6
[pip](https://pip.pypa.io/en/stable/installing/)                    | 18.1
[virtualenv](https://virtualenv.pypa.io/en/stable/installation/)    | 16.0.0

Further software versions are specified in the `src/requirements.txt` and in Docker images. It is not necessary to manually install those.

## [Execution](src/README.md)
