import time
import json
import docker
import logging
import sys
import unittest
from beeprint import pp, Config

import trustas

from .utils import BaseTestCase
from .config import E2E_CONFIG
from random import randint

CREATE_LOGS = True
LOG_FILE = "logs/main.log"
CC_PATH = 'github.com/trustas_cc'
CC_NAME = 'trustas_cc'
CC_VERSION = '1.0'

logging.basicConfig(
    level=logging.DEBUG, filename=LOG_FILE if CREATE_LOGS else "")
logger = logging.getLogger(__name__)


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
                    '/var/hyperledger/production/chaincodes/' + CC_NAME + '.' + CC_VERSION)
                self.assertEqual(code, 0, "chaincodes pack not exists")


    # Instantiating an example chaincode to peer
    def chaincode_instantiate(self, args=['a', '200', 'b', '300']):

        orgs = ["org1.example.com"]
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
    def chaincode_invoke(self, args=['a', 'b', '100']):

        orgs = ["org1.example.com"]
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
    def query_block(self, block_number=0):

        orgs = ["org1.example.com"]
        for org in orgs:
            org_admin = self.client.get_user(org, "Admin")
            response = self.client.query_block(
                requestor=org_admin,
                channel_name=self.channel_name,
                peer_names=['peer0.' + org, 'peer1.' + org],
                block_number=str(block_number)
            )
            self.assertEqual(
                response['header']['number'],
                block_number,
                "Query failed: block numbers do not match")
            self.blockheader = response['header']

        return response

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

        return response.get('transaction_envelope').get('payload')

    # Create channel and join
    def channel_init(self):
        self.channel_create()
        time.sleep(5)  # wait for channel creation
        self.channel_join()

    # install and instantiate chaincode
    def chaincode_init(self):
        # chaincode methods
        self.chaincode_install()
        self.chaincode_instantiate()

    # Testing routine
    def test_in_sequence(self):

        pp_conf = Config()
        pp_conf.max_depth = 20
        pp_conf.text_autoclip_maxline = 50

        # initialization
        # self.channel_init()
        # self.chaincode_init()

        self.channel_create()
        time.sleep(5)  # wait for channel creation
        self.channel_join()

        self.chaincode_install()
        self.chaincode_instantiate(args=['a', '100', 'b', '100'])
        self.chaincode_invoke(args=['a', 'b', '20'])

        # custom operations
        # sla, met = self.fabricate_sla_and_metrics()
        # self.chaincode_invoke(args=['a', 'b', sla])

        res = self.query_block(block_number=2)
        # res = self.query_transaction()
        pp(res, config=pp_conf)

        # input("Press ENTER to end tests")

        logger.info("Sequential test done\n\n")

    def fabricate_sla_and_metrics(self):

        # agreement properties and sample measurement
        asn_a   = randint(0, 2**15-1)
        asn_b   = randint(2**15, 2**16-1)
        peers   = { asn_a, asn_b }
        sla     = trustas.sla.SLA(latency=5)
        metrics = trustas.sla.SLA(latency=8)

        # create an agreement
        agreement = trustas.agreement.Agreement(SLA=sla, peers=peers)
        agreement.append_metrics(metrics)

        # get encrypted properties
        enc_sla = agreement.get_encrypted_sla()
        enc_met = agreement.get_encrypted_metrics()

        # sanity check
        self.assertGreater(
            enc_met[0]['latency'],
            enc_sla['latency'],
            "The latency measured should be greater than the SLA's even after encrypted."
        )

        return json.dumps(enc_sla), json.dumps(enc_met)


if __name__ == "__main__":
    unittest.main()
