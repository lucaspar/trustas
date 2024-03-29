# Data structure for Service Level Agreements
# Can describe an SLA agreed (ideal) or a set of measured properties (real)

import uuid
from pyope import ope
import trustas

class Agreement:
    """Describes an agreement between ASes (peers).

    Attributes:
        id:         An uuid for this agreement.
        enc_key:    Key used to encrypt SLA and metrics before
                    making them public. Comes from SLA class.
        sla:        SLA set for this agreement.
    """

    def __init__(self, SLA, peers):
        """Instantiates a new agreement.

        Args:
            SLA:    An SLA instance describing the agreement.
            peers:  A Set of ASNs which are part of the agreement.
        Raises:
            ValueError: If "peers" does not contain two ASNs
        """

        p = list(peers)
        if len(p) != 2 or not \
            (isinstance(p[0], int) and isinstance(p[1], int)):
            raise ValueError("Argument peers must contain two integers")
        if not isinstance(SLA, trustas.sla.SLA):
            raise ValueError("Argument SLA must be instance of trustas.sla.SLA")

        self.__met = []
        self.__met_enc = []
        self.__peers = peers
        self.__sla = SLA
        self.id = uuid.uuid4()
        self.enc_key, self.__sla_enc = SLA.encrypt()

    @property
    def sla(self):
        return self.__sla

    @property
    def peers(self):
        return list(self.__peers)

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

    def get_plaintext_sla(self):
        """Returns PLAINTEXT SLA of agreement [dict]."""
        return self.__sla.extract()

    def get_plaintext_metrics(self):
        """Returns PLAINTEXT agreement metrics [list of dicts]."""
        plain_metrics = []
        for m in self.__met:
            plain_metrics.append(m.extract())
        return plain_metrics
