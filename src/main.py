import unittest

from network import tests as net_tests
from trustas import tests as tru_tests

def testTrustAS():
    suite = unittest.TestLoader().loadTestsFromModule(tru_tests)
    return unittest.TextTestRunner(verbosity=0).run(suite)

def testNetwork():
    suite = unittest.TestLoader().loadTestsFromModule(net_tests)
    return unittest.TextTestRunner(verbosity=0).run(suite)

def tests():

    print("\n\n" + \
            "\t ______                        __    ______  ____       \n" + \
            "\t/\__  _\                      /\ \__/\  _  \/\  _`\     \n" + \
            "\t\/_/\ \/ _ __   __  __    ____\ \ ,_\ \ \L\ \ \,\L\_\   \n" + \
            "\t   \ \ \/\`'__\/\ \/\ \  /',__\\\ \ \\/\ \  __ \/_\__ \   \n" + \
            "\t    \ \ \ \ \/ \ \ \_\ \/\__, `\\\ \ \_\ \ \/\ \/\ \L\ \ \n" + \
            "\t     \ \_\ \_\  \ \____/\/\____/ \ \__\\\ \_\ \_\ `\____\ \n" + \
            "\t      \/_/\/_/   \/___/  \/___/   \/__/ \/_/\/_/\/_____/\n" + \
            "\t                                                        \n" + \
            "\t                                                        \n\n")

    res = testTrustAS()
    if len(res.failures) > 0:
        print("\t[ ABORTING: TrustAS tests failed ]\n")
        exit(1)

    res = testNetwork()
    if len(res.failures) > 0:
        print("\t[ ABORTING: Network tests failed ]\n")
        exit(1)

    print("\tPASS: All tests were successful :)\n")

if __name__ == "__main__":
    tests()
