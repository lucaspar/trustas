import os
import re
import subprocess
import threading
import time
import unittest

from hfc.fabric.client import Client
from hfc.fabric.user import create_user
from test.integration.config import E2E_CONFIG

NET_CONFIG      = E2E_CONFIG['trustas-net']
FABRIC_LOGS     = False
LOG_FILE        = "logs/trustas." + str(time.time()) + ".log"
NET_STATS_DIR   = "experiments/network"
ALIVE           = False  # Whether the network is up

class BaseTestCase(unittest.TestCase):
    """
    Base class for test cases.
    All test cases can feel free to implement this.
    """

    def setUp(self):
        self.gopath_bak = os.environ.get('GOPATH', '')
        gopath = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                               "../fixtures/chaincode"))
        os.environ['GOPATH'] = os.path.abspath(gopath)
        self.channel_tx = \
            NET_CONFIG['channel-artifacts']['channel.tx']
        self.compose_file_path = \
            NET_CONFIG['docker']['compose_file_tls']

        self.config_yaml = \
            NET_CONFIG['channel-artifacts']['config_yaml']
        self.channel_profile = \
            NET_CONFIG['channel-artifacts']['channel_profile']
        self.client = Client('test/fixtures/trustas-net.json')
        self.channel_name = "businesschannel"                               # application channel
        self.user = self.client.get_user('org1.example.com', 'Admin')
        self.assertIsNotNone(self.user, 'org1 admin should not be None')

        global ALIVE
        ALIVE = True

        # Boot up the testing network
        self.start_test_env()

    def tearDown(self):
        time.sleep(1)
        self.shutdown_test_env()
        global ALIVE
        ALIVE = False

    def check_logs(self):
        cli_call(["docker-compose", "-f", self.compose_file_path, "logs",
                  "--tail=200"])

    def start_test_env(self):

        cli_call(["docker-compose", "-f", self.compose_file_path, "up", "-d"])
        time.sleep(1)

        if FABRIC_LOGS:
            network_logs = threading.Thread(target=self.__log_network)
            network_logs.start()
            print(" > Logging Network output to \"{}\"".format(LOG_FILE))

        network_traffic = threading.Thread(target=self.__network_traffic)
        network_traffic.start()
        print(" > Logging Network Traffic")

    def shutdown_test_env(self):
        cli_call(["docker-compose", "-f", self.compose_file_path, "down"])

    # Logs Hyperledger network output
    def __log_network(self):
        # capture logs
        output, _, _ = cli_call(
            ["docker-compose", "-f", self.compose_file_path, "logs", "-f"])
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
        command = [
            "docker", "stats", "--no-stream", "--all", "--format",
            "{{.Name}},{{.NetIO}}"
        ]
        mkdir_p(NET_STATS_DIR)
        filename = os.path.join(NET_STATS_DIR, str(time.time()) + ".csv")
        while ALIVE:
            netstats, _, _ = cli_call(command)
            netstats = netstats.decode()
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
                line = ','.join([measurement] + columns +
                                [str(ingress), str(egress)])
                lines.append(line)

            netstats = '\n'.join(lines)
            with open(filename, "a") as f:
                f.write(netstats)


# This should be deprecated, and use client.get_user() API instead
def get_peer_org_user(org, user, state_store):
    """Loads the requested user for a given peer org
        and returns a user object.
    """

    peer_user_base_path = os.path.join(
        os.getcwd(),
        'test/fixtures/trustas/crypto-config/peerOrganizations/{0}'
        '/users/{1}@{0}/msp/'.format(org, user)
    )

    key_path = os.path.join(
        peer_user_base_path, 'keystore/',
        NET_CONFIG[org]['users'][user]['private_key']
    )

    cert_path = os.path.join(
        peer_user_base_path, 'signcerts/',
        NET_CONFIG[org]['users'][user]['cert']
    )

    msp_id = NET_CONFIG[org]['mspid']

    return create_user(user, org, state_store, msp_id, key_path, cert_path)


def get_orderer_org_user(org='example.com', user='Admin', state_store=None):
    """Loads the admin user for a given orderer org and
        returns an user object.
        Currently, orderer org only has Admin

    """
    msp_path = os.path.join(
        os.getcwd(),
        'test/fixtures/trustas/crypto-config/ordererOrganizations/'
        'example.com/users/Admin@example.com/msp/')

    key_path = os.path.join(
        msp_path, 'keystore/',
        NET_CONFIG['orderer']['users'][user]['private_key']
    )

    cert_path = os.path.join(
        msp_path, 'signcerts',
        NET_CONFIG['orderer']['users'][user]['cert']
    )
    msp_id = NET_CONFIG['orderer']['mspid']

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
        The integer of number of bytes. Special cases:
            Ret. zero if it fails to find a number
            Ret. the number if it fails to find a unit (KB, MB, ...)
    """
    factors = {
        "kB": 1e3,
        "MB": 1e6,
        "GB": 1e9,
        "TB": 1e12,
        "PB": 1e15,
        "EB": 1e18,
        "ZB": 1e21,
        "YB": 1e24
    }

    # parse floating point number from string
    numbers = re.findall(r'[-+]?[0-9]*\.?[0-9]+', str)
    if not numbers:
        return 0
    number = float(numbers[0])

    # return number * first factor found
    for key, factor in factors.items():
        if key in str:
            return int(number * factor)

    # else return number only
    return number
