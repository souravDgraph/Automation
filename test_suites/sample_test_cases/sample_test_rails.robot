*** Settings ***
Library           CustomTestRailListener
Suite Setup     test rail Setup    https://dgraph.testrail.io    email_id    password     Dgraph    Automation_Test_Run

*** Variables ***
${version}      V20.11.2

*** Test Cases ***

Update Check for test rail
    [Documentation]      Test case to add test run and update results
    [Tags]  C1496   ${version}
    ${proj_id}=     test rail get project id       Dgraph
    ${suite_id}=    test rail get suite id     ${proj_id}      Automation_Suite
    ${case_ids}      Create List     1496
    test rail add test run     ${proj_id}      suite_id=${suite_id}      name=Automation_Test_Run       description="Robot famrework check"     case_ids=${case_ids}
    ${run_id}=      test rail get run id by name   ${proj_id}      Automation_Test_Run     created_after=1609499627
    test rail add result for test case test run    ${run_id}   1496    status_id=2     version=20.11   comment=Updating Comments as part of Autamation comment
