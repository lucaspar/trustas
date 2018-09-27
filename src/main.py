#!/usr/bin/env python3
import unittest

from network import start
from network import tests as net_tests
from trustas import tests as tru_tests

RUN_TESTS = True
MODULES = [{
    'name': "TrustAS",
    'module': tru_tests,
    'testable': True,
}, {
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
    print("\tPASS: All tests were successful :)\n")

if __name__ == "__main__":

    print("\n\n" + \
            "\t ______                        __    ______  ____       \n" + \
            "\t/\__  _\                      /\ \__/\  _  \/\  _`\     \n" + \
            "\t\/_/\ \/ _ __   __  __    ____\ \ ,_\ \ \L\ \ \,\L\_\   \n" + \
            "\t   \ \ \/\`'__\/\ \/\ \  /',__\\\ \ \\/\ \  __ \/_\__ \   \n" + \
            "\t    \ \ \ \ \/ \ \ \_\ \/\__, `\\\ \ \_\ \ \/\ \/\ \L\ \ \n" + \
            "\t     \ \_\ \_\  \ \____/\/\____/ \ \__\\\ \_\ \_\ `\____\ \n" + \
            "\t      \/_/\/_/   \/___/  \/___/   \/__/ \/_/\/_/\/_____/\n\n\n")

    if RUN_TESTS:
        tests()
