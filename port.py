"""
Classes that relate the the idea of a port which is part of a deviee.
"""
from constants import NOTFOUND


class VlanIds:
    """ VlanIds are part of the port designation.  All Port behaviors are here f, for now """

    def __init__(self):
        """ Constructor allows a finite number of vlan_id locations to be created. """
        self._vlan_ids = {}

    def assign(self, idx, msg):
        """ Assign a request msg to the vlan_id dict """
        self._vlan_ids[idx] = msg

    def remove(self, idx):
        """ Placeholder method.  Removes a msg from the vlan_ids; not part of the problem definition. """
        del self._vlan_ids[idx]

    def maximum(self):
        """ Get max available id"""
        val = next((key for key in self._vlan_ids.keys() if not self._vlan_ids[key]), NOTFOUND)
        # val = NOTFOUND
        # for key in self._vlan_ids.keys():
        #     if not self._vlan_ids[key]:
        #         val = key
        #         break
        return val

    def size(self):
        """ Get max number of ids """
        return len(self._vlan_ids)

    def has(self, idx):
        """ Check if vlan_ids has the given idx value. """
        return idx in self._vlan_ids

    def __str__(self):
        """ Get list of vlan id for this vlan_ids instance. """
        result = ""
        for stored_id in self._vlan_ids.keys():
            result += "{}|{} ".format(stored_id, repr(self._vlan_ids[stored_id]))
        return result

    def numeric_dict(self):
        """ Get list of vlan id for this vlan_ids instance, as numbers. """
        result = {}
        for vlan_id in self._vlan_ids.keys():
            if self._vlan_ids[vlan_id]:
                result[vlan_id] = self._vlan_ids[vlan_id]
        return result

    @property
    def vlan_ids(self):
        """ Get dict of ids in ascending order by vlan id number """
        return self._vlan_ids # {key: self._vlan_ids[key] for key in sorted(self._vlan_ids.keys())}


class Port(VlanIds):
    """
    A Port allows an (or any) application to listen for and respond to requests.
    For this problem, a Port only uses VLAN ids.

    The Port impl relies on behaviors in the parent class (VlanIDs), representing
    a 'Port isa VlanIds' relationship.
    Later behavioral changes in the Port instance may prompt refactoring
    (and a more inflated Port impl).

    Note: This class acts as a placeholder for readability wrt
    to correspondence with the problem description.
    Assumption: A Port instance can include other things other than VLAN ids.
    That is, we keep the name to allow for 1-to-1 correspondence with what the solution maps to.
    """
    pass
