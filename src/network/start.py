import time
import json
import docker
import logging
import os
import sys
import unittest
from beeprint import pp, Config

import trustas

from .utils import BaseTestCase
from .config import E2E_CONFIG
from queue import Queue
from random import randint

from hfc.fabric.peer import create_peer
from hfc.protos.peer import query_pb2
from hfc.fabric.transaction.tx_context import create_tx_context
from hfc.fabric.transaction.tx_proposal_request import create_tx_prop_req, \
    CC_TYPE_GOLANG, CC_INSTANTIATE, CC_INSTALL, CC_INVOKE, CC_QUERY, TXProposalRequest
from hfc.util.crypto.crypto import ecies
from hfc.util.utils import send_transaction, build_tx_req
from .utils import get_peer_org_user, \
    BaseTestCase
from .e2e_utils import build_channel_request, \
    build_join_channel_req

# ----------
# SETTINGS

CREATE_LOGS     = True
KEEP_NETWORK    = False
WIPE_ALL        = False
LOG_FILE        = "logs/main.log"

DEFAULT_SLEEP   = 5
LONGER_SLEEP    = DEFAULT_SLEEP * 1.5
DOUBLE_SLEEP    = DEFAULT_SLEEP * 2

TEST_NETWORK    = E2E_CONFIG['test-network']
CC_PATH         = 'github.com/trustas_cc'
CC_NAME         = 'trustas_cc'
CC_VERSION      = '1.0'

# ----------

# logging config
logging.basicConfig(
    level=logging.DEBUG,
    filename=LOG_FILE if CREATE_LOGS else ""
)
logger = logging.getLogger(__name__)

# beeprint config
pp_conf = Config()
pp_conf.max_depth = 20
pp_conf.text_autoclip_maxline = 50

# ----------

def global_config():
    """Get configuration from environment variables"""

    global DEFAULT_SLEEP
    global KEEP_NETWORK
    global WIPE_ALL

    if "DEFAULT_SLEEP" in os.environ:
        DEFAULT_SLEEP = int(os.environ["DEFAULT_SLEEP"])
    if "KEEP_NETWORK" in os.environ:
        KEEP_NETWORK = os.environ["KEEP_NETWORK"] == "True"
    if "WIPE_ALL" in os.environ:
        WIPE_ALL = os.environ["WIPE_ALL"] == "True"

    logger.info('  - Default sleep time:         \t{} seconds'.format(DEFAULT_SLEEP))
    logger.info('  - Keep network running:       \t{}'.format(KEEP_NETWORK))
    logger.info('  - Wipe assets before running: \t{}'.format(WIPE_ALL))


class E2eTest(BaseTestCase):

    def setUp(self):
        global_config()  # get configuration from environment
        logger.info("\n\n\n\t--- SETTING UP NETWORK ---\n")
        super(E2eTest, self).setUp(wipe_all=WIPE_ALL)

    def tearDown(self):
        super(E2eTest, self).tearDown(keep_network=KEEP_NETWORK)
        logger.info("\n\n\t--- FINISHED E2E TEST ---\n")

    def test_in_sequence(self):
        """Test sequential execution"""

        self.__configure()      # set ledger configs
        self.__init_ledger()    # create the channel and init chaincode
        self.__cc_ops()         # run chaincode operations (e.g. queries)

        input("Press Enter to finish experiment")


    def __cc_ops(self):

        # create an agreement and wait
        args = ['123', '456', 'SLA_MAROTO', 'aid_p1234567890']
        self.__cc_call('createAgreement', args)
        time.sleep(DEFAULT_SLEEP)

        # query an agreement
        args = ['aid_p1234567890']
        res = self.__cc_call('queryAgreement', args=args, prop_type=CC_QUERY)
        logger.info("Query Result: %s", json.dumps(res).encode('utf-8'))


    def __configure(self):
        """Get network configuration and make it available from self."""

        peer_config = TEST_NETWORK['org1.example.com']['peers']['peer0']

        endpoint = peer_config['grpc_request_endpoint']
        tls_cacerts = peer_config['tls_cacerts']
        opts = (('grpc.ssl_target_name_override',
                 peer_config['server_hostname']), )
        peer = create_peer(
            endpoint=endpoint, tls_cacerts=tls_cacerts, opts=opts)

        self.peers = [peer]
        self.org1 = 'org1.example.com'
        self.crypto = ecies()
        self.ixp_admin = get_peer_org_user(self.org1, 'Admin',
                                            self.client.state_store)


    def __init_ledger(self):
        """Creates channel and chaincode"""

        # create channel and join it
        self.__create_channel()
        time.sleep(DEFAULT_SLEEP)
        self.__join_channel()
        time.sleep(DEFAULT_SLEEP)

        # install and instantiate the chaincode
        self.__cc_install()
        time.sleep(DEFAULT_SLEEP)
        args = ['a', '100', 'b', '40']
        self.__cc_call(fcn='init', args=args, prop_type=CC_INSTANTIATE)


    def __create_channel(self):
        """Creates the default channel"""

        request = build_channel_request(self.client, self.channel_tx,
                                        self.channel_name)
        res = self.client._create_channel(request)

    def __join_channel(self, create_new_channel=True):
        """Joins the default channel"""

        if create_new_channel:
            self.channel = self.client.new_channel(self.channel_name)
            join_req = build_join_channel_req(self.org1, self.channel, self.client)
            self.channel.join_channel(join_req)
        # else:
        #     logger.warn("create_new_channel flag is not stable")
        #     self.channel = self.client.channel_join(
        #         self.client, self.channel_name, self.peers,
        #         TEST_NETWORK["orderer"]["mspid"])
        #     print(type(self.channel), self.channel) # bool, False


    def __cc_install(self):
        """Installs chaincode"""

        tran_prop_req_in = create_tx_prop_req(
            prop_type=CC_INSTALL,
            cc_path=CC_PATH,
            cc_type=CC_TYPE_GOLANG,
            cc_name=CC_NAME,
            cc_version=CC_VERSION)
        tx_ctx = create_tx_context(self.ixp_admin, self.crypto,
                                   tran_prop_req_in)
        self.client.send_install_proposal(tx_ctx, self.peers)


    def __cc_call(self, fcn, args, prop_type=CC_INVOKE):
        """Instantiate chaincode or invoke a cc function with args

        Args:
            fcn:        Chaincode function name
            args:       Chaincode function arguments
            prop_type:  Proposal request type (default CC_INVOKE)
        Returns:
            Chaincode response
            None when prop_type is not valid
        """

        tran_prop_req = create_tx_prop_req(
            prop_type=prop_type,
            cc_type=CC_TYPE_GOLANG,
            cc_name=CC_NAME,
            cc_version=CC_VERSION,
            fcn=fcn,
            args=args)
        tx_ctx = create_tx_context(self.ixp_admin, self.crypto, tran_prop_req)

        # invoke calls
        if prop_type == CC_INVOKE:
            # send standard invocation
            res = self.channel.send_tx_proposal(tx_ctx, self.peers)

        # query calls
        elif prop_type == CC_QUERY:
            response = self.channel.send_tx_proposal(tx_ctx, self.peers)
            q = Queue(1)
            response.subscribe(
                on_next=lambda x: q.put(x), on_error=lambda x: q.put(x))

            try:
                res = q.get(timeout=DEFAULT_SLEEP)
                logger.debug(res)
                response = res[0][0][0]
                if response.response:
                    pld = response.response.payload
                    logger.debug("Query Payload: %s", pld)
                    pld = json.loads(pld.decode('utf-8'))
                    return pld
                return response

            except Exception:
                logger.error("Failed to query chaincode: {}", sys.exc_info()[0])
                raise

        # instantiate calls
        elif prop_type == CC_INSTANTIATE:
            # instantiate chaincode and wait for propagation
            res = self.channel.send_instantiate_proposal(tx_ctx, self.peers)
            time.sleep(LONGER_SLEEP)

        # invalid call
        else:
            logger.error("Invalid proposal request type." + \
            "Must be {} or {}.".format(CC_INVOKE, CC_INSTANTIATE))

            return None

        # send the transaction to the channel
        tran_req = build_tx_req(res)
        tx_2_ctx = create_tx_context(self.ixp_admin, self.crypto,
                                     TXProposalRequest())
        response = send_transaction(self.channel.orderers, tran_req, tx_2_ctx)

        # wait for chaincode instantiation consensus
        if prop_type == CC_INSTANTIATE:
            time.sleep(LONGER_SLEEP)

        # collect results
        q = Queue(1)
        response.subscribe(
            on_next=lambda x: q.put(x), on_error=lambda x: q.put(x))
        res, _ = q.get(timeout=DEFAULT_SLEEP)
        # self.assertEqual(res.status, 200)

        return res


if __name__ == "__main__":
    unittest.main()
