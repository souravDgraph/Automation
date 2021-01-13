*** Settings ***
Documentation     This is a simple test with Robot Framework
Suite Teardown
Test Setup
Test Teardown
Library           SlashAPI
Library           Collections
Variables         ../../../conf/slash/slash_api/variables.py

*** Variables ***
${deployment_id}    ${EMPTY}
${Session_alias}    Session1

*** Test Cases ***
Create Deployment
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    Set Suite Variable    ${deployment_id}

Delete deployment
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${deployment_id}

*** Keywords ***
