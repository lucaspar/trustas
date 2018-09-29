# SPDX-License-Identifier: Apache-2.0

import os
import re
import subprocess
import time
import unittest

from hfc.fabric.client import Client
from hfc.fabric.user import create_user
from .config import E2E_CONFIG

NETWORK_NAME = "test-network"

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
            E2E_CONFIG[NETWORK_NAME]['docker']['compose_file_tls_cli']

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
        self.check_logs()
        time.sleep(3)
        self.shutdown_test_env()

    # outputs log to trustas.log
    def check_logs(self):
        output, _, _ = cli_call([
            "docker-compose", "-f", self.compose_file_path, "logs",
            "--tail=400"
        ])
        output = output.decode()
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        output = ansi_escape.sub('', output)
        with open("trustas.log", "w+") as fp:
            fp.write(output)

    def start_test_env(self):
        # cli_call(["docker-compose", "-f", self.compose_file_path, "up", "-d"])
        cli_call(["docker-compose", "-f", self.compose_file_path, "up", "-d", "--scale", "cli=0"])

    def shutdown_test_env(self):
        cli_call(["docker-compose", "-f", self.compose_file_path, "down"])


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
