import datetime
import errno
import itertools
import json
import math
import os
import random
import sys
import time

from beeprint import pp

import trustas

# SETTINGS
EXP_DIR         = "experiments"
MAX_ASN         = 2**16-1
PEERS_SIM       = 100
PEERS_REAL      = 100
CONNECTIONS     = 100
MPA             = 1

def exp_privacy_cost(encryption,
                     experiment_path,
                     peers_real,
                     peers_sim=100,
                     connections=100,
                     mpa=1,
                     storage="json"):
    """Simulates agreements with or without encryption.

    Agreements are simulated based on a set of parameters passed.
    If the storage is set to "json", the agreements will be stored
    in a JSON file in EXP_DIR + experiment_path.

    Args:
        encryption:         boolean: if true, enables OPE on data output
        experiment_path:    path for working dir (from EXP_DIR/)
        peers_real:         number of real ASes in the network (docker containers)
        peers_sim:          number of simulated ASes in the network (for the agreement factory)
        connections:        number of interconnections among ASes
        mpa:                metric sets per agreement
        storage:            storage mode: "json" for JSON output
    Raises:
        ValueError:     if S (peers_sim) is less than 3
        ValueError:     if the number of connections is too large for the net size (nCr formula)
    Returns:
        List of agreements created

    """
    global PEERS_SIM
    global PEERS_REAL
    global CONNECTIONS
    global MPA

    PEERS_SIM       = peers_sim
    PEERS_REAL      = peers_real
    CONNECTIONS     = connections
    MPA             = mpa

    working_dir = os.path.join(EXP_DIR, experiment_path)

    __validate_data()
    as_list     = __generate_ases()
    as_pairs    = __generate_as_pairs(as_list)
    agreements  = __generate_agreements(as_pairs)

    if storage == "json":
        print(" > Printing to files")

        # Experiment information
        metadata = [{
            "timestamp"     : datetime.datetime.now().isoformat(),
            "peers_real"    : PEERS_REAL,
            "connections"   : CONNECTIONS,
            "mpa"           : MPA
        }]
        __agreements_to_file(
            agreements=agreements,
            filepath=working_dir,
            extras=metadata,
            encryption=encryption)

    return agreements


def exp_package_demos():
    """Print examples of the encryption used to stdout."""

    asn_a   = random.randint(0, 2**15 - 1)
    asn_b   = random.randint(2**15, 2**16 - 1)
    peers   = {asn_a, asn_b}

    sla = trustas.sla.SLA(
        bandwidth=100,
        packet_loss=1e-1,
        latency=5,
        jitter=40,
        repair=4,
        guarantee=1 - 1e-1,
        availability=1 - 1e-2)

    metrics = trustas.sla.SLA(
        bandwidth=116,
        packet_loss=0.27e-1,
        latency=7,
        jitter=60,
        repair=1,
        guarantee=1 - 0.83e-1,
        availability=1 - 0.21e-2)

    # create an agreement
    agreement = trustas.agreement.Agreement(SLA=sla, peers=peers)
    agreement.append_metrics(metrics)

    # get encrypted properties
    enc_sla = agreement.get_encrypted_sla()
    enc_met = agreement.get_encrypted_metrics()

    sla.print()
    metrics.print()

    pp(enc_sla)
    pp(enc_met)


def __validate_data():
    fnn = math.factorial(PEERS_SIM)
    fnd = math.factorial(PEERS_SIM - 2)
    if PEERS_SIM > MAX_ASN:
        raise ValueError("Network is too large ({})".format(PEERS_SIM))
    if fnn / (2 * fnd) < CONNECTIONS:
        raise ValueError(
            "Too many connections ({}) for the simulated network of size ({}).".format(
                CONNECTIONS, PEERS_SIM))


def __generate_ases():
    return random.sample(range(1, MAX_ASN), PEERS_SIM)


def __generate_as_pairs(ASes):
    combinations = list(itertools.combinations(ASes, 2))
    return random.sample(combinations, CONNECTIONS)


def __agreement_factory(asn_a, asn_b, metric_samples=1):
    """Returns a random agreement between asn_a and asn_b.

    Args:
        asn_a:          AS Number of one peer in the agreement.
        asn_b:          AS Number of the other peer.
        metric_samples: Number of simulated metrics samples.
    Returns:
        An Agreement instance between a and b.
    """

    # create an agreement
    peers = {asn_a, asn_b}
    sla = trustas.sla.SLA(randomize=True)
    agreement = trustas.agreement.Agreement(SLA=sla, peers=peers)

    # generate metrics
    for m in range(0, metric_samples):
        metrics = trustas.sla.SLA(randomize=True)
        agreement.append_metrics(metrics)

    return agreement


def __generate_agreements(pairs):
    """Returns a random agreement between asn_a and asn_b.

    Args:
        pairs: list of pairs of ASes which form agreements.
    Returns:
        A list of Agreement instances of size len(pairs).
    """
    size = len(pairs)
    agreements = []
    print(' > Generating agreements', end='', flush=True)
    for idx, pair in enumerate(pairs):
        agreement = __agreement_factory(
            pair[0], pair[1], metric_samples=MPA)
        agreements.append(agreement)

        # show discrete progress to cli
        if (idx+1) % 100 == 0:
            print('.', end='', flush=True)

    print('')
    return agreements


def __agreements_to_file(agreements, filepath, extras=[], encryption=True):
    """Writes agreement list to two files: encrypted and plaintext.

    If path to filename does not exist, it will be created.

    Args:
        agreements: list of Agreement instances.
        filepath:   output directory.
        extras:     metadata on the experiment.
        encryption: cryptography enabled.
    Raises:
        PermissionError: if unable to create file or directory.
    """

    # form object
    text = __jsonify_agreements(
        agreements, encryption=encryption, extras=extras)

    # creates file path
    name = "agreements_enc.json" if encryption else "agreements_pla.json"
    filename = os.path.join(filepath, name)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise PermissionError

    # write to files
    with open(filename, "w+") as fp:
        fp.write(text)


def __jsonify_agreements(agreements, encryption=True, extras=[]):
    ags = extras.copy()
    if encryption:
        for agr in agreements:
            ag = {
                "id": str(agr.id),
                "sla": agr.get_encrypted_sla(),
                "met": agr.get_encrypted_metrics()
            }
            ags.append(ag)
    else:
        for agr in agreements:
            ag = {
                "id": str(agr.id),
                "sla": agr.get_plaintext_sla(),
                "met": agr.get_plaintext_metrics()
            }
            ags.append(ag)

    return json.dumps(ags)


def run():
    """Run all experiments available."""

    exp_privacy_cost(
        encryption      = True,
        experiment_path = "experiments/storage",
        peers_real      = 10,
        peers_sim       = 100,
        connections     = 100,
        mpa             = 1,
        storage         = "json")

    exp_package_demos()
