*** Settings ***
Documentation     This Suite contains the sanity test cases for Slash UI
Test Teardown     Delete Backend
Suite Setup       Setup
Suite Teardown    Close Browser    ${Browser_Alias}
Library           Slash
Variables         ../../conf/slash/variables.py

*** Variables ***
${Browser_Alias}    Browser1
${GRAPHQL_GUIDE}      https://graphql.dgraph.io/slash-quick-start/
${API_key_name}     test

*** Test Cases ***
User should be able to create backend and navigate to schema page
    [Documentation]
    ...    List of tests covered
    ...
    ...
    sleep    20
    Click Launch New Backend      ${Browser_Alias}
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}
    sleep     10
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      70
    Click Schema In Backend Creation     ${Browser_Alias}

User should be able to delete a backend
    [Documentation]
    ...    List of tests covered
    ...
    ...
    sleep    20
    Click Launch New Backend      ${Browser_Alias}
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}
    sleep     10
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      70

User should be able to navigate to API Explorer
    [Documentation]
    ...    List of tests covered
    ...
    ...
    sleep    20
    Click Launch New Backend      ${Browser_Alias}
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}
    sleep     10
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      70
    Click Api Explorer In Menu      ${Browser_Alias}

User should be able to navigate to Settings tab
    [Documentation]
    ...    List of tests covered
    ...
    ...
    sleep    20
    Click Launch New Backend      ${Browser_Alias}
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}
    sleep     10
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      70

User should be able to view the graphql endpoint
    [Documentation]
    ...    List of tests covered
    ...
    ...
    sleep    20
    Click Launch New Backend      ${Browser_Alias}
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}
    sleep     10
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      70
    Click Overview In Menu       ${Browser_Alias}
    View Graphql Endpoint      ${Browser_Alias}      https://${BACKEND_NAME}.${BACKEND_ZONE}.aws.cloud.dgraph.io/graphql

User should be able to navigate to metrics tab
    [Documentation]
    ...    List of tests covered
    ...
    ...
    sleep    20
    Click Launch New Backend      ${Browser_Alias}
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}
    sleep     10
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      70
    Click Usage Metrics In Menu      ${Browser_Alias}

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    sleep     10
    Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}

Delete Backend
    Click Settings In Menu      ${Browser_Alias}
    Delete Deployment     ${Browser_Alias}     ${BACKEND_NAME}
    sleep     10