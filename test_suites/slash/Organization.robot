*** Settings ***
Documentation     This is a simple test with Robot Framework
Test Setup        Setup
Test Teardown     Close Browser    ${Browser_Alias}
Library           Slash
Variables         ../../conf/slash/variables.py
Library           AWSLibrary
Library           OperatingSystem

*** Variables ***
${Browser_Alias}    Browser1
${invalid_user_alert}    No user found with this email
${invalid_email}    a@b.com

*** Test Cases ***
Add member to an Organization
    [Documentation]    *Test includes the followig Scenarios*
    ...
    ...    \ \ - Add member to an Organization
    ...    \ - Remove member from an Organization
    ...    - Leave from an Organization
    sleep    20
    Click Organizations In Profile    ${Browser_Alias}
    Get Organization List    ${Browser_Alias}
    Click Organization    ${Browser_Alias}    ${ORGANIZATION_NAME}
    Add Member To Organization    ${Browser_Alias}    ${USER_NAME_2}
    sleep    2
    Remove Member From Organization    ${Browser_Alias}    ${USER_NAME_2}
    sleep    2
    Add Member To Organization    ${Browser_Alias}    ${USER_NAME_2}
    Logout    ${Browser_Alias}
    Login    ${Browser_Alias}    ${USER_NAME_2}    ${PASSWORD}
    sleep    5
    Click Organizations In Profile    ${Browser_Alias}
    Get Organization List    ${Browser_Alias}
    Click Organization    ${Browser_Alias}    ${ORGANIZATION_NAME}
    Leave Member From Organization    ${Browser_Alias}    ${USER_NAME_2}
    sleep    2

validate only valid and registered emails can be added to an Organization
    [Documentation]    *Test includes the followig Scenarios*
    ...
    ...    \ \ - Add member to an Organization
    ...    \ - Remove member from an Organization
    ...    - Leave from an Organization
    [Tags]    Regression    Sanity
    sleep    20
    Click Organizations In Profile    ${Browser_Alias}
    sleep    5
    Get Organization List    ${Browser_Alias}
    Click Organization    ${Browser_Alias}    ${ORGANIZATION_NAME}
    sleep    3
    Add Member To Organization    ${Browser_Alias}    ${invalid_email}
    sleep    2
    Validate Organization Alert And Close Dialogue    ${Browser_Alias}    ${invalid_user_alert}

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}
