*** Settings ***
Documentation     This Suite contains the sanity test cases for Slash UI
Suite Setup       Run Keywords     Setup     AND     Create Backend        AND        Get Deployment Endpoint For Backend
Suite Teardown    Run Keywords     Delete Backend     AND    Close Browser    ${Browser_Alias}
Library           Slash
Library           SlashAPI
Library           Collections
Variables         ../../../conf/slash/variables.py
Variables         ../../../conf/slash/slash_api/variables.py

*** Variables ***
${Browser_Alias}    Browser1
${API_key_name}     test
${Session_alias}    Session1
${deployment_jwt_token}       eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJzL3Byb3h5IiwiZHVpZCI6IjB4Y2FkZmYyIiwiZXhwIjoxNjE3OTY0MTA0LCJpc3MiOiJzL2FwaSJ9.rtgNTm6ySN1RqnjE20i35QVaOuntfTXoiLe48cH_kVM

*** Test Cases ***
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
    View Graphql Endpoint      ${Browser_Alias}      ${BACKEND_ZONE}.enterprise.stage.thegaas.com/graphql

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

User should be able to add schema
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Tags]    1
    Click Schema In Menu     ${Browser_Alias}
    Click Switch To Ui Mode      ${Browser_Alias}
    Add Type     ${Browser_Alias}
    Add Field     ${Browser_Alias}       UntitledType0
    Change Field Name      ${Browser_Alias}      UntitledType0      untitledfield      name
    Deploy Schema      ${Browser_Alias}
    ${schema_result}=    Get Schema From Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    log      ${schema_result}
    Run Keyword If    '${schema_result}'!='${SCHEMA2}'    Fail

User should be able to edit and update schema
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Tags]    1
    Click Schema In Menu     ${Browser_Alias}
    Click Switch To Ui Mode      ${Browser_Alias}
    Add Field     ${Browser_Alias}         UntitledType0
    Change Field Name      ${Browser_Alias}      UntitledType0      untitledfield      age
    Change Field Type       ${Browser_Alias}      UntitledType0      age      String     Int
    Deploy Schema      ${Browser_Alias}
    ${schema_result}=    Get Schema From Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    log      ${schema_result}
    Run Keyword If    '${schema_result}'!='${SCHEMA3}'    Fail

Drop unused fields from Schema
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Tags]    1
    Click Schema In Menu     ${Browser_Alias}
    Click Switch To Ui Mode      ${Browser_Alias}
    Remove Field      ${Browser_Alias}      UntitledType0     age    
    Deploy Schema      ${Browser_Alias}
    Click Settings In Menu     ${Browser_Alias}
    Click Schema In Menu     ${Browser_Alias}
    Click Switch To Ui Mode      ${Browser_Alias}
    Click Drop Data Button     ${Browser_Alias}
    Select Unused Field      ${Browser_Alias}       UntitledType0.age
    Click Drop Button      ${Browser_Alias}
    Validate Field Removed      ${Browser_Alias}      UntitledType0.age
    ${schema_result}=    Get Schema From Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    log      ${schema_result}
    Run Keyword If    '${schema_result}'!='${SCHEMA2}'    Fail
    
Take Manual Backups
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Tags]    1
    Click Settings In Menu      ${Browser_Alias}
    Click Backups Tab      ${Browser_Alias}
    Click Create Backup Button       ${Browser_Alias}

List Backups
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Tags]    1
    Click Settings In Menu      ${Browser_Alias}
    Click Backups Tab      ${Browser_Alias}

Add Card And Verify Billing page
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Tags]    1
    Click Launch New Backend      ${Browser_Alias}     20
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}       Slash GraphQL
    Click Launch Button      ${Browser_Alias}
    Add Card     ${Browser_Alias}       4242424242424242      424      242      42424
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      70
    Click Billing Button     ${Browser_Alias}

Cancel Subscription
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Tags]    1
    Click Avatar    ${Browser_Alias}
    Click Billing Button     ${Browser_Alias}
    Cancel Subscription      ${Browser_Alias}

Should be able to run a mutation
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Tags]    1
    Click Api Explorer In Menu      ${Browser_Alias}
    Select Query Type       ${Browser_Alias}        mutation
    Click Add Query Type Button        ${Browser_Alias}       mutation
    Expand Add Query        ${Browser_Alias}        add       UntitledType0
    Add Value To Field        ${Browser_Alias}        name        santhosh
    Click Execute Query Button       ${Browser_Alias}
    Click Remove Query Button        ${Browser_Alias}       mutation
    ${response}=       Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY1}
    Run Keyword If    ${response}=='${EMPTY}'    Fail

Should be able to query and return response
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Tags]    1
    Click Api Explorer In Menu      ${Browser_Alias}
    Select Query Type       ${Browser_Alias}        query
    Click Add Query Type Button        ${Browser_Alias}       query
    Expand Add Query        ${Browser_Alias}        query       UntitledType0
    Select Search Fields     ${Browser_Alias}        ${FIELD_NAMES}
    Click Execute Query Button       ${Browser_Alias}
    Click Remove Query Button        ${Browser_Alias}       query
    ${response}=       Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY1}
    Run Keyword If    ${response}=='${EMPTY}'    Fail

Drop data from schema
    [Documentation]
    ...    List of tests covered
    ...
    ...
    [Tags]    1
    Click Api Explorer In Menu      ${Browser_Alias}
    Select Query Type       ${Browser_Alias}        mutation
    Click Add Query Type Button        ${Browser_Alias}       mutation
    Expand Add Query        ${Browser_Alias}        add       UntitledType0
    Add Value To Field        ${Browser_Alias}        name        santhosh
    Click Execute Query Button       ${Browser_Alias}
    Click Remove Query Button        ${Browser_Alias}       mutation
    Click Schema In Menu     ${Browser_Alias}
    Click Drop Data Button      ${Browser_Alias}
    Click Drop All Data Button      ${Browser_Alias}
    ${response}=       Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY1}
    Run Keyword If    ${response}!='${EMPTY}'    Fail

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    Login Ui    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}

Create Backend
    Click Launch New Backend      ${Browser_Alias}     20
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      70
    ${deployment_auth}=    Create Dictionary    x-auth-token=${deployment_jwt_token}    Content-Type=application/json
    Set Suite Variable      ${deployment_auth}

Delete Backend
    Click Settings In Menu      ${Browser_Alias}
    Click General Tab      ${Browser_Alias}
    Delete Deployment     ${Browser_Alias}     ${BACKEND_NAME}
    Check Deployment Is Deleted     ${Browser_Alias}     ${BACKEND_NAME}

Get Deployment Endpoint For Backend
    Click Overview In Menu      ${Browser_Alias}
    ${deployment_endpoint}=        Get Deployment Endpoint        ${Browser_Alias}         ${BACKEND_ZONE}.enterprise.stage.thegaas.com/graphql
    Set Suite Variable       ${deployment_endpoint}