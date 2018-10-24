#!/usr/bin/env python3
import getopt
import logging
import os
import sys
import unittest

from beeprint import pp
from trustas import experiments
from network import start
from network import tests as net_tests

# SETTINGS
RUN_EXPERIMENTS = False     # Run TrustAS experiments
RUN_TESTS = False           # Run unit and e2e tests
KEEP_NETWORK = False        # Keeps network running when finished
DEFAULT_SLEEP = 4           # Default sleep time (seconds)
WIPE_ALL = False            # Wipes all Docker assets before starting

# logging config
CREATE_LOGS = True
LOG_FILE    = "logs/main.log"
logging.basicConfig(
    level       = logging.DEBUG,
    filename    = LOG_FILE if CREATE_LOGS else "")
logger = logging.getLogger(__name__)

MODULES = [{
    'name': "Network",
    'module': net_tests,
    'testable': True,
}]

def testModule(module):
    suite = unittest.TestLoader().loadTestsFromModule(module)
    return unittest.TextTestRunner(verbosity=0).run(suite)

def tests():
    for m in MODULES:
        if ("testable" not in m) or (not m["testable"]):
            continue
        result = testModule(m["module"])
        if len(result.failures) > 0:
            print("\t[ ABORTING: {} module failed one or more tests ]\n".format(m["name"]))
            exit(1)
        if len(result.errors) > 0:
            print("\t[ ABORTING: {} had an execution error ]\n".format(m["name"]))
            exit(1)

    print("\n\tPASS: All tests were successful :)\n")


def help_and_exit(EXIT_CODE=0):
    """Print command line help and finishes execution"""

    msg = "\n USAGE:\t\t./main.py [OPTIONS]\n" + \
        "\n OPTIONS:\n" + \
        "\n\t-h  --help              Displays this message." + \
        "\n\t-w  --wipe              Wipes all Docker assets before starting (runs './cleanup.sh')." + \
        "\n\t-k  --keep              Keeps network running after execution (no 'docker-compose down')." + \
        "\n\t-s TIME --sleep TIME    Set default sleep time used to TIME." + \
        "\n\n"
    print(msg)
    sys.exit(EXIT_CODE)

def config(argv):
    """Get arguments from command line"""

    global KEEP_NETWORK
    global DEFAULT_SLEEP
    global WIPE_ALL

    try:
        opts, args = getopt.getopt(
            argv, "hwks:",
            ["help", "wipe", "keep", "sleep="])
    except getopt.GetoptError:
        help_and_exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help_and_exit()
        elif opt in ("-w", "--wipe"):
            WIPE_ALL = True
        elif opt in ("-k", "--keep"):
            KEEP_NETWORK = True
        elif opt in ("-s", "--sleep"):
            DEFAULT_SLEEP = arg

    os.environ["DEFAULT_SLEEP"] = str(DEFAULT_SLEEP)
    os.environ["KEEP_NETWORK"] = str(KEEP_NETWORK)
    os.environ["WIPE_ALL"] = str(WIPE_ALL)

    print('')
    print(' -> Default sleep time:           \t{} s'.format(
        os.environ["DEFAULT_SLEEP"]))
    print(' -> Keeping network running:      \t{}'.format(os.environ["KEEP_NETWORK"]))
    print(' -> Wiping assets before running: \t{}'.format(os.environ["WIPE_ALL"]))
    print('')


if __name__ == "__main__":

    config(sys.argv[1:])

    print("\n\n" + \
            "\t ______                        __    ______  _____.      \n" + \
            "\t/\__  _\                      /\ \__/\  _  \/\  ___\     \n" + \
            "\t\/_/\ \/ _ __   __  __    ____\ \ ,_\ \ \L\ \ \ \____   \n" + \
            "\t   \ \ \/\`'__\/\ \/\ \  /',__\\\ \ \\/\ \  __ \ \ __  \   \n" + \
            "\t    \ \ \ \ \/ \ \ \_\ \/\__, `\\\ \ \_\ \ \/\ \/____\ \ \n" + \
            "\t     \ \_\ \_\  \ \____/\/\____/ \ \__\\\ \_\ \_\/\_____\ \n" + \
            "\t      \/_/\/_/   \/___/  \/___/   \/__/ \/_/\/_/\______/\n\n\n")

    if RUN_TESTS:
        tests()

    if RUN_EXPERIMENTS:
        experiments.run()

    testModule(start)
