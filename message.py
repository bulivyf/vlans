"""

Classes that represent a message.
For this problem a message represents a request for allocation to a vlan_id on a port.

"""
from enum import Enum


class RequestType(Enum):
    """
    Types represent request-to-reserve for Vlan Id
    They are called Non Redundant and Redundant.

    Non-Redundant means request that do not need to be stored in both prim and sec; just prim.
    Redundancy means the message must be stored in both a prim and sec vlaid both with the same id number on the device.

    Used in RequestMsg to indicate its type.
    """
    NON = 0
    RED = 1


class RequestMsg:
    """ This is the request that will be set as a VlanId item. """

    def __init__(self, ref_type: RequestType, idx: int = 0, data: str = ""):
        self._id = idx
        self._type = ref_type
        self._data = data

    @property
    def id_val(self):
        """ Get id of this request message """
        return self._id

    @property
    def req_type(self):
        """ Get the type for this request message """
        return self._type

    @property
    def data(self):
        """ Get any data related to the request msg """
        return self._data

    def __repr__(self):
        return r"{}:{} ".format(str(self._id), self._type.name)  # , self._data)
