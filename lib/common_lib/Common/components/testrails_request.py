"""
 Test Rails lib implementation
"""
from testrail_api import TestRailAPI

__all__ = ['TestRailsRequest']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Staging"


class TestRailsRequest:
    """
    Test Rails request handler class.
    """

    def __init__(self, url, user_name, password):
        """
        Method to initialize test rails api.
        :param url:
        :param user_name:
        :param password:
        """
        self.api = TestRailAPI(url, user_name, password)

    def get_all_test(self, run_id):
        """
        Method implementation to fetch all the test for a run
        :param run_id:
        :return: <response>
        """
        tests = self.api.tests
        return tests.get_tests(run_id)

    def get_test(self, test_id):
        """
        Method implementation for fetching particular test case details.
        :param test_id:
        :return: <response>
        """
        tests = self.api.tests
        return tests.get_test(test_id)
