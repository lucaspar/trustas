# Data structure for Service Level Agreements
# Can describe an SLA agreed (ideal) or a set of measured properties (real)

import uuid
from pyope import ope

class Agreement:

    def __init__(self, SLA, peers):
        self.met = []
        self.met_enc = []
        self.sla = SLA
        self.id = uuid.uuid4()
        self.encryption_key, self.sla_enc = SLA.encrypt()

    # Appends a set of measurements to this agreement
    def append_metrics(self, metrics):
        self.met.append(metrics)
        _, metrics_encrypted = metrics.encrypt(self.encryption_key)
        self.met_enc.append(metrics_encrypted)

    # Returns the encrypted SLA for publishing
    def get_encrypted_sla(self):
        return self.sla_enc

    # Returns the encrypted metrics list for publishing
    def get_encrypted_metrics(self):
        print(type(self.met_enc))
        return self.met_enc
