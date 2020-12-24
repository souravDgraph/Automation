from Dgraph.components.testrails_request import TestRailsRequest
from robot.api import logger

__all__ = ['TestRailsKeywords']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "tkrishnakaushik96@gmail.com"
__status__ = "Stagging"


class TestRailsKeywords:

    def test_rails_setup(self, url, user_name, password):
        """
        Method to configure test rails with requested project before execution.
        \n:param url:<test_rails_url>
        \n:param user_name:<username>@mail.com
        \n:param password: <password>
        \n:return: none

         Example:
        | Test rails setup | url | user_name | password
        | Test rails setup | https://dgraph.testrail.io/ | user@mail.com | password
        """
        self.test_rails_request = TestRailsRequest(url, user_name, password)
        logger.debug("Initialized Test Rails for " + url)

    def test_rails_get_all_tests(self, run_id):
        """
        Method to get all the tests created as part of run_id
        \n:param run_id: 7
        \n:return: <response>

         Example:
        | Get all tests | 7
        """
        all_tests = self.test_rails_request.get_all_test(run_id)
        logger.debug(all_tests)
        return all_tests

    def test_rails_get_test(self, test_id):
        """
        Method to get particular test from test rails.
        \n:param test_id: <test_case>
        \n:return: <response>

         Example:
        | Get Test | 582
        """
        tests = self.test_rails_request.get_test(test_id)
        logger.debug(tests)
        return tests
