import datetime
import errno
import itertools
import json
import math
import os
import random
import sys

from beeprint import pp

import trustas

EXP_DIR = "experiments"
MAX_ASN = 2**16-1

def privacy_cost(network_size=100, connections=100, mpa=10):
    """Simulates agreements with and without privacy (encryption).

    Agreements are simulated based on a set of parameters passed.
    The timeline of events is output to a file and to stdout.
    The blockchain data is output to a file.
    The output directory is EXP_DIR + EXP_NAME.

    Args:
        network_size:   number (S) of ASes in the network
        connections:    number of interconnections among ASes
        mpa:            metric sets per agreement
    Raises:
        ValueError:     if S (network_size) is less than 3
        ValueError:     if the number of connections is too large (nCr formula)
    Returns:
        None

    """

    # SETTINGS
    EXP_NAME = "A"

    def __validate_data():
        fnn = math.factorial(network_size)
        fnd = math.factorial(network_size-2)
        if network_size > MAX_ASN:
            raise ValueError("Network is too large ({})".format(network_size))
        if fnn / (2 * fnd) < connections:
            raise ValueError(
                "Too many connections ({}) for the network size ({}).".format(
                    connections, network_size))

    def __generate_ases():
        return random.sample(range(1, MAX_ASN), network_size)

    def __generate_as_pairs(ASes):
        combinations = list(itertools.combinations(ASes, 2))
        return random.sample(combinations, connections)

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
        peers   = { asn_a, asn_b }
        sla     = trustas.sla.SLA(randomize=True)
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
        for idx,pair in enumerate(pairs):
            agreement = __agreement_factory(
                pair[0], pair[1], metric_samples=mpa)

            # get encrypted properties
            enc_sla = agreement.get_encrypted_sla()
            enc_met = agreement.get_encrypted_metrics()

            agreements.append(agreement)

        return agreements

    def __agreements_to_file(agreements, filepath, extras=[]):
        """Writes agreement list to two files: encrypted and plaintext.

        If path to filename does not exist, it will be created.

        Args:
            agreements: list of Agreement instances.
            filepath: output directory.
        Raises:
            PermissionError: if unable to create file or directory.
        """

        # form object
        enc_text = __jsonify_agreements(agreements, encrypted=True, extras=extras)
        pla_text = __jsonify_agreements(agreements, encrypted=False, extras=extras)

        # creates file path
        enc_filename = os.path.join(filepath, "agreements_enc.json")
        pla_filename = os.path.join(filepath, "agreements_pla.json")
        if not os.path.exists(os.path.dirname(enc_filename)):
            try:
                os.makedirs(os.path.dirname(enc_filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise PermissionError

        # write to files
        with open(enc_filename, "w+") as fp:
            chars = fp.write(enc_text)
            print("Written {} out of {} characters to {}".format(chars, len(enc_text), enc_filename))

        # write to files
        with open(pla_filename, "w+") as fp:
            chars = fp.write(pla_text)
            print("Written {} out of {} characters to {}".format(chars, len(pla_text), pla_filename))


    def __jsonify_agreements(agreements, encrypted=True, extras=[]):
        ags = extras.copy()
        if encrypted:
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


    working_dir = os.path.join(EXP_DIR, EXP_NAME)

    print(" > Validating data...")
    __validate_data()

    print(" > Creating ASes...")
    as_list     = __generate_ases()

    print(" > Generating pairs...")
    as_pairs    = __generate_as_pairs(as_list)

    print(" > Generating agreements...")
    agreements  = __generate_agreements(as_pairs)

    # Experiment information
    exp = [{
        "timestamp": datetime.datetime.now().isoformat(),
        "network_size": network_size,
        "connections": connections
    }]
    print(" > Printing to files...")
    __agreements_to_file(agreements, filepath=working_dir, extras=exp)

def package_demos():
    """Print examples of the encryption used to stdout."""

    asn_a   = random.randint(0, 2**15 - 1)
    asn_b   = random.randint(2**15, 2**16-1)
    peers   = { asn_a, asn_b }
    sla     = trustas.sla.SLA(latency=5)
    metrics = trustas.sla.SLA(latency=10)

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


def run():
    """Run all experiments available."""
    # privacy_cost()
    package_demos()
