"""
Rudimentary unit tests for performance measuring.

PyCharm, datadoghq.com etc can give further perspectives on performance.
"""
import timeit
from main_processor import main as runner


def run_main():
    runner("data/test_vlans.csv", "data/test_requests.csv", "out.csv", False)


def test_1000_runs():
    result = timeit.timeit(run_main, number=1000)
    print(result)


if __name__ == "__main__":
    """ For command line execution. """
    test_1000_runs()
