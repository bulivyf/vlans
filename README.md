READ ME

Date: 7/27/18
Author: Evan Fraser


APPLICATION PURPOSE
This code is a solution to a preset programming problem.

The code is intended to assign requests to available vlan_ids across multiple devices.
The relationships of the objects are as follows:
* A Devices instance, holds a list of Device instances.
* A Device instance contains two ports. One primary port, and potentially a secondary port.
* Each port has a dictionary of vlan_ids.
* One vlan_id can hold a request id.


DESIGN NOTES
In most languages collections have been expanded with fairly extensive
alternatives. Each collection has its pro's and con's for a given problem.
For speed considerations add and lookup operations may inspire us to use a
hashmap collection for speed.  However, since we don't do any lookup
for existing collection elements such optimization isn't necessary.
Consequently, list and dict were the familiar and reasonable choices for this solution.

Note: for output we used namedtuple to allow percolation of results up to the calling method.
The namedtuple organization allowed extraction of the values into a numeric matrix.
From there, we use sort to organize the matrix according to the problem requirements.


DEVELOPER NOTES
Development of this code was through PyCharm Community Edition 2018.3.

Solution Modules
main_prcessor.py is the primary module in this work.  It contains all the following classes:
* RequestMsg is a more complex form of a what a VlanId can hold. VlanIds can simply hold a request id; which is the norms here.
* VlanIds is a list of requests (can be an request id or a RequestMsg)
* Port which is a child of a VlanIds instance.
* Device is an instance that holds two ports.
* Devices contains a list of Devices.
* Configuration performs the setup of the Devices, Device ports and Vlan Ids for the ports.
* FileOperators performs the work of loading data from the vlan_ids and requests files.

Main execution occurs from within the main_prcessor.py file.
Execution is controlled by argparse, which will inform you of expected arguments via the command line.

Note: API documentation exists under:

    docs/api/html/index.html

This was generated using doxygen (Doxyfile included).


DEVOPS NOTES
This code was developed using Python 3.6.  Your chosen interpreter libraries should include enum and argparse.

Deployment involves copying the code to the directory of your choice.
Basic execution will be as follows, via the command line:

    python main_prcessor.py

From there, follow the help guidance.

To turn on verbosity (output results to screen); add --verbose VERBOSE to the end of the command line.


TESTER NOTES
Unit tests are in place to test the public methods for most of the main_prcessor classes.

From the command line you can run these tests using the following:

    nosetests <test_filename>.py

Remember to substitute the actual test filename into the <test_filename> section.

For performance tests, test_performace.pt is written as a standalone main app.
It uses timeit to allow visual performance output on tne command line.


USER NOTES
This section not applicable.
No front end provided.
