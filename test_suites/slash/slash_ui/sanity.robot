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
Dashboard should show the cluster usage statistics
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the overview for the backend
    ...    dashboard shows the cluster usage statistics
    Click Overview In Menu       ${Browser_Alias}
    View Cluster Usage Statistics      ${Browser_Alias}  
    
User should be able to create backend and navigate to schema page
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the schema for the backend
    Click Schema In Menu     ${Browser_Alias}

User should be able to navigate to API Explorer
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the api explorer for the backend
    Click Api Explorer In Menu      ${Browser_Alias}

User should be able to navigate to Settings tab
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the settings for the backend
    Click Settings In Menu      ${Browser_Alias}

User should be able to view the graphql endpoint in Overview
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the overview for the backend
    ...    View the graphql endpoint
    Click Overview In Menu       ${Browser_Alias}
    View Graphql Endpoint      ${Browser_Alias}      ${BACKEND_ZONE}.aws.stage.thegaas.com/graphql

User should be able to view the location of the deployment
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the overview for the backend
    ...    View the location
    Click Overview In Menu       ${Browser_Alias}
    View Deployment Zone      ${Browser_Alias}       ${BACKEND_ZONE}
    
User should not be able to create more than one backend
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the launch new backend button
    ...    Check the starter product is disabled
    Click Launch New Backend      ${Browser_Alias}
    Check Starter Product Disabled       ${Browser_Alias}

User should be able to add new API key
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the settings for the backend
    ...    Click the api key tab
    ...    Create new api key
    ...    Verify api key generated
    Click Settings In Menu      ${Browser_Alias}
    Click Api Key Tab      ${Browser_Alias}
    Create New Api Key      ${Browser_Alias}       ${API_key_name}
    Verify Api Key Generated     ${Browser_Alias}     ${API_key_name}

User should be able to delete API Key
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the settings for the backend
    ...    Click the api key tab and create new api key
    ...    Verify Api key generated
    ...    Delete the API key
    Click Settings In Menu      ${Browser_Alias}
    Click Api Key Tab      ${Browser_Alias}
    Create New Api Key      ${Browser_Alias}       ${API_key_name}
    Verify Api Key Generated     ${Browser_Alias}     ${API_key_name}
    Delete Api Key      ${Browser_Alias}      ${API_key_name}

User should be able to delete a backend
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the settings for the backend
    ...    Click the general tab
    ...    Delete the deployment
    ...    Check the deployment is deleted
    Click Settings In Menu      ${Browser_Alias}
    Click General Tab      ${Browser_Alias}
    Delete Deployment     ${Browser_Alias}     ${BACKEND_NAME}
    Check Deployment Is Deleted     ${Browser_Alias}     ${BACKEND_NAME}
    [Teardown]     Create Backend

User should be able signout from the logout button in the header
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the avatar button
    ...    Click logout button
    Click Avatar    ${Browser_Alias}
    Click Logout Button    ${Browser_Alias}
    [Teardown]     Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}

User should be able to view the documentation
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the documentation for the backend
    Click Documentation In Menu     ${Browser_Alias}

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}

Create Backend
    Click Launch New Backend      ${Browser_Alias}     20
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      70

Delete Backend
    Click Settings In Menu      ${Browser_Alias}
    Click General Tab      ${Browser_Alias}
    Delete Deployment     ${Browser_Alias}     ${BACKEND_NAME}
    Check Deployment Is Deleted     ${Browser_Alias}     ${BACKEND_NAME}