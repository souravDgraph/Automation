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
__status__ = "Stagging"

from CustomTestRailListener.keywords.test_rail_keywords import TestRailsKeywords
import os


class CustomTestRailListener(TestRailsKeywords):
    """Robot Framework Slash GraphQL Keyword Library.
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
        print('Common Library')

    def about(self):
        """
        Common Library consists of Keywords related to both Slash and Dgraph
        """
        print("Common Lib keywords: TestRailsKeywords, PydgraphKeywords")

    def _end_test(self, name, attrs):
        test_rail_request = TestRailsKeywords()
        tr_listener_outpath = os.path.join(os.getcwd(), "tr_listener.txt")
        tr_details_path = os.path.join(os.getcwd(), "tr_details.txt")
        print("Listener file location: " + tr_listener_outpath)
        tr_details = open(tr_details_path, "r")
        outfile = open(tr_listener_outpath, 'a')
        print("Test Case status is updating under test rail for: " + name)
        tr_config = {}
        for line in tr_details:
            key, value = line.split(": ")
            tr_config[key] = value.replace("\n", "")
        print(tr_config)

        ta = []
        for tag in attrs['tags']:
            tag = tag.lower()
            if tag.startswith('c'):
                ta.append(tag.split('c')[1])
        print(ta)
        test_rail_request.test_rail_setup(url=tr_config["url"], user_name=tr_config["username"], password=tr_config["password"],
                                          project_name=tr_config["project_name"], run_name=tr_config["run_name"])
        for test_case in ta:
            if attrs['status'] == 'PASS':
                outfile.write('PASS: %s\n' % test_case)
                comment = "Test Case Passed as part of Automation Run."
                test_rail_request.test_rail_add_result_for_a_test_case_under_test_run(int(tr_config["run_id"]), test_case, status_id=1, comment=comment, version="20.11")
            else:
                outfile.write('FAIL: %s %s\n' % test_case % attrs['message'])
                comment = "Test Case Failed as part of Automation Run."
                self.test_rail_request.test_rail_add_result_for_a_test_case_under_test_run(int(tr_config["run_id"]), test_case, status_id=5, comment=comment, version="20.11")
