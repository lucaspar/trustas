import csv
import json
import logging
import os
import random
import sys
import time
import unittest

import matplotlib.pyplot as plt
from beeprint import pp, Config
from queue import Queue
from hfc.fabric.peer import create_peer
from hfc.protos.peer import query_pb2
from hfc.fabric.transaction.tx_context import create_tx_context
from hfc.fabric.transaction.tx_proposal_request import create_tx_prop_req, \
    CC_TYPE_GOLANG, CC_INSTANTIATE, CC_INSTALL, CC_INVOKE, CC_QUERY, TXProposalRequest
from hfc.util.crypto.crypto import ecies
from hfc.util.utils import send_transaction, build_tx_req

import trustas
from .config import E2E_CONFIG
from .utils import get_peer_org_user, BaseTestCase, cli_call, mkdir_p
from .e2e_utils import build_channel_request, build_join_channel_req

# ----------
# SETTINGS

KEEP_NETWORK    = False
WIPE_ALL        = False
EXP_DIR         = "experiments"

DEFAULT_SLEEP   = 5
HALF_SLEEP      = DEFAULT_SLEEP * 0.5
LONGER_SLEEP    = DEFAULT_SLEEP * 1.5
DOUBLE_SLEEP    = DEFAULT_SLEEP * 2

TEST_NETWORK    = E2E_CONFIG['test-network']
CC_PATH         = 'github.com/trustas_cc'
CC_NAME         = 'trustas_cc'
CC_VERSION      = '1.0'

logger = logging.getLogger(__name__)

# ----------

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

    def __craft_settings(self):
        """Set interconnection settings"""

        privacy = True      # storage privacy: True means encryption is enabled
        net_size = 100      # network size: number of ASes in the IXP
        connections = 100   # total number of pair interconnections / agreements in the network
        mpa = 1             # number of metrics per agreement
        mode = "ciphertext" if privacy else "plaintext"
        path = os.path.join(
            "A", mode, "{}_{}_{}".format(net_size, connections, mpa), str(time.time()))

        return {
            "privacy": privacy,
            "experiment_path": path,
            "network_size": net_size,
            "connections": connections,
            "mpa": mpa,
            "storage": "json"
        }


    def __cc_ops(self):
        """A sequence of chaincode operations simulating agreements"""

        exp_settings = self.__craft_settings()   # create settings
        agreements = trustas.experiments.exp_privacy_cost(**exp_settings)   # simulate agreements

        # create agreement entries in the ledger
        print(" > Saving agreements to the ledger")
        data_x, data_y = self.__save_agreements(
            agreements, privacy=exp_settings["privacy"])

        # save storage data to files
        print(" > Saving statistics")
        save_data(
            data_x,
            data_y,
            file="size_creation",
            title="Blockchain growth (agreement creation only)",
            path=exp_settings["experiment_path"],
            xlabel="Number of agreements published",
            ylabel="Blockchain size (KB)")

        # create measurement entries in the ledger
        print(" > Saving measurements to the ledger")
        data_x, data_y = self.__save_measurements(
            agreements, privacy=exp_settings["privacy"])

        # save storage data to files
        print(" > Saving statistics")
        save_data(
            data_x,
            data_y,
            file="size_{}_measurements".format(exp_settings["mpa"]),
            title="Blockchain growth ({} measurement(s) per agreement)".format(
                exp_settings["mpa"]),
            path=exp_settings["experiment_path"],
            xlabel="Number of measurements published",
            ylabel="Blockchain size (KB)")

        time.sleep(DEFAULT_SLEEP)

        # query a random agreement
        args = [str(random.choice(agreements).id)]
        res = self.__cc_call('queryAgreement', args=args, prop_type=CC_QUERY)
        logger.info("Query Result: %s", json.dumps(res).encode('utf-8'))

    def __save_measurements(self, agreements, privacy=True, monitor_size=True):
        """Save measurements in agreements to the ledger"""

        data_x = []
        data_y = []
        for idx, ag in enumerate(agreements):
            metrics = ag.get_encrypted_metrics() if privacy else ag.get_plaintext_metrics()
            for idxm, m in enumerate(metrics):
                args = [
                    str(ag.id),             # agreement ID
                    str(ag.id) + str(idxm), # measurement ID
                    json.dumps(m)           # single set of metrics
                ]
                self.__cc_call('publishMeasurement', args)

            if monitor_size and (idx + 1) % 10 == 0:
                time.sleep(HALF_SLEEP)
                data_x.append(idx + 1)
                data_y.append(measure_blockchain_size())

        return data_x, data_y

    def __save_agreements(self, agreements, privacy=True, monitor_size=True):
        """Save agreements to the ledger"""

        data_x = []
        data_y = []
        for idx, ag in enumerate(agreements):
            peers = ag.peers
            sla = json.dumps(ag.get_encrypted_sla() if privacy else ag.get_plaintext_sla())
            args = [
                str(ag.id),     # agreement ID
                str(peers[0]),  # peer A
                str(peers[1]),  # peer B
                sla             # agreement SLA
            ]
            self.__cc_call('createAgreement', args)

            if monitor_size and (idx + 1) % 10 == 0:
                time.sleep(HALF_SLEEP)
                data_x.append(idx+1)
                data_y.append(measure_blockchain_size())

        return data_x, data_y


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

        return res


def save_data(x, y, path, file, title='', label='', xlabel='', ylabel='', legend=''):
    """Saves generated data (plot + csv) to path.

    Args:
        x:          X axis data.
        y:          Y axis data.
        path:       part of output directory as in: [EXP_DIR]/[path]/data
        title:      title of plot.
        file:       filenames used for svg and csv output
        xlabel:     X axis label.
        ylabel:     Y axis label.
        legend:     plot legend.
    Returns:
        None (only outputs files).
    """
    working_dir = os.path.join(EXP_DIR, path, "data")
    mkdir_p(working_dir)
    svg_filepath = os.path.join(working_dir, file + ".svg")
    csv_filepath = os.path.join(working_dir, file + ".csv")

    # plot and save
    plt.clf()                   # clear old plots
    plt.plot(x, y, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(legend)
    plt.savefig(svg_filepath)

    # build csv and save
    rows = zip(x, y)
    with open(csv_filepath, 'w+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([xlabel, ylabel])
        for r in rows:
            spamwriter.writerow(r)


def measure_blockchain_size(peer="peer0.org1.example.com"):
    """Measures blockchain size through a command line call to a container.

    Args:
        peer:   The container name (also full peer name) to consult.
    Returns:
        Integer representing the current ledger size in KB (1024B) on disk.
    """

    output, error, _ = cli_call([
        "docker", "exec", "-it", peer, "du",
        "/var/hyperledger/production/ledgersData/chains/chains/businesschannel"
    ])
    if error:
        return None
    try:
        size = output.decode("utf-8").split()[0]
        size = int(size)
        return size
    except:
        return None


if __name__ == "__main__":
    unittest.main()
