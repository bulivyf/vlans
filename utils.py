"""

Utility classes

"""


class FileOperators:
    """
    The FileOperations class reads content in csv file.  That content is not expected to change in format.
    """
    @staticmethod
    def get_reqs_lst(reqs_filename):
        """
        Get the list of requests from the csv file.
        This data feeds the application with request for assignment to existing vlan_ids within a port.
        """
        reqs_lst = []
        with open(reqs_filename, "r") as ref_file:
            for line in ref_file.readlines():
                request_id, redundant = line.split(",")
                if request_id.isdigit():
                    # print(request_id, redundant)
                    reqs_lst.append((int(request_id), int(redundant)))
        return reqs_lst

    @staticmethod
    def get_vlans_lst(vlans_filename):
        """
        Get list of vlan_ids from csv file.
        This helps to configure the assignment of vlan_ids to a given primary or secondary port.
        """
        vlans_lst = []
        with open(vlans_filename, "r") as ref_file:
            for line in ref_file.readlines():
                device_id, primary_port, vlan_id = line.split(",")
                if device_id.isdigit():
                    # print(device_id, primary_port, vlan_id)
                    vlans_lst.append((int(device_id), int(primary_port), int(vlan_id)))
        return vlans_lst
