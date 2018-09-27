import time
import docker
import logging
import unittest

from .utils import BaseTestCase
from .config import E2E_CONFIG

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

CC_PATH = 'github.com/example_cc'
CC_NAME = 'example_cc'
CC_VERSION = '1.0'


class E2eTest(BaseTestCase):

    def setUp(self):
        super(E2eTest, self).setUp()

    def tearDown(self):
        super(E2eTest, self).tearDown()

    # Create an channel for further testing.
    def channel_create(self):

        logger.info("E2E: Channel creation start: name={}".format(
            self.channel_name))

        # By default, self.user is the admin of org1
        response = self.client.channel_create('orderer.example.com',
                                              self.channel_name,
                                              self.user,
                                              self.config_yaml,
                                              self.channel_profile)
        self.assertTrue(response)

        logger.info("E2E: Channel creation done: name={}".format(
            self.channel_name))

    # Join peers of two orgs into the existing channel
    def channel_join(self):

        # channel must already exist when to join
        channel = self.client.get_channel(self.channel_name)
        self.assertIsNotNone(channel)

        orgs = ["org1.example.com", "org2.example.com"]
        for org in orgs:
            org_admin = self.client.get_user(org, 'Admin')
            response = self.client.channel_join(
                requestor=org_admin,
                channel_name=self.channel_name,
                peer_names=['peer0.' + org, 'peer1.' + org],
                orderer_name='orderer.example.com'
            )
            self.assertTrue(response)
            # Verify the ledger exists now in the peer node
            dc = docker.from_env()
            for peer in ['peer0', 'peer1']:
                peer0_container = dc.containers.get(peer + '.' + org)
                code, output = peer0_container.exec_run(
                    'test -f '
                    '/var/hyperledger/production/ledgersData/chains/chains/{}'
                    '/blockfile_000000'.format(self.channel_name))
                self.assertEqual(code, 0, "Local ledger not exists")

    # Installing an example chaincode to peer
    def chaincode_install(self):

        orgs = ["org1.example.com", "org2.example.com"]
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")
            response = self.client.chaincode_install(
                requestor=org_admin,
                peer_names=['peer0.' + org, 'peer1.' + org],
                cc_path=CC_PATH,
                cc_name=CC_NAME,
                cc_version=CC_VERSION
            )
            self.assertTrue(response)
            # Verify the cc pack exists now in the peer node
            dc = docker.from_env()
            for peer in ['peer0', 'peer1']:
                peer0_container = dc.containers.get(peer + '.' + org)
                code, output = peer0_container.exec_run(
                    'test -f '
                    '/var/hyperledger/production/chaincodes/example_cc.1.0')
                self.assertEqual(code, 0, "chaincodes pack not exists")


    def chaincode_install_fail(self):
        pass

    # Instantiating an example chaincode to peer
    def chaincode_instantiate(self):

        orgs = ["org1.example.com"]
        args = ['a', '200', 'b', '300']
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")
            response = self.client.chaincode_instantiate(
                requestor=org_admin,
                channel_name=self.channel_name,
                peer_names=['peer0.' + org, 'peer1.' + org],
                args=args,
                cc_name=CC_NAME,
                cc_version=CC_VERSION
            )
            logger.info(
                "E2E: Chaincode instantiation response {}".format(response))
            self.assertTrue(response)


    # Invoking an example chaincode to peer
    def chaincode_invoke(self):

        orgs = ["org1.example.com"]
        args = ['a', 'b', '100']
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")
            response = self.client.chaincode_invoke(
                requestor=org_admin,
                channel_name=self.channel_name,
                peer_names=['peer0.' + org, 'peer1.' + org],
                args=args,
                cc_name=CC_NAME,
                cc_version=CC_VERSION
            )
            self.assertTrue(response)


    # Query installed chaincodes on peer
    def query_installed_chaincodes(self):

        orgs = ["org1.example.com", "org2.example.com"]
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")
            response = self.client.query_installed_chaincodes(
                requestor=org_admin,
                peer_names=['peer0.' + org, 'peer1.' + org],
            )
            self.assertEqual(
                response.chaincodes[0].name, CC_NAME, "Query failed")
            self.assertEqual(
                response.chaincodes[0].version, CC_VERSION, "Query failed")
            self.assertEqual(
                response.chaincodes[0].path, CC_PATH, "Query failed")


    # Querying channel
    def query_channels(self):

        orgs = ["org1.example.com"]
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")
            response = self.client.query_channels(
                requestor=org_admin,
                peer_names=['peer0.' + org, 'peer1.' + org],
            )
            self.assertEqual(
                response.channels[0].channel_id,
                'businesschannel',
                "Query failed")


    # Querying information on the state of the Channel
    def query_info(self):

        orgs = ["org1.example.com"]
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")
            response = self.client.query_info(
                requestor=org_admin,
                channel_name=self.channel_name,
                peer_names=['peer0.' + org, 'peer1.' + org],
            )
            self.assertEqual(
                response.height,
                3,
                "Query failed")


    # Querying block by tx id
    def query_block_by_txid(self):
        orgs = ["org1.example.com"]
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")
            response = self.client.query_block_by_txid(
                requestor=org_admin,
                channel_name=self.channel_name,
                peer_names=['peer0.' + org, 'peer1.' + org],
                tx_id=self.client.txid_for_test
            )
            self.assertEqual(
                response['header']['number'],
                1,
                "Query failed")


    # Querying block by block hash
    def query_block_by_hash(self):

        orgs = ["org1.example.com"]
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")

            response = self.client.query_info(
                requestor=org_admin,
                channel_name=self.channel_name,
                peer_names=['peer0.' + org, 'peer1.' + org],
            )

            response = self.client.query_block_by_hash(
                requestor=org_admin,
                channel_name=self.channel_name,
                peer_names=['peer0.' + org, 'peer1.' + org],
                block_hash=response.currentBlockHash
            )
            self.assertEqual(
                response['header']['number'],
                2,
                "Query failed")


    # Querying block by block number
    def query_block(self):

        orgs = ["org1.example.com"]
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")
            response = self.client.query_block(
                requestor=org_admin,
                channel_name=self.channel_name,
                peer_names=['peer0.' + org, 'peer1.' + org],
                block_number='1'
            )
            self.assertEqual(
                response['header']['number'],
                1,
                "Query failed")
            self.blockheader = response['header']


    # Querying transaction by tx id
    def query_transaction(self):

        orgs = ["org1.example.com"]
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")
            response = self.client.query_transaction(
                requestor=org_admin,
                channel_name=self.channel_name,
                peer_names=['peer0.' + org, 'peer1.' + org],
                tx_id=self.client.txid_for_test
            )
            self.assertEqual(
                response.get('transaction_envelope').get('payload').get(
                    'header').get('channel_header').get('channel_id'),
                self.channel_name,
                "Query failed")


    # Query instantiated chaincodes on peer
    def query_instantiated_chaincodes(self):

        orgs = ["org1.example.com", "org2.example.com"]
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")
            response = self.client.query_instantiated_chaincodes(
                requestor=org_admin,
                channel_name=self.channel_name,
                peer_names=['peer0.' + org, 'peer1.' + org]
            )
            self.assertEqual(
                response.chaincodes[0].name, CC_NAME, "Query failed")
            self.assertEqual(
                response.chaincodes[0].version, CC_VERSION, "Query failed")
            self.assertEqual(
                response.chaincodes[0].path, CC_PATH, "Query failed")

    def test_in_sequence(self):

        # channel methods
        self.channel_create()
        time.sleep(5)           # wait for channel creation
        self.channel_join()

        # chaincode methods
        self.chaincode_install()
        self.chaincode_install_fail()
        self.chaincode_instantiate()
        self.chaincode_invoke()

        # query methods
        self.query_installed_chaincodes()
        self.query_channels()
        self.query_info()
        self.query_block_by_txid()
        self.query_block_by_hash()
        self.query_block()
        self.query_transaction()
        self.query_instantiated_chaincodes()

        logger.info("E2E all test cases done\n\n")


if __name__ == "__main__":
    unittest.main()
