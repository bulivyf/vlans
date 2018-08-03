from nose import tools

from constants import NOTSET
from hardware import Devices, Device
from message import RequestMsg, RequestType
from port import Port


class TestDevices:

    def setUp(self):
        # GIVEN
        self._devices = Devices()

        for dev_id in range(5):
            device=Device(dev_id, Port(), Port())
            for idx in range(5):
                device.primary.assign(idx, NOTSET)
                device.secondary.assign(idx, NOTSET)
            self._devices.all.append(device)

    def test_process_request_on_lowest_vlan_id_for_nonred_msgs(self):
        for idx in range(10):
            # WHEN
            msg = RequestMsg(RequestType.NON, 0)
            device_id = self._devices.process_request(msg)
            # THEN
            tools.assert_equal(device_id, idx % 5)

    def test_process_request_on_lowest_vlan_id_for_red_msgs(self):
        for idx in range(10):
            msg = RequestMsg(RequestType.RED, 0)
            # WHEN
            device_id = self._devices.process_request(msg)
            # THEN
            tools.assert_equal(device_id, idx % 5)
