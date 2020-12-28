*** Settings ***
Documentation     This is a simple test with Robot Framework
Test Setup        Setup
Test Teardown     Close Browser    ${Browser_Alias}
Library           Slash
Variables         ../../conf/slash/variables.py

*** Variables ***
${Browser_Alias}    Browser1

*** Test Cases ***
launch and login
    [Tags]    Sanity    Regression

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}
