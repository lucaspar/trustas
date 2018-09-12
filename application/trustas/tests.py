#!/usr/bin/python3
import unittest
from . import api
from pyope import ope
from random import randint
from .sla import SLA

# Unit tests for TrustAS

class TestExternalDependencies(unittest.TestCase):

    def test_pyope_integers(self):

        random_key = ope.OPE.generate_key()
        cipher = ope.OPE(random_key)
        a = cipher.encrypt(1000)
        b = cipher.encrypt(3000)
        c = cipher.encrypt(3000)

        self.assertTrue(a < b and b == c)
        self.assertTrue(cipher.decrypt(cipher.encrypt(1337)) == 1337)

    def test_pyope_boundaries(self):

        IN_BOUND = 2**32
        OUT_BOUND = 2**64

        random_key = ope.OPE.generate_key()
        cipher = ope.OPE(random_key,
            in_range=ope.ValueRange(-IN_BOUND+1, IN_BOUND-1),
            out_range=ope.ValueRange(-OUT_BOUND+1, OUT_BOUND-1)
        )

        a = cipher.encrypt(IN_BOUND-2)
        b = cipher.encrypt(IN_BOUND-1)
        c = cipher.encrypt(4294967295)
        self.assertTrue(a < b and b == c)

        d = cipher.encrypt(-IN_BOUND+1)
        e = cipher.encrypt(-IN_BOUND+2)
        f = cipher.encrypt(-4294967294)
        self.assertTrue(d < e and e == f)

        self.assertTrue(cipher.decrypt(cipher.encrypt(-1337)) == -1337)

class TestTrustAS(unittest.TestCase):

    def test_SLA(self):
        sampleSLA = SLA()
        self.assertTrue(sampleSLA.bandwidth > 0)

    def testAgreementCreation(self):
        sla = SLA()
        asn = randint(0, 2**16-1)
        aid, _, _ = api.createAgreement(asn, sla)
        self.assertTrue(len(str(aid)) == 36)

    def testMeasurementsPublishing(self):

        asn = randint(0, 2**16-1)
        sla = SLA(latency=5)
        measurements = SLA(latency=8)

        aid, enc_key, sla_data = api.createAgreement(asn, sla)
        measured_data = api.publishMeasurements(aid, measurements, enc_key)

        # measured_data and sla_data contain only encrypted info
        self.assertGreater( measured_data['latency'],
            sla_data['latency'],
            "The latency measured should be greater than the SLA's even after encrypted."
        )

        print("LATENCY")
        print("Plaintext:\tMeasured: {},\t\tSLA: {}".format(measurements.latency, sla.latency))
        print("Ciphertext:\tMeasured: {},\t\tSLA: {}".format(measured_data['latency'], sla_data['latency']))
        print("\n")

    def testASHistoryRetrieval(self):

        # define asn, sla and create an agreement
        asn = randint(0, 2**16-1)
        sla = SLA(latency=5)
        # aid = None
        aid, enc_key, sla_data = api.createAgreement(asn, sla)

        # simulate a few measurements and publish
        enc_measurements = []
        measurements = [ SLA(latency=8), SLA(latency=4), SLA(latency=5) ]
        for m in measurements:
            enc_measurements.append(api.publishMeasurements(aid, m, enc_key))

        # retrieve AS history
        history = api.retrieveASHistory(asn)
        # print(history)
