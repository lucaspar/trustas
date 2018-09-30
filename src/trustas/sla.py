# Data structure for Service Level Agreements
# Can describe an SLA agreed (ideal) or a set of measured properties (real)
import math
import random

from pyope import ope

class SLA:

    # Known properties of the SLA.
    # Only these will be encrypted and passed to the blockchain.
    PROPS = {
        'bandwidth'     : { 'type': int,   'min': 1, 'max': 1e9,       'precision': 1,     'desc': 'Available bandwidth [Mbps]'},
        'latency'       : { 'type': int,   'min': 0, 'max': 1e3,       'precision': 1,     'desc': 'Expected latency [ms]'},
        'packet_loss'   : { 'type': float, 'min': 0, 'max': 1e2,       'precision': 1e-8,  'desc': 'Expected packet loss [%]'},
        'jitter'        : { 'type': int,   'min': 0, 'max': 1e3,       'precision': 1,     'desc': 'Expected jitter [ms]'},
        'repair'        : { 'type': int,   'min': 0, 'max': 2**16-1,   'precision': 1,     'desc': 'Repair time [min]'},
        'guarantee'     : { 'type': float, 'min': 0, 'max': 1e2,       'precision': 1e-8,  'desc': 'SLA guarantee [% of time]'},
        'availability'  : { 'type': float, 'min': 0, 'max': 1e2,       'precision': 1e-8,  'desc': 'Link availability [% of time]'},
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

    # Normalizes a property before encryption
    #   Float props are multiplied by their inverted precision.
    #   This maps the domain [min, max] to [min/precision, max/precision]
    #   allowing the casting of floats to integers with this precision
    def __normalizeProp(self, k, v):
        if type(v) is not float:
            try:
                return int(v)
            except:
                print("ERROR: Could not cast {} of type {} to integer".format(v, type(v)))
        return int(v / self.PROPS[k]['precision'])

    # ==============
    # PUBLIC METHODS

    # Print instance for debugging purposes
    def print(self):
        for k,v in self.PROPS.items():
            print("\t{}\t{}".format(self.__getattribute__(k), v['desc']))
        print("\n")


    # Encrypts props data using OPE (pyope)
    def encrypt(self, encryption_key=None):

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
