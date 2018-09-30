#!/usr/bin/env python3
import unittest
from beeprint import pp
from network import start
from network import tests as net_tests

RUN_TESTS = False
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


if __name__ == "__main__":

    """
        ______                        __    ______  _____
        /\__  _\                      /\ \__/\  _  \/\  _ `\
        \/_/\ \/ _ __   __  __    ____\ \ ,_\ \ \L\ \ \,\L\_\
        \ \ \/\`'__\/\ \/\ \  /',__\\ \ \/\ \  __ \/ \__ \
            \ \ \ \ \/ \ \ \_\ \/\__, `\\ \ \_\ \ \/\ \/\ \L\ \
            \ \_\ \_\  \ \____/\/\____/ \ \__\\ \_\ \_\ `\____\
            \/_/\/_/   \/___/  \/___/   \/__/ \/_/\/_/\/_____/
    """

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

    # testModule(start)
