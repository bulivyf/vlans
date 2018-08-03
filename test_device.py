from nose import tools

from constants import NOTSET
from hardware import Device
from message import RequestMsg, RequestType
from port import Port


class TestDevice:

    def setUp(self):
        # GIVEN
        device0 = Device(0, Port(), Port())

        for idx in range(5):
            device0.primary.assign(idx, NOTSET)
        for idx in range(4, 7):
            device0.secondary.assign(idx, NOTSET)

        device1 = Device(1, Port(), Port())
        for idx in range(5):
            device1.primary.assign(idx, NOTSET)
        for idx in range(3, 4):
            device1.secondary.assign(idx, NOTSET)

        self._devices = [device0, device1]

    def test_vlanid_allocation(self):
        # THEN
        tools.assert_true(self._devices[0].primary.size() == 5)
        tools.assert_true(self._devices[0].secondary.size() == 3)
        tools.assert_true(self._devices[1].primary.size() == 5)
        tools.assert_true(self._devices[1].secondary.size() == 1)

    def test_process_request(self):
        # WHEN
        msg = RequestMsg(RequestType.NON, 0)
        self._devices[0].process_request(msg)
        self._devices[1].process_request(msg)
        msg = RequestMsg(RequestType.RED, 1)
        self._devices[0].process_request(msg)
        self._devices[1].process_request(msg)

        # THEN
        tools.assert_true(self._devices[0].primary.vlan_ids[4].req_type.value == 1)
        tools.assert_true(self._devices[0].secondary.vlan_ids[4].req_type.value == 1)

    def test_process_request_that_exceeds_available_ids(self):
        # WHEN
        msg = RequestMsg(RequestType.NON, 0)
        self._devices[0].process_request(msg)
        self._devices[1].process_request(msg)
        msg = RequestMsg(RequestType.RED, 1)
        self._devices[0].process_request(msg)
        self._devices[1].process_request(msg)

        msg = RequestMsg(RequestType.RED, 2)
        self._devices[0].process_request(msg)
        self._devices[1].process_request(msg)
        # Test for no change...
        tools.assert_true(self._devices[0].primary.vlan_ids[4].req_type.value == 1)
        tools.assert_true(self._devices[0].secondary.vlan_ids[4].req_type.value == 1)
