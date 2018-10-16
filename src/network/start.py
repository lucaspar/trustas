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
LOG_FILE        = "logs/main.log"

TEST_NETWORK    = E2E_CONFIG['test-network']
CC_PATH         = 'github.com/trustas_cc'
CC_NAME         = 'trustas_cc'
CC_VERSION      = '1.0'
DEFAULT_SLEEP   = 4

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


class E2eTest(BaseTestCase):

    def setUp(self):
        super(E2eTest, self).setUp()

    def tearDown(self):
        super(E2eTest, self).tearDown()

    def test_in_sequence(self):
        """Test sequential execution"""

        # set ledger configs
        self.__configure()

        # create the channel and chaincode
        self.__init_ledger()

        # create an agreement
        args = ['123', '456', 'SLA_MAROTO', 'aid_p1234567890']
        self.__cc_call('createAgreement', args)
        time.sleep(DEFAULT_SLEEP)

        # query an agreement
        args = ['aid_p1234567890']
        res = self.__cc_query('queryAgreement', args=args)
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
        self.org1_admin = get_peer_org_user(self.org1, 'Admin',
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


    def __cc_query(self, fcn, args):
        """Runs chaincode query functions"""

        request = create_tx_prop_req(
            prop_type=CC_QUERY,
            cc_name=CC_NAME,
            cc_type=CC_TYPE_GOLANG,
            fcn=fcn,
            args=args)

        tx_context = create_tx_context(self.org1_admin, self.crypto,
                                       TXProposalRequest())
        tx_context.tx_prop_req = request

        response = self.channel.send_tx_proposal(
            tx_context, self.peers)

        queue = Queue(1)
        response.subscribe(
            on_next=lambda x: queue.put(x), on_error=lambda x: queue.put(x))

        try:
            res = queue.get(timeout=DEFAULT_SLEEP)
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

    def __create_channel(self):
        """Creates the default channel"""

        request = build_channel_request(self.client, self.channel_tx,
                                        self.channel_name)
        self.client._create_channel(request)

    def __join_channel(self):
        """Joins the default channel"""

        self.channel = self.client.new_channel(self.channel_name)
        join_req = build_join_channel_req(self.org1, self.channel, self.client)
        self.channel.join_channel(join_req)

    def __cc_install(self):
        tran_prop_req_in = create_tx_prop_req(
            prop_type=CC_INSTALL,
            cc_path=CC_PATH,
            cc_type=CC_TYPE_GOLANG,
            cc_name=CC_NAME,
            cc_version=CC_VERSION)
        tx_ctx = create_tx_context(self.org1_admin, self.crypto,
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
        tx_ctx = create_tx_context(self.org1_admin, self.crypto, tran_prop_req)

        # invoke vs instantiate
        if prop_type == CC_INVOKE:
            # send standard invocation
            res = self.channel.send_tx_proposal(tx_ctx, self.peers)
        elif prop_type == CC_INSTANTIATE:
            # instantiate chaincode and wait for propagation
            res = self.channel.send_instantiate_proposal(tx_ctx, self.peers)
            time.sleep(DEFAULT_SLEEP)
        else:
            logger.error("Invalid proposal request type." + \
            "Must be {} or {}.".format(CC_INVOKE, CC_INSTANTIATE))

            return None

        # send the transaction to the channel
        tran_req = build_tx_req(res)
        tx_2_ctx = create_tx_context(self.org1_admin, self.crypto,
                                     TXProposalRequest())
        response = send_transaction(self.channel.orderers, tran_req, tx_2_ctx)

        # wait for chaincode instantiation consensus
        if prop_type == CC_INSTANTIATE:
            time.sleep(DEFAULT_SLEEP)

        # collect results
        q = Queue(1)
        response.subscribe(
            on_next=lambda x: q.put(x), on_error=lambda x: q.put(x))
        res, ign = q.get(timeout=DEFAULT_SLEEP)
        # self.assertEqual(res.status, 200)

        return res


if __name__ == "__main__":
    unittest.main()
