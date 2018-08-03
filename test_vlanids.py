"""
Test public (API) methods for class VlanIds
"""
from nose import tools

from constants import NOTFOUND
from message import RequestMsg, RequestType
from port import VlanIds


class TestVlanIds:

    def test_assign(self):
        # GIVEN
        vlanids = VlanIds()
        msg = RequestMsg(RequestType.NON)

        # WHEN/THEN
        vlanids.assign(0, msg)
        tools.assert_equal(vlanids.size(), 1)
        vlanids.assign(1, RequestType.NON)
        tools.assert_equal(vlanids.size(), 2)

    def test_remove(self):
        # GIVEN
        vlanids = VlanIds()
        msg = RequestMsg(RequestType.NON)

        # WHEN/THEN
        vlanids.assign(0, msg)
        tools.assert_equal(vlanids.size(), 1)
        vlanids.remove(0)
        tools.assert_equal(vlanids.size(), 0)

    def test_maximum(self):
        # GIVEN
        vlanids = VlanIds()
        # WHEN
        for i in range(5):
            msg = RequestMsg(RequestType.NON)
            vlanids.assign(i, msg)
        ref_max = vlanids.maximum()
        # THEN
        tools.assert_equal(ref_max, NOTFOUND)  # No available vlan ids found.
        tools.assert_equal(vlanids.size(), 5)

    def test_has(self):
        # GIVEN
        vlanids = VlanIds()
        msg = RequestMsg(RequestType.NON)

        # WHEN/THEN
        vlanids.assign(1, msg)
        tools.assert_true(vlanids.has(1))
        tools.assert_false(vlanids.has(0))
        tools.assert_false(vlanids.has(-1))
