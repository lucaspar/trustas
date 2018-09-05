#!/usr/bin/python3
from pyope import ope

def testPyope():

    random_key = ope.OPE.generate_key()
    cipher = ope.OPE(random_key)
    a = cipher.encrypt(1000)
    b = cipher.encrypt(3000)
    c = cipher.encrypt(3000)

    assert a < b and b == c
    assert cipher.decrypt(cipher.encrypt(1337)) == 1337

    print("\n\t>>> PASS: OPE test <<<\n")
