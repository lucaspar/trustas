# Data structure for Service Level Agreements
# Can describe an SLA agreed (ideal) or a set of measured properties (real)
import math
import random

from pyope import ope

class SLA:
    """Represents a Service Level Agreement or a set of measured properties.

    The SLA by itself does not imply there exists an agreement. See the Agreement class for that.

    """

    # >>>>>>> EXPERIMENTS WITH OPE PRECISION x DATA SIZE <<<<<<<<<
    # Known properties of the SLA.
    # Only these will be encrypted and passed to the blockchain.
    PROPS = {
        'bandwidth'     : { 'type': int,   'min': 1, 'max': 1e6,  'precision': 1,     'desc': 'Available bandwidth [Mbps]'},
        'latency'       : { 'type': int,   'min': 0, 'max': 1e3,  'precision': 1,     'desc': 'Expected latency [ms]'},        # latencies >1s are too high
        'packet_loss'   : { 'type': float, 'min': 0, 'max': 1e2,  'precision': 1e-2,  'desc': 'Expected packet loss [%]'},
        'jitter'        : { 'type': int,   'min': 0, 'max': 1e3,  'precision': 1,     'desc': 'Expected jitter [ms]'},
        'repair'        : { 'type': int,   'min': 0, 'max': 1440, 'precision': 1,     'desc': 'Repair time [min]'},             # max 1 day
        'guarantee'     : { 'type': float, 'min': 0, 'max': 1e2,  'precision': 1e-4,  'desc': 'SLA guarantee [% of time]'},
        'availability'  : { 'type': float, 'min': 0, 'max': 1e2,  'precision': 1e-4,  'desc': 'Link availability [% of time]'},
    }

    def __init__( self, randomize=False, bandwidth=100, latency=5, packet_loss=1e-2,
            jitter=2, repair=5, guarantee=1-5e-2, availability=1-1e-2 ):

        # eliminates "has no attribute" warning
        self.bandwidth = self.latency = self.packet_loss = self.jitter = \
        self.repair = self.guarantee = self.availability = self.encrypted = None

        # set all properties received in constructor
        props = locals()
        for k,v in props.items():

            # ignore if there is no property with the name
            if k not in self.PROPS:
                continue

            # pick random value in field range
            if randomize:

                if self.PROPS[k]["type"] == float:

                    # get number of digits from precision
                    rounding_digits = int( max( 0,
                        math.log(1 / self.PROPS[k]["precision"], 10))
                    )
                    value = random.uniform(
                        self.PROPS[k]["min"],
                        self.PROPS[k]["max"]
                    )
                    value = round(value, rounding_digits)

                elif self.PROPS[k]["type"] == int:
                    value = random.randint(self.PROPS[k]["min"],
                                          self.PROPS[k]["max"])

                setattr(self, k, value)

            # or pick from the props
            elif self.__isValidProp(k,v):
                setattr(self, k, v)

    # ===============
    # PRIVATE METHODS

    # Checks if a property is valid according to the expected type and range
    # Returns True if valid, throws an exception otherwise
    def __isValidProp(self, k, v, should_raise=True):
        """Checks if property is valid based on self.PROPS.

        Args:
            k:              Property key
            v:              Property value
            should_raise:   Flag that enables raise behavior
        Returns:
            True if valid.
            False if invalid AND should_raise is False
        Raises:
            (Only if should_raise is True)
            TypeError: if property type does not match self.PROPS
            ValueError: if property value is out of the range defined in self.PROPS
        """

        if k not in self.PROPS:
            return True
        if type(v) is not self.PROPS[k]['type']:
            msg = "Property {} must be a {}, not a {}.".format(k, self.PROPS[k]['type'], type(v))
            if should_raise:
                raise TypeError(msg)
            else:
                print(msg)
                return False

        norm_val = self.__normalizeProp(k, v)
        norm_min = int(self.PROPS[k]['min'] / self.PROPS[k]['precision'])
        norm_max = int(self.PROPS[k]['max'] / self.PROPS[k]['precision'])
        if norm_val < norm_min or norm_val > norm_max:
            raise ValueError("Property {} must be between {} and {}.".format(k, self.PROPS[k]['min'], self.PROPS[k]['max']))

        return True


    def __normalizeProp(self, k, v):
        """Maps a property to the integer spectrum before encryption.

        Float props are multiplied by their inverted precision.
        This maps the domain [min, max] to [min/precision, max/precision]
            allowing the casting of floats to integers with this precision

        Args:
            k: key of property to be normalized.
            v: value of property to be normalized.
        Returns:
            Normalized property as an integer.
        Raises:
            TypeError if casting to integer fails.
        """
        if type(v) is not float:
            try:
                return int(v)
            except:
                raise TypeError(
                    "Could not cast {} of type {} to integer".format( v, type(v) )
                )
        return int(v / self.PROPS[k]['precision'])

    # ==============
    # PUBLIC METHODS

    def print(self):
        """Prints the instance props to stdout for debugging purposes."""
        for k,v in self.PROPS.items():
            print("\t{}\t{}".format(self.__getattribute__(k), v['desc']))
        print("\n")


    def encrypt(self, encryption_key=None):
        """Encrypts props data using OPE (PyOPE)

        The property keys are not encrypted, only their values.
        The encryption algorithm used is the Order Preserving Encryption
        provided by PyOPE library. The ciphertexts reveals the order between
        plaintexts (a and b) encrypted with the same key (k), as in:

            a > b    iff    enc(a,k) > enc(b,k)

        This is useful to compare whether a measurement is within the
        SLA of the corresponding agreement.

        Args:
            encryption_key: used to encrypt the data.
        Returns:
            A tuple with:
                The encryption_key used.
                A dict with the encrypted properties.
        """
        if encryption_key is None:
            encryption_key = ope.OPE.generate_key()
        encrypted_sla = {}

        # for every property, normalize and encrypt the data
        for k,v in self.PROPS.items():

            norm_val = self.__normalizeProp(k, self.__getattribute__(k))
            norm_min = int(self.PROPS[k]['min'] / self.PROPS[k]['precision'])
            norm_max = int(self.PROPS[k]['max'] / self.PROPS[k]['precision'])

            cipher = ope.OPE(encryption_key,
                in_range=ope.ValueRange(norm_min, norm_max),
                out_range=ope.ValueRange(norm_min**2, norm_max**2)
            )

            encrypted_sla[k] = cipher.encrypt(int(norm_val))

        return encryption_key, encrypted_sla


    def extract(self):
        """Extracts a plaintext (readable) dict from this SLA instance.

        Sometimes it is useful to have a simple dict with the SLA properties.
        It works like a version of self.encrypt() without the encryption part.

        Returns
            A dict with the plaintext properties.
        """

        plaintext_sla = {}
        # for every property, create a dict entry
        for k, v in self.PROPS.items():
            plaintext_sla[k] = self.__getattribute__(k)

        return plaintext_sla
