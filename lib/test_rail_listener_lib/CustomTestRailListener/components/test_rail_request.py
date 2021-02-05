"""
 Test Rails lib implementation
"""
from typing import List

from robot.api import logger
from testrail_api import TestRailAPI

# pylint: disable=C0301

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
        self.run_id = 0

    def get_all_test(self, run_id):
        """
        Method implementation to fetch all the test for a run
        :param run_id:
        :return: <response>
        """
        self.run_id = run_id
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

    def get_all_projects(self):
        """
        Method to get all the projects
        :return:
        """
        projects = self.api.projects.get_projects()
        return projects

    def get_project_id(self, project_name):
        """
        Method to get project id based on project name.
        :param project_name:
        :return:<project_id>
        """
        list_projects = self.get_all_projects()
        proj_id = None
        for data in list_projects:
            if data['name'] == project_name:
                proj_id = data['id']
        logger.debug(proj_id)
        if proj_id is None:
            raise Exception("Project not found" + project_name)
        return proj_id


    def get_suite_id(self, project_id, suite_name):
        """
        Method to get suite id based on suite name
        :param project_id:
        :param suite_name:
        :return:
        """
        suites_list = self.get_all_suites(project_id)
        suite_id = None
        for data in suites_list:
            if data['name'] == suite_name:
                suite_id = data['id']
        logger.debug(suite_id)
        if suite_id is None:
            raise Exception("Suite not found: " + suite_name + "for project_id: " + project_id)
        return suite_id

    def get_all_suites(self, project_id: int):
        """
        Method to get all suites for the specified project
        \n:param project_id:
            project id
        \n:return:<response>
        """
        response = self.api.suites.get_suites(project_id=project_id)
        return response


    def get_all_section_id(self, project_id, **kwargs):
        """
        Returns a list of sections for a project and test suite.

        :param project_id:
            The ID of the project
        :param kwargs:
            :key suite_id:
                The ID of the test suite (optional if the project is operating in
                single suite mode)
        :return: response
        """
        return self.api.sections.get_sections(project_id, **kwargs)

    def get_section_id_by_section_name(self, project_id, section_name, **kwargs):
        """
        Method to get section id by section name
        :param project_id:
        :param section_name:
        :param kwargs:
            :key suite_id:
                The ID of the test suite (optional if the project is operating in
                single suite mode)
        :return: section_id
        """
        sections = self.get_all_section_id(project_id, **kwargs)
        for section_details in sections:
            if section_details['name'] == section_name:
                section_id = section_details['id']
        logger.debug(sections)
        logger.info(section_id)
        return section_id

    def update_results(self, run_id, results: list):
        """
                This method expects an array of test results (via the 'results' field,
                please see below). Each test result must specify the test ID and can pass in
                the same fields as add_result, namely all test related system and custom fields.

                Please note that all referenced tests must belong to the same test run.

                :param run_id:
                    The ID of the test run the results should be added to
                :param results: List[dict]
                    This method expects an array of test results (via the 'results' field,
                    please see below).
                    Each test result must specify the test ID and can pass in the same fields
                    as add_result, namely all test related system and custom fields.

                    Please note that all referenced tests must belong to the same test run.
                :return: response
                """
        response = self.api.results.add_results(run_id, results)
        return response

    def add_results_for_a_case(self, run_id, case_id, **kwargs):
        """
                Adds a new test result, comment or assigns a test (for a test run and case
                combination). It's recommended to use add_results_for_cases instead if you
                plan to add results for multiple test cases.

                The difference to add_result is that this method expects a test run +
                test case instead of a test. In TestRail, tests are part of a test run and
                the test cases are part of the related test suite.
                So, when you create a new test run, TestRail creates a test for each test case
                found in the test suite of the run.
                You can therefore think of a test as an “instance” of a test case which can
                have test results, comments and a test status.
                Please also see TestRail's getting started guide for more details about the
                differences between test cases and tests.

                :param run_id:
                    The ID of test run
                :param case_id:
                    The ID of the test case under test suite
                :param kwargs:
                    :key status_id: int
                        The ID of the test status. The built-in system
                        statuses have the following IDs:
                            1 - Passed
                            2 - Blocked
                            3 - Untested (not allowed when adding a result)
                            4 - Retest
                            5 - Failed
                        You can get a full list of system and custom statuses via get_statuses.
                    :key comment: str
                        The comment / description for the test result
                    :key version: str
                        The version or build you tested against
                    :key elapsed: str
                        The time it took to execute the test, e.g. "30s" or "1m 45s"
                    :key defects: str
                        A comma-separated list of defects to link to the test result
                    :key assignedto_id: int
                        The ID of a user the test should be assigned to

                    Custom fields are supported as well and must be submitted with their
                    system name, prefixed with ‘custom_’, e.g.:
                        {
                            ...
                            "custom_comment": "This is a custom comment"
                            ...
                        }
                :return: response
                """
        response = self.api.results.add_result_for_case(run_id, case_id, **kwargs)
        return response

    def add_results_for_multiple_test_cases(self, run_id: int, results: List[dict]):
        """
                Adds one or more new test results, comments or assigns one or more tests
                (using the case IDs).
                Ideal for test automation to bulk-add multiple test results in one step.

                Requires TestRail 3.1 or later

                :param run_id:
                    The ID of the test run the results should be added to
                :param results: List[dict]
                    This method expects an array of test results (via the 'results' field,
                    please see below). Each test result must specify the test case ID and
                    can pass in the same fields as add_result, namely all test related
                    system and custom fields.

                    The difference to add_results is that this method expects test case IDs
                    instead of test IDs. Please see add_result_for_case for details.

                    Please note that all referenced tests must belong to the same test run.
                :return: response
                """
        self.api.results.add_results_for_cases(run_id, results)

    def get_run_id_by_name(self, project_id, run_name, **kwargs):
        """
                Returns a list of test runs for a project. Only returns those test runs that
                are not part of a test plan (please see get_plans/get_plan for this).

                :param project_id: The ID of the project
                :param run_name: Name of the run
                :param kwargs: filters
                    :key created_after: int/datetime
                        Only return test runs created after this date (as UNIX timestamp).
                    :key created_before: int/datetime
                        Only return test runs created before this date (as UNIX timestamp).
                    :key created_by: List[int] or comma-separated string
                        A comma-separated list of creators (user IDs) to filter by.
                    :key is_completed: int/bool
                        1/True to return completed test runs only.
                        0/False to return active test runs only.
                    :key limit/offset: int
                        Limit the result to :limit test runs. Use :offset to skip records.
                    :key milestone_id: List[int] or comma-separated string
                        A comma-separated list of milestone IDs to filter by.
                    :key refs_filter: str
                        A single Reference ID (e.g. TR-a, 4291, etc.)
                    :key suite_id: List[int] or comma-separated string
                        A comma-separated list of test suite IDs to filter by.
                :return: response
                """
        all_runs = self.api.runs.get_runs(project_id, **kwargs)
        logger.debug(all_runs)
        run_id = None
        for run_details in all_runs:
            if run_details['name'] == run_name:
                run_id = run_details['id']
        if run_id is None:
            raise Exception("Run id was not found for run name: " + run_name)
        return run_id

