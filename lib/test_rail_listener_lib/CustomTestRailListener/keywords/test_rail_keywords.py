"""
Test Rails Request Lib
"""
from CustomTestRailListener.components.test_rail_request import TestRailsRequest
from robot.api import logger
import os

# pylint: disable=C0301

__all__ = ['TestRailsKeywords']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Staging"


class TestRailsKeywords:
    """
    Test Rails request keywords
    """

    def __init__(self):
        self.test_rail_request = TestRailsRequest

    def test_rail_setup(self, url, user_name, password, project_name, run_name):
        """
        Method to configure test rails with requested project before execution.
        \n:param url:<test_rail_url>
        \n:param user_name:<username>@mail.com
        \n:param password: <password>
        \n:return: none

         Example:
        | Test rails setup | url | user_name | password
        | Test rails setup | https://dgraph.testrail.io/ | user@mail.com | password
        """
        self.test_rail_request = TestRailsRequest(url, user_name, password)
        self.project_id = self.test_rail_request.get_project_id(project_name)
        self.run_id = self.test_rail_request.get_run_id_by_name(self.project_id, run_name=run_name)
        outpath = os.path.join(os.getcwd(), "tr_details.txt")
        print("Listener file location: " + outpath)
        outfile = open(outpath, 'w')
        outfile.write("url: %s\n" % url)
        outfile.write("username: %s\n" % user_name)
        outfile.write("password: %s\n" % password)
        outfile.write("run_name: %s\n" % run_name)
        outfile.write("run_id: %s\n" % self.run_id)
        outfile.write("project_name: %s\n" % project_name)
        outfile.write("project_id: %s\n" % self.project_id)
        logger.debug("Initialized Test Rails for " + url)

    def test_rail_get_all_tests(self, run_id):
        """
        Method to get all the tests created as part of run_id
        \n:param run_id: 7
        \n:return: <response>

         Example:
        | Get all tests | 7
        """
        all_tests = self.test_rail_request.get_all_test(run_id)
        logger.debug(all_tests)
        return all_tests

    def test_rail_get_test(self, test_id):
        """
        Method to get particular test from test rails.
        \n:param test_id: <test_case>
        \n:return: <response>

         Example:
        | Get Test | 582
        """
        tests = self.test_rail_request.get_test(test_id)
        logger.debug(tests)
        return tests

    def test_rail_get_all_projects(self):
        """
        Method to get all the projects
        :return:<all_projects_response>

        Example:
        | test rails get all projects |
        """

        projects = self.test_rail_request.get_all_projects()
        logger.debug(projects)
        return projects

    def test_rail_get_all_suites(self, project_id: int):
        """
        \nMethod to get all the suite id's based on the project id
        \n:param project_id:
        \n:return:<response>

        Example:
        | test rails get all suites | project_id
        | test rails get all suites | 190
        """
        response = self.test_rail_request.get_all_suites(project_id)
        return response

    def test_rail_get_suite_id(self, project_id, suite_name):
        """
        \nMethod to get suite id based on project id and suite name
        \n:param project_id: <project_id>
        \n:param suite_name: <suite_name>
        \n:return:<suite_id>

        Example:
        | test rails get suite id | project_id | suite_name
        | test rails get suite id | 4 | Test Suite

        """
        suite_id = self.test_rail_request.get_suite_id(project_id, suite_name)
        logger.info("Suite id: " + str(suite_id) + " suite: "
                    + suite_name + " for project_id: " + str(project_id))
        return suite_id

    def test_rail_get_project_id(self, project_name):
        """
        \nMethod to get project id based on project name
        \n:param project_name:
        \n:return:

         Example:
        | test rails get project id | project_name
        | test rails get project id | Dgraph
        | test rails get project id | Slash
        """
        proj_id = self.test_rail_request.get_project_id(project_name)
        logger.info("Project id for project:" + project_name + " is: " + str(proj_id))
        return proj_id

    def test_rail_get_section_id(self, project_id, section_name, **kwargs):
        """
        \nMethod to get section id based on section name
        \n:param project_id: id of the project
        \n:param section_name: name of the section under test suite
        \n:param kwargs:
        \n    :key suite_id:
        \n        The ID of the test suite (optional if the project is operating in
        \n        single suite mode)
        \n:return:<response>

         Example:
        | test rails get section id | project_id | section_name | suite_id
        | test rails get section id | Dgraph | Automation Section | suite_id=190
        | test rails get section id | Slash | API Section | suite_id=150
        """
        section_id = self.test_rail_request.get_section_id_by_section_name(project_id, section_name, **kwargs)
        return section_id

    def test_rail_get_run_id_by_name(self, project_id, run_name, **kwargs):
        """
        \n                Returns a list of test runs for a project. Only returns those test runs that
        \n                are not part of a test plan (please see get_plans/get_plan for this).
        \n
        \n                :param project_id: The ID of the project
        \n                :param run_name: Name of the run
        \n                :param kwargs: filters
        \n                    :key created_after: int/datetime
        \n                        Only return test runs created after this date (as UNIX timestamp).
        \n                   :key created_before: int/datetime
        \n                        Only return test runs created before this date (as UNIX timestamp).
        \n                    :key created_by: List[int] or comma-separated string
        \n                        A comma-separated list of creators (user IDs) to filter by.
        \n                    :key is_completed: int/bool
        \n                        1/True to return completed test runs only.
        \n                        0/False to return active test runs only.
        \n                    :key limit/offset: int
        \n                        Limit the result to :limit test runs. Use :offset to skip records.
        \n                    :key milestone_id: List[int] or comma-separated string
        \n                        A comma-separated list of milestone IDs to filter by.
        \n                    :key refs_filter: str
        \n                        A single Reference ID (e.g. TR-a, 4291, etc.)
        \n                    :key suite_id: List[int] or comma-separated string
        \n                        A comma-separated list of test suite IDs to filter by.
        \n                :return: response

         Example:
        | test rails get run id by name | project_id | run_name | **kwargs
        | test rails get run id by name | 4 | Automation Run | created_after= 123149124
        | test rails get run id by name | 4 | Automation Run | created_by= [2, 3, 4]
        | test rails get run id by name | 4 | Automation Run | is_completed= True
        | test rails get run id by name | 4 | Automation Run | suite_id= 190,123
        | test rails get run id by name | 4 | Automation Run | suite_id= [190, 123]

                        """
        run_id = self.test_rail_request.get_run_id_by_name(project_id, run_name, **kwargs)
        return run_id

    def test_rail_add_result_for_a_test_case_under_test_run(self, run_id, case_id, **kwargs):
        """
                        Adds a new test result, comment or assigns a test (for a test run and case
                        combination). It's recommended to use add_results_for_cases instead if you
                        plan to add results for multiple test cases.

        \n                The difference to add_result is that this method expects a test run +
                        test case instead of a test. In TestRail, tests are part of a test run and
                        the test cases are part of the related test suite.
                        So, when you create a new test run, TestRail creates a test for each test case
                        found in the test suite of the run.
                        You can therefore think of a test as an “instance” of a test case which can
                        have test results, comments and a test status.
                        Please also see TestRail's getting started guide for more details about the
                        differences between test cases and tests.

        \n                :param run_id:
                            The ID of the test run
        \n                :param case_id:
                            The ID of the test case under test suite
        \n                :param kwargs:
        \n                    :key status_id: int
        \n                        The ID of the test status. The built-in system
                                statuses have the following IDs:
        \n                            1 - Passed
        \n                            2 - Blocked
        \n                            3 - Untested (not allowed when adding a result)
        \n                            4 - Retest
        \n                            5 - Failed
        \n                        You can get a full list of system and custom statuses via get_statuses.
        \n                    :key comment: str
                                The comment / description for the test result
        \n                    :key version: str
                                The version or build you tested against
        \n                    :key elapsed: str
                                The time it took to execute the test, e.g. "30s" or "1m 45s"
        \n                    :key defects: str
                                A comma-separated list of defects to link to the test result
        \n                    :key assignedto_id: int
                                The ID of a user the test should be assigned to

        \n                   Custom fields are supported as well and must be submitted with their
                            system name, prefixed with ‘custom_’, e.g.:
        \n                        {
        \n                            ...
        \n                            "custom_comment": "This is a custom comment"
        \n                            ...
        \n                        }
        \n                :return: response

         Example:
        | test rails add result for test case test run | run_id | case_id |  **kwargs
        | test rails add result for test case test run | 34 | 1233 | status_id= 2 | comment= Result Comment
        | test rails add result for test case test run | 56 | 2332 | status_id= 5 | comment= Result Comment
                        """
        response = self.test_rail_request.add_results_for_a_case(run_id, case_id, **kwargs)
        return response
