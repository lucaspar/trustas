# Data structure for Service Level Agreements
# Can describe an SLA agreed (ideal) or a set of measured properties (real)

import uuid
from pyope import ope

class Agreement:
    """Describes an agreement between ASes (peers).

    Attributes:
        id:         An uuid for this agreement.
        enc_key:    Key used to encrypt SLA and metrics before
                    making them public. Comes from SLA class.
    """

    def __init__(self, SLA, peers):
        """Instantiates a new agreement.

        Args:
            SLA:    An SLA instance describing the agreement.
            peers:  A Set of ASNs which are part of the agreement.
        """
        self.__met = []
        self.__met_enc = []
        self.__sla = SLA
        self.id = uuid.uuid4()
        self.enc_key, self.__sla_enc = SLA.encrypt()

    # Appends a set of measurements to this agreement
    def append_metrics(self, metrics):
        """Appends metrics to this Agreement object.

        Args:
            metrics:    An SLA instance.
        Returns:
            None
        Raises:
            Nothing
        """
        self.__met.append(metrics)
        _, metrics_encrypted = metrics.encrypt(self.enc_key)
        self.__met_enc.append(metrics_encrypted)

    def get_encrypted_sla(self):
        """Returns encrypted SLA of agreement [dict]."""
        return self.__sla_enc

    def get_encrypted_metrics(self):
        """Returns encrypted agreement metrics [list of dicts]."""
        return self.__met_enc
