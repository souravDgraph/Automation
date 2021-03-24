*** Settings ***
Documentation     This Suite contains the sanity test cases for Slash UI
Suite Setup       Setup
Suite Teardown    Close Browser    ${Browser_Alias}
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
    [Setup]     Create Backend
    Click Schema In Menu     ${Browser_Alias}
    [Teardown]     Delete Backend

User should be able to delete a backend
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Setup]     Create Backend
    Click Settings In Menu      ${Browser_Alias}
    Delete Deployment     ${Browser_Alias}     ${BACKEND_NAME}
    sleep     10

User should be able to navigate to API Explorer
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Setup]     Create Backend
    Click Api Explorer In Menu      ${Browser_Alias}
    [Teardown]      Delete Backend

User should be able to navigate to Settings tab
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Setup]      Create Backend
    Click Settings In Menu      ${Browser_Alias}
    [Teardown]    Delete Backend

User should be able to view the graphql endpoint
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Setup]     Create Backend
    Click Overview In Menu       ${Browser_Alias}
    View Graphql Endpoint      ${Browser_Alias}      https://${BACKEND_NAME}.${BACKEND_ZONE}.aws.cloud.dgraph.io/graphql
    [Teardown]      Delete Backend

User should be able to view the documentation
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Documentation In Menu     ${Browser_Alias}

User should not be able to create more than one backend
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Setup]     Create Backend
    sleep    20
    Click Launch New Backend      ${Browser_Alias}
    sleep    10
    Check Starter Product Disabled       ${Browser_Alias}
    [Teardown]     Delete Backend

User should be able to add new API key
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Setup]     Create Backend
    Click Settings In Menu      ${Browser_Alias}
    Click Api Key Tab      ${Browser_Alias}
    Create New Api Key      ${Browser_Alias}       ${API_key_name}
    sleep     20
    Verify Api Key Generated     ${Browser_Alias}     ${API_key_name}
    Click General Tab      ${Browser_Alias}
    [Teardown]      Delete Backend

User should be able to delete API Key
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Setup]     Create Backend
    Click Settings In Menu      ${Browser_Alias}
    Click Api Key Tab      ${Browser_Alias}
    Create New Api Key      ${Browser_Alias}       ${API_key_name}
    sleep     20
    Verify Api Key Generated     ${Browser_Alias}     ${API_key_name}
    Delete Api Key      ${Browser_Alias}      ${API_key_name}
    Click General Tab      ${Browser_Alias}
    [Teardown]      Delete Backend

User should be able signout from the logout button in the header
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Avatar    ${Browser_Alias}
    Click Logout Button    ${Browser_Alias}

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
    Monitor Backend Creation      ${Browser_Alias}      40

Delete Backend
    Click Settings In Menu      ${Browser_Alias}
    Delete Deployment     ${Browser_Alias}     ${BACKEND_NAME}
    sleep     10