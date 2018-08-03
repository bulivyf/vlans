"""

Classes that represent the physical ideal of a Device and a collection of same.

"""
from collections import namedtuple

from constants import NOTFOUND, NOTSET
from message import RequestMsg, RequestType
from port import Port


class Device:
    """ A Device has a max of two ports: primary and possibly secondary. """

    def __init__(self, idx, primary_port: Port = None, secondary_port: Port = None):
        """ Constructor allows the definition of a device as a primary and seconfdary port """
        self._id = idx
        self._primary_port = primary_port
        self._secondary_port = secondary_port

    def process_request(self, msg: RequestMsg):
        """
        Process a request-to-reserve msg.
        This results in the placement of a request in a vlan_id
        list for a device with lowest vlan_id available.
        """
        avail_id = self.get_best_vlan_id(msg)
        if avail_id != NOTFOUND:
            self._primary_port.assign(avail_id, msg)
            if msg.req_type == RequestType.RED:
                self._secondary_port.assign(avail_id, msg)
        return avail_id

    def get_best_vlan_id(self, msg: RequestMsg):
        """
        Get the max used vlan_id from primary (possibly secondary)
        ports on this device instance
        """
        if msg.req_type == RequestType.NON:
            max_val = self._primary_port.maximum()
        else:
            max_val = self._find_max_id_for_redundancy_msg()
        return max_val

    def _find_max_id_for_redundancy_msg(self):
        """
        If there is a secondary port, find if there is an avail id for both prim and sec ports.
        If there isn't, report that we cant use this device; with a NOTFOUND setting.
        """
        if self._secondary_port:
            max_val = self._process_for_secondary_ids()
        else:
            max_val = NOTFOUND
        return max_val

    def _process_for_secondary_ids(self):
        """ Get max primary port vlan_id, then do a search from there to find an equivalent sec port vlan id """
        max_prim_val = self._primary_port.maximum()
        if max_prim_val != NOTFOUND:
            if max_prim_val != self._secondary_port.maximum():
                max_val = self._find_equivalent_ids_from_id(max_prim_val)
            else:
                max_val = max_prim_val
        else:
            max_val = NOTFOUND
        return max_val

    def _find_equivalent_ids_from_id(self, max_prim_val):
        """
        Find equivalent vlanids that are valid on both the prim and secondary port
        Here we search in the available range of vlanids for a prim==sec port id value.
        If we exceed the prim port vlandid range, we receive an IDXEXCEEDED flag,
        but then flag the return as NOTFOUND.
        NOTFOUND means we couldn't find a valid prim/sec correlation.
        """
        search_id = NOTFOUND
        primary_ids = list(self._primary_port.vlan_ids.keys())
        secondary_ids = list(self._secondary_port.vlan_ids.keys())

        shared_ids = sorted(list(set(primary_ids) & set(secondary_ids)))

        for idx in shared_ids:
            if self._primary_port.vlan_ids[idx] == NOTSET:
                search_id = idx

        return search_id

    def __str__(self):
        """ Return a string of port information for this Device (i.e. the vlan_ids that relate to each port) """
        result = r"Dev:{} ".format(self._id) + '\n'
        result += r"Pri: {} ".format(self._primary_port.__str__()) + '\n'
        if self._secondary_port:
            result += r"Sec: {} ".format(self._secondary_port.__str__())
        return result

    def list_numeric(self):
        """ Create the results as a namedtuple of device, port, vlan and rea.
        This ordering perceived as the order in which a dev would look at the data. """
        results = []
        DeviceRef = namedtuple("DeviceRef", "device port vlan req")

        self._build_primary_port_nametuples_list(DeviceRef, results)

        self._build_secondary_port_namedtuples_list(DeviceRef, results)

        return results

    def _build_secondary_port_namedtuples_list(self, DeviceRef, results):
        """ Build the name tuples list from the secondary port data available """
        if self._secondary_port:
            for vlan_id_key in self._secondary_port.vlan_ids.keys():
                if self._secondary_port.vlan_ids[vlan_id_key]:
                    results.append(DeviceRef(
                        device=self._id,
                        port=0,
                        vlan=vlan_id_key,
                        req=self._secondary_port.vlan_ids[vlan_id_key]))

    def _build_primary_port_nametuples_list(self, DeviceRef, results):
        """ Build the name tuples list from the primary port data available """
        for vlan_id_key in self._primary_port.vlan_ids.keys():
            if self._primary_port.vlan_ids[vlan_id_key]:
                results.append(DeviceRef(
                    device=self._id,
                    port=1,
                    vlan=vlan_id_key,
                    req=self._primary_port.vlan_ids[vlan_id_key]))

    @property
    def primary(self):
        """ primary port instnce for this device """
        return self._primary_port

    @primary.setter
    def primary(self, ref_port):
        """ primary port instance for this device """
        self._primary_port = ref_port

    @property
    def secondary(self):
        """ secondary port instance for this device """
        return self._secondary_port

    @secondary.setter
    def secondary(self, ref_port):
        """ secondary port instance for this device """
        self._secondary_port = ref_port

    @property
    def id_val(self):
        """ id for this device """
        return self._id


class Devices:
    """ Collection holder and operator for all instantiated Devices """

    def __init__(self):
        """ Constructor inits Devices list that we'll be working with. """
        self._devices = []

    def process_request(self, msg: RequestMsg):
        """
        With a given msg, process it to be placed on a device with the min vlan_id
        (by finding min idx over all devices).
        """
        device_id = self._get_max_min_vlan_id(msg)
        self._devices[device_id].process_request(msg)
        return device_id

    def _get_max_min_vlan_id(self, msg):
        """
        Given the message request-type,
        find the device with the minimum vlan_id (i.e. min id across all devices).
        """
        device_maxs = [device.get_best_vlan_id(msg) for device in self._devices]
        device_min_id = min(device_maxs)
        return device_maxs.index(device_min_id)

    def add(self, device: Device):
        self.all.append(device)

    def list_numeric(self):
        results = []
        for device in self._devices:
            results.append(device.list_numeric())
        return results

    def __str__(self):
        """ List Information on all defined devices """
        result = ""
        for ref_device in self._devices:
            result += ref_device.__str__() + '\n'
        return result

    @property
    def all(self):
        """ Return all setup devices """
        return self._devices

    @all.setter
    def all(self, ref_devices):
        """ Set the devices this collection will process """
        self._devices = ref_devices
