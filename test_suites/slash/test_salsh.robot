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

*** Test Cases ***
launch and login
    [Tags]    Sanity    Regression
    Click Launch New Backend    ${Browser_Alias}
    Fill Backend Details    ${Browser_Alias}    ${BACKEND_NAME}    organization=${ORGANIZATION}
    Click Launch Button    ${Browser_Alias}
    Monitor Backend Creation    ${Browser_Alias}    ${BACKEND_MONITORING_TIMEOUT}
    Click Lambdas In Menu    ${Browser_Alias}
    ${lambda_script}=    Get File    ../../conf/slash/lambda_script
    log    ${lambda_script}
    Fill Lambda Script    ${Browser_Alias}    ${lambda_script}
    Click Settings In Menu    ${Browser_Alias}
    Validate General Tab Data    ${Browser_Alias}    ${BACKEND_NAME}    ${ORGANIZATION}
    Update Backend Organization    ${Browser_Alias}    ${NEW_ORGANIZATION}
    Delete Deployment    ${Browser_Alias}    ${BACKEND_NAME}

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}
