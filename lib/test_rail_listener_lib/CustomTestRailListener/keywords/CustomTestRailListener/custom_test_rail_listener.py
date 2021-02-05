"""
Author: krishna@dgraph.io
"""
# pylint: disable=too-many-ancestors

__version__ = "1.0.0"
__all__ = ['CustomTestRailListener']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Staging"

from CustomTestRailListener.keywords.test_rail_keywords import TestRailsKeywords
import os


class CustomTestRailListener(TestRailsKeywords):
    """Robot Framework Custom Test Rails Listener Keyword Library.
    All the keywords pertaining to Networker are
    exposed to the user through this library.
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LISTENER_API_VERSION = 2

    ROBOT_CODE_ROOT_FOLDER_PATH = None
    ROBOT_CODE_BRANCH_FOLDER_PATH = None
    ROBOT_CODE_UTILS_FOLDER_PATH = None
    OS = None

    def __init__(self):
        """
        Framework init
        Initializes framework properties such as absolute code path
        """
        self.ROBOT_LIBRARY_LISTENER = self
        print('CustomTestRailListener Library')

    def about(self):
        """
        Custom Test Rail Listener Library consists of Keywords related to test rail result updating.
        """
        print("CustomTestRailListener Lib keywords: TestRailsKeywords")

    def _end_test(self, name, attrs):
        print("Test Case status is updating under test rail for: " + name)
        # Reading test rails details
        tr_details_path = os.path.join(os.getcwd(), "tr_details.txt")
        tr_listener_path = os.path.join(os.getcwd(), "tr_listener.txt")
        print("Test Case Status file location: " + tr_listener_path)
        tr_details = open(tr_details_path, "r")
        outfile = open(tr_listener_path, 'a')

        # Reading Test Rail configurations
        tr_config = {}
        for line in tr_details:
            key, value = line.split(": ")
            tr_config[key] = value.replace("\n", "")
        print(tr_config)

        # Reading tags for test case
        tags_list = []
        for tag in attrs['tags']:
            tag = tag.lower()
            if tag.startswith('c'):
                tags_list.append(tag.split('c')[1])
            if tag.startswith('v'):
                version = tag.split('v')[1]
        print(tags_list)
        test_rail_request = TestRailsKeywords()
        test_rail_request.test_rail_setup(url=tr_config["url"], user_name=tr_config["username"], password=tr_config["password"],
                                          project_name=tr_config["project_name"], run_name=tr_config["run_name"])

        # Updating Status for test case wrt tag
        for test_case in tags_list:
            if attrs['status'] == 'PASS':
                outfile.write('PASS: %s\n' % test_case)
                comment = "Test Case Passed as part of Automation Run."
                test_rail_request.test_rail_add_result_for_a_test_case_under_test_run(int(tr_config["run_id"]), test_case, status_id=1, comment=comment, version=version)
            else:
                outfile.write('FAIL: %s %s\n' % test_case % attrs['message'])
                comment = "Test Case Failed as part of Automation Run."
                self.test_rail_request.test_rail_add_result_for_a_test_case_under_test_run(int(tr_config["run_id"]), test_case, status_id=5, comment=comment, version=version)
