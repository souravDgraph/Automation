*** Settings ***
Documentation     This Suite contains the sanity test cases for Slash UI
Suite Setup       Run Keywords     Setup     AND     Create Backend
Suite Teardown    Run Keywords     Delete Backend     AND    Close Browser    ${Browser_Alias}
Library           Slash
Variables         ../../../conf/slash/variables.py

*** Variables ***
${Browser_Alias}    Browser1
${API_key_name}     test

*** Test Cases ***
User should be able to create backend and navigate to schema page
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Schema In Menu     ${Browser_Alias}

User should be able to navigate to API Explorer
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Api Explorer In Menu      ${Browser_Alias}

User should be able to navigate to Settings tab
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Settings In Menu      ${Browser_Alias}

User should be able to view the graphql endpoint in Overview
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Overview In Menu       ${Browser_Alias}
    View Graphql Endpoint      ${Browser_Alias}      ${BACKEND_ZONE}.aws.stage.thegaas.com/graphql

User should not be able to create more than one backend
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Launch New Backend      ${Browser_Alias}
    sleep    10
    Check Starter Product Disabled       ${Browser_Alias}

User should be able to add new API key
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Settings In Menu      ${Browser_Alias}
    Click Api Key Tab      ${Browser_Alias}
    Create New Api Key      ${Browser_Alias}       ${API_key_name}
    sleep     20
    Verify Api Key Generated     ${Browser_Alias}     ${API_key_name}

User should be able to delete API Key
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Settings In Menu      ${Browser_Alias}
    Click Api Key Tab      ${Browser_Alias}
    Create New Api Key      ${Browser_Alias}       ${API_key_name}
    sleep     20
    Verify Api Key Generated     ${Browser_Alias}     ${API_key_name}
    Delete Api Key      ${Browser_Alias}      ${API_key_name}

User should be able to delete a backend
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Settings In Menu      ${Browser_Alias}
    Click General Tab      ${Browser_Alias}
    Delete Deployment     ${Browser_Alias}     ${BACKEND_NAME}
    Check Deployment Is Deleted     ${Browser_Alias}     ${BACKEND_NAME}
    [Teardown]     Create Backend

User should be able signout from the logout button in the header
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Avatar    ${Browser_Alias}
    Click Logout Button    ${Browser_Alias}
    [Teardown]     Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}

User should be able to view the documentation
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Documentation In Menu     ${Browser_Alias}

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    sleep     10
    Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}

Create Backend
    sleep    20
    Click Launch New Backend      ${Browser_Alias}
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}
    sleep     10
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      70

Delete Backend
    Click Settings In Menu      ${Browser_Alias}
    Click General Tab      ${Browser_Alias}
    Delete Deployment     ${Browser_Alias}     ${BACKEND_NAME}
    Check Deployment Is Deleted     ${Browser_Alias}     ${BACKEND_NAME}