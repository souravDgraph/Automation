*** Settings ***
Documentation     This is a simple test with Robot Framework
Test Setup        Setup
Test Teardown     Close Browser    ${Browser_Alias}
Library           Slash
Variables         ../../conf/slash/variables.py
Variables         ../../conf/slash/variables.py

*** Variables ***
${Browser_Alias}    Browser1

*** Test Cases ***
launch and login
    Click Launch New Backend    ${Browser_Alias}
    Fill Backend Details    ${Browser_Alias}    ${BACKEND_NAME}    organization=${ORGANIZATION}
    Click Launch Button    ${Browser_Alias}
    Monitor Backend Creation    ${Browser_Alias}    ${BACKEND_MONITORING_TIMEOUT}
    Click Settings In Menu    ${Browser_Alias}
    Validate General Tab Data    ${Browser_Alias}    ${BACKEND_NAME}    ${ORGANIZATION}
    Update Backend Organization    ${Browser_Alias}    ${NEW_ORGANIZATION}
    Delete Deployment    ${Browser_Alias}    ${BACKEND_NAME}

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}
