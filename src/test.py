#!/usr/bin/python3
import unittest
from trustas import tests
from trustas import api

# run all tests with unittest
def runTests():
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    return unittest.TextTestRunner(verbosity=0).run(suite)

if __name__ == "__main__":
    print("\n\t\t>>> TrustAS <<<\n")

    res = runTests()
    if len(res.failures) > 0:
        print("\t[ ABORTING: One or more tests did not pass ]\n")
        exit(1)
    else:
        print("\tPASS: TrustAS tests")
