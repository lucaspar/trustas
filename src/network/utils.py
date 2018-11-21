# SPDX-License-Identifier: Apache-2.0

import errno
import os
import re
import subprocess
import threading
import time
import unittest

from hfc.fabric.client import Client
from hfc.fabric.user import create_user
from .config import E2E_CONFIG

HOST = "localhost"
NAME = "localhost"
ALIVE = False                   # Whether the network is up
LOCAL_DEPLOY = False            # Localhost deploy
GCP_DEPLOY = not LOCAL_DEPLOY   # GCP deploy
NETWORK_NAME = "trustas-network"
LOG_FILE = "logs/trustas." + str(time.time()) + ".log"
NET_STATS_DIR = "experiments/network_stats"

class BaseTestCase(unittest.TestCase):
    """
    Base class for test cases.
    All test cases can feel free to implement this.
    """

    def setUp(self, wipe_all):
        self.gopath_bak = os.environ.get('GOPATH', '')
        gopath = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                               "../test/fixtures/chaincode"))

        os.environ['GOPATH'] = os.path.abspath(gopath)
        if "LOCAL_DEPLOY" in os.environ:
            LOCAL_DEPLOY = os.environ["LOCAL_DEPLOY"] == "True"
        GCP_DEPLOY = not LOCAL_DEPLOY

        self.channel_tx = \
            E2E_CONFIG[NETWORK_NAME]['channel-artifacts']['channel.tx']
        self.compose_file_path = \
            E2E_CONFIG[NETWORK_NAME]['docker']['compose_file_trustas_gcp'] if GCP_DEPLOY else \
            E2E_CONFIG[NETWORK_NAME]['docker']['compose_file_trustas_localhost']
        self.config_yaml = \
            E2E_CONFIG[NETWORK_NAME]['channel-artifacts']['config_yaml']
        self.channel_profile = \
            E2E_CONFIG[NETWORK_NAME]['channel-artifacts']['channel_profile']
        self.client =   Client('test/fixtures/trustas_net_gcp.json') if GCP_DEPLOY else \
                        Client('test/fixtures/local-25peers.json')
        self.channel_name = "businesschannel"  # default application channel
        self.user = self.client.get_user('org1.example.com', 'Admin')
        self.assertIsNotNone(self.user, 'org1 admin should not be None')

        global ALIVE
        ALIVE = True

        # Boot up the testing network
        self.start_test_env(wipe_all)
        return HOST, NAME

    def tearDown(self, keep_network=False):
        if not keep_network:
            self.shutdown_test_env()
        global ALIVE
        ALIVE = False

    # Logs Hyperledger network output
    def __log_network(self):
        # capture logs
        output, _, _ = cli_call([
            "docker-compose", "-f", self.compose_file_path,
            "logs", "-f"
        ])
        output = output.decode()

        # remove color encoding
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        output = ansi_escape.sub('', output)

        # create output dir if it does not exist
        mkdir_p('/'.join(LOG_FILE.split('/')[:-1]))

        # write log
        with open(LOG_FILE, "w+") as fp:
            fp.write(output)

    # Logs Docker network traffic
    def __network_traffic(self):
        global ALIVE
        command = [ "docker", "stats", "--no-stream", "--all", "--format", "{{.Name}},{{.NetIO}}" ]
        mkdir_p(NET_STATS_DIR)
        filename = os.path.join(NET_STATS_DIR, str(time.time()) + ".csv")
        while ALIVE:
            netstats, _, _ = cli_call(command)
            netstats = netstats.decode()
            with open(filename, "a") as f:
                f.write(netstats)
            measurement = str(time.time())
            lines = []
            for line in netstats.split('\n'):
                columns = line.split(',')
                if not line or len(columns) < 2:
                    lines.append('\n')
                    continue
                # individual, agregado / input, output / peers, orderer

                # from 3rd column, remove whitespaces and separate ingress and egress traffic
                val = columns[1].replace(" ", "").split('/')
                if len(val) < 2:
                    lines.append('\n')
                    continue

                # convert B, KB, MB, ... into numbers only
                ingress = human_to_bytes(val[0])
                egress = human_to_bytes(val[1])

                # join everything to the line
                line = ','.join([measurement] + columns + [str(ingress), str(egress)])
                lines.append(line)

            netstats = '\n'.join(lines)
            with open(filename, "a") as f:
                f.write(netstats)
            # TODO: ver como timestamp varia com 100 peers
            time.sleep(1)

    def start_test_env(self, wipe_all):

        if wipe_all:
            print(" > Wiping old assets")
            # Remove unwanted containers, images, and files
            cli_call(["./cleanup.sh"])

        if "LOCAL_DEPLOY" in os.environ:
            LOCAL_DEPLOY = os.environ["LOCAL_DEPLOY"] == "True"
        GCP_DEPLOY = not LOCAL_DEPLOY

        # GCP environment
        if GCP_DEPLOY:

            HOST, _, _ = cli_call(["curl", "--ssl", "-sH", "Metadata-Flavor: Google",
                            "http://metadata.google.internal/computeMetadata/v1/instance/hostname"])
            NAME, _, _ = cli_call(["curl", "--ssl", "-sH", "Metadata-Flavor: Google",
                            "http://metadata.google.internal/computeMetadata/v1/instance/name"])
            HOST = HOST.decode()
            NAME = NAME.decode()

            os.environ["GCP_HOST"] = HOST
            os.environ["GCP_NAME"] = NAME

            service = NAME + ".org1.example.com" if NAME.startswith("peer") else NAME + ".example.com"
            print(" > Starting service {}".format(service))
            cli_call(["docker-compose", "-f", self.compose_file_path, "up", "--no-start"])
            cli_call(["docker-compose", "-f", self.compose_file_path, "start", service])

        # local environment
        else:
            host = "localhost"
            name = "localhost"
            print(" > Setting network... see it with \"docker stats\"")
            cli_call(["docker-compose", "-f", self.compose_file_path, "up", "-d", "--scale", "cli=0"])

        time.sleep(1)
        network_logs = threading.Thread(target=self.__log_network)
        network_logs.start()
        print(" > Logging Network output to \"{}\"".format(LOG_FILE))

        network_traffic = threading.Thread(target=self.__network_traffic)
        network_traffic.start()
        print(" > Logging Network Traffic".format(LOG_FILE))


    def shutdown_test_env(self):
        print(" > Shutting down network")

        # Get network down
        cli_call([ "docker-compose", "-f", self.compose_file_path, "down", "--volumes" ])


# This should be deprecated, and use client.get_user() API instead
def get_peer_org_user(org, user, state_store):
    """Loads the requested user for a given peer org
        and returns a user object.
    """

    peer_user_base_path = os.path.join(
        os.getcwd(),
        'test/fixtures/e2e_cli/crypto-config/peerOrganizations/{0}'
        '/users/{1}@{0}/msp/'.format(org, user))

    key_path = os.path.join(
        peer_user_base_path, 'keystore/',
        E2E_CONFIG[NETWORK_NAME][org]['users'][user]['private_key'])

    cert_path = os.path.join(
        peer_user_base_path, 'signcerts/',
        E2E_CONFIG[NETWORK_NAME][org]['users'][user]['cert'])

    msp_id = E2E_CONFIG[NETWORK_NAME][org]['mspid']

    return create_user(user, org, state_store, msp_id, key_path, cert_path)


def get_orderer_org_user(org='example.com', user='Admin', state_store=None):
    """Loads the admin user for a given orderer org and
        returns an user object.
        Currently, orderer org only has Admin
    """
    msp_path = os.path.join(
        os.getcwd(),
        'test/fixtures/e2e_cli/crypto-config/ordererOrganizations/'
        'example.com/users/Admin@example.com/msp/')

    key_path = os.path.join(
        msp_path, 'keystore/',
        E2E_CONFIG[NETWORK_NAME]['orderer']['users'][user]['private_key'])

    cert_path = os.path.join(
        msp_path, 'signcerts',
        E2E_CONFIG[NETWORK_NAME]['orderer']['users'][user]['cert'])
    msp_id = E2E_CONFIG[NETWORK_NAME]['orderer']['mspid']

    return create_user(user, org, state_store, msp_id, key_path, cert_path)


def cli_call(arg_list, expect_success=True, env=os.environ.copy()):
    """Executes a CLI command in a subprocess and return the results.

    Args:
        arg_list: a list command arguments
        expect_success: use False to return even if an error occurred
                        when executing the command
        env:

    Returns: (string, string, int) output message, error message, return code

    """
    p = subprocess.Popen(arg_list, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, env=env)
    output, error = p.communicate()
    if p.returncode != 0:
        if output:
            print("Output:\n" + str(output))
        if error:
            print("Error Message:\n" + str(error))
        if expect_success:
            raise subprocess.CalledProcessError(
                p.returncode, arg_list, output)
    return output, error, p.returncode


def mkdir_p(mypath):
    '''Creates a directory. Equivalent to using mkdir -p <mypath> on the command line.'''

    from errno import EEXIST
    from os import makedirs, path

    try:
        makedirs(mypath)
    except OSError as exc:
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else:
            raise

def human_to_bytes(str):
    """Converts first human readable number into bytes

    Returns
        Integer of number of bytes
    """
    factors = {
        "kB": 1e3,
        "MB": 1e6,
        "GB": 1e9,
        "TB": 1e12,
        "PB": 1e15,
        "YB": 1e16
    }
    numbers = re.findall(r'[-+]?[0-9]*\.?[0-9]+', str)
    if not numbers:
        return 0
    number = float(numbers[0])

    for key, factor in factors.items():
        if key in str:
            return int(number * factor)

    return number
