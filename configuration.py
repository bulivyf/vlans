"""

Classes that help define the problem.

This problem is defined via the content of .csv files.

"""
from constants import NOTSET
from hardware import Device
from port import Port
from utils import FileOperators


class Configurator:
    """
    Configure the application with device, port and vlan ids
    based on entries from a csv file.
    """

    def setup_devices(self, vlans_file, verbose=False):
        """ Setup our devices, ports and related vlan ids per port """
        vlans_lst = FileOperators.get_vlans_lst(vlans_file)
        ref_dev_id = -1
        ref_prim_port = -1
        devices_lst = []
        for vlans_item in vlans_lst:
            dev_id, prim_port, vlan_id = vlans_item
            if verbose:
                print(dev_id, prim_port, vlan_id)
            if ref_dev_id != dev_id:
                ref_dev_id = dev_id
                devices_lst.append(Device(ref_dev_id))
                ref_prim_port = -1
            if ref_prim_port != prim_port:
                ref_prim_port = prim_port
                self._add_port(devices_lst, ref_dev_id, ref_prim_port)
            self._add_vlan_id(devices_lst, ref_dev_id, ref_prim_port, vlan_id)

            # print(dev_id, prim_port, vlan_id)
        return devices_lst

    @staticmethod
    def _add_vlan_id(devices_lst, ref_dev_id, ref_prim_port, vlan_id):
        """ Add a vlan ref to the relevant port """
        if ref_prim_port == 0:
            devices_lst[ref_dev_id].secondary.assign(vlan_id, NOTSET)
        if ref_prim_port == 1:
            devices_lst[ref_dev_id].primary.assign(vlan_id, NOTSET)

    @staticmethod
    def _add_port(devices_lst, ref_dev_id, ref_prim_port):
        """
        Add/create a port to the reference device.
        If config entry is:
            * 1 then its a primary port
            * 0 then its a secondary port
        """
        if ref_prim_port == 0 and not devices_lst[ref_dev_id].secondary:
            devices_lst[ref_dev_id].secondary = Port()
        if ref_prim_port == 1 and not devices_lst[ref_dev_id].primary:
            devices_lst[ref_dev_id].primary = Port()
