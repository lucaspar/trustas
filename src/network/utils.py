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

NETWORK_NAME = "test-network"
LOG_FILE = "logs/trustas." + str(time.time()) + ".log"

class BaseTestCase(unittest.TestCase):
    """
    Base class for test cases.
    All test cases can feel free to implement this.
    """

    def setUp(self):
        self.gopath_bak = os.environ.get('GOPATH', '')
        gopath = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                               "../test/fixtures/chaincode"))

        os.environ['GOPATH'] = os.path.abspath(gopath)
        self.channel_tx = \
            E2E_CONFIG[NETWORK_NAME]['channel-artifacts']['channel.tx']
        self.compose_file_path = \
            E2E_CONFIG[NETWORK_NAME]['docker']['compose_file_tls']

        self.config_yaml = \
            E2E_CONFIG[NETWORK_NAME]['channel-artifacts']['config_yaml']
        self.channel_profile = \
            E2E_CONFIG[NETWORK_NAME]['channel-artifacts']['channel_profile']
        self.client = Client('test/fixtures/network.json')
        self.channel_name = "businesschannel"  # default application channel
        self.user = self.client.get_user('org1.example.com', 'Admin')
        self.assertIsNotNone(self.user, 'org1 admin should not be None')

        # Boot up the testing network
        self.start_test_env()

    def tearDown(self):
        self.shutdown_test_env()

    # Logs Hyperledger network output
    def __log_network(self):
        output, _, _ = cli_call([
            "docker-compose", "-f", self.compose_file_path,
            "logs", "-f"
        ])
        output = output.decode()
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        output = ansi_escape.sub('', output)
        if not os.path.exists(os.path.dirname(LOG_FILE)):
            try:
                os.makedirs(os.path.dirname(LOG_FILE))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(LOG_FILE, "w+") as fp:
            fp.write(output)

    def start_test_env(self):

        print(" > Removing old assets")
        # Remove unwanted containers, images, and files
        cli_call(["./cleanup.sh"])

        print(" > Setting network... see it with \"docker stats\"")
        cli_call(["docker-compose", "-f", self.compose_file_path, "up", "-d", "--scale", "cli=0"])
        time.sleep(1)
        network_logs = threading.Thread(target=self.__log_network)
        network_logs.start()
        print(" > Logging Network output to \"{}\"".format(LOG_FILE))

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
        E2E_CONFIG['test-network'][org]['users'][user]['private_key'])

    cert_path = os.path.join(
        peer_user_base_path, 'signcerts/',
        E2E_CONFIG['test-network'][org]['users'][user]['cert'])

    msp_id = E2E_CONFIG['test-network'][org]['mspid']

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
        E2E_CONFIG['test-network']['orderer']['users'][user]['private_key'])

    cert_path = os.path.join(
        msp_path, 'signcerts',
        E2E_CONFIG['test-network']['orderer']['users'][user]['cert'])
    msp_id = E2E_CONFIG['test-network']['orderer']['mspid']

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
