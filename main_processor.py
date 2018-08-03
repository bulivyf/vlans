"""

MAIN Module

VLAN_ID assignment solution;
Almost a load-balancer for port allocation (and eventual request processing; not impl).

"""
import argparse
from pprint import pprint

from configuration import Configurator
from hardware import Devices
from message import RequestMsg, RequestType
from utils import FileOperators


def main(vlans_filename, reqs_filename, output_filename, verbosity):
    """ Main execution point for this application. """

    # SETUP
    devices = Devices()
    devices.all = Configurator().setup_devices(vlans_filename, verbosity)

    # INPUT
    reqs_lst = FileOperators.get_reqs_lst(reqs_filename)

    # PROCESS
    _process(devices, reqs_lst)
    if verbosity:
        print(devices.__str__())

    # OUTPUT
    _create_formatted_output(devices, output_filename, verbosity)


def _create_formatted_output(devices, output_filename, verbosity):
    """
        sort your output.csv
        first ascending by request_id and
        then ascending by primary_port
    """
    with open(output_filename, "w") as out_file:

        out_file.write("request_id,device_id,primary_port,vlan_id\n")

        matrix = _setup_data(devices)
        matrix = _post_process_data(matrix, verbosity)

        for r in range(len(matrix)):
            ref_str = "{},{},{},{}\n".format(matrix[r][0], matrix[r][1], matrix[r][2], matrix[r][3])
            out_file.write(ref_str)


def _post_process_data(matrix, verbosity):
    if verbosity:
        print("Matrix Output (consecutive rows are): requests, devices, ports, vlan_ids")
        pprint(matrix)
    matrix = _get_matrix_transpose(matrix)
    # Sort by 1st then 3rd col; i.e. requ_id, then prim_port
    matrix.sort(key=lambda x: (x[0], x[2]))
    if verbosity:
        print("Matrix Output (consecutive columns are): requests, devices, ports, vlan_ids " +
              "(sorted by reqs, then ports)")
        pprint(matrix)
    return matrix


def _setup_data(devices):
    reqs = []
    devs = []
    prts = []
    vlns = []
    for result in devices.list_numeric():
        for p in result:
            reqs.append(p.req.id_val)
            devs.append(p.device)
            prts.append(p.port)
            vlns.append(p.vlan)
    matrix = [reqs, devs, prts, vlns]
    return matrix


def _process(devices, reqs_lst):
    """ Process the request to reserve through the application steps. """
    for line in reqs_lst:
        request_id, redundant = line
        # print(request_id, redundant)
        msg = RequestMsg(RequestType(redundant), request_id)
        # device_id = \
        devices.process_request(msg)


def _get_matrix_transpose(m):
    """ create the transpose of the given matrix m """
    matrix = []
    for x in range(len(m[0])):
        row = []
        for y in range(4):
            row.append(m[y][x])
        matrix.append(row)
    return matrix


if __name__ == "__main__":
    """ For command line execution. """
    parser = argparse.ArgumentParser()
    parser.add_argument("vlanids", help="file location for vlan list")
    parser.add_argument("requests", help="file location for requests list")
    parser.add_argument("output", help="file location for output result")
    parser.add_argument("--verbose", help="increase output verbosity")
    args = parser.parse_args()

    main(args.vlanids, args.requests, args.output, args.verbose)
