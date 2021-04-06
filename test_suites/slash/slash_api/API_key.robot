*** Settings ***
Documentation     This is a simple test with Robot Framework
Suite Setup       Create Backend
Suite Teardown    Delete Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
Test Setup
Test Teardown
Default Tags      Sanity
Library           SlashAPI
Library           Collections
Variables         ../../../conf/slash/slash_api/variables.py

*** Variables ***
${Session_alias}    Session1

*** Test Cases ***
Introspection API without Schema
    ${response}=    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${introspection_query}
    ${errors}=    Get From Dictionary    ${response}    errors
    ${error_messages}=    Get From List    ${errors}    0
    ${message}=    Get From Dictionary    ${error_messages}    message
    log    ${No_schema_error}
    log    ${message}
    Should Contain    ${message}    ${No_schema_error}

Add schema and perform queries and mutation
    Update Schema To Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${SCHEMA}
    ${schema}=    Get Schema From Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    Run Keyword If    '${schema}'=='${EMPTY}'    Fail
    Log    Add data to database - Mutation
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${MUTATION_QUERY_1}
    Log    Fetch data from database - Query
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY}
    Log    Drop data from database
    Drop Data From Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    Log    Drop data and schema from database
    Drop Data From Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${True}
    ${schema}=    Get Schema From Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    Run Keyword If    '${schema}'!='${EMPTY}'    Fail

Introspection API with Schema
    Update Schema To Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${Schema}
    ${schema}=    Get Schema From Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    Run Keyword If    '${schema}'=='${EMPTY}'    Fail
    ${response}=    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${introspection_query}
    ${errors}=    Get From Dictionary    ${response}    data
    ${value}=    Get From Dictionary    ${errors}    __schema
    ${errors}=    Get From Dictionary    ${value}    __typename
    Should not Contain    ${errors}    ${No_schema_error}

create manual backup
    Backup Ops    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    create

list backups
    ${backups} =    Backup Ops    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    list
    log    ${backups}

freeze deployment
    Freeze Ops    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    false    true

*** Keywords ***
Create Backend
    ${auth_token}=    Login    ${Session_alias}    ${URL}    ${HEADERS}    ${USER_NAME}    ${PASSWORD}
    ${HEADER}=    Create Dictionary    Authorization=Bearer ${auth_token}    Content-Type=application/json
    Set Suite Variable    ${HEADER}
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    ${endpoint}=    Collections.Get From Dictionary    ${data}    url
    ${deployment_endpoint}=    Catenate    SEPARATOR=    https://    ${endpoint}
    Get Deployment Health    ${Session_alias}    ${deployment_endpoint}    ${HEADER}
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    Set Suite Variable    ${deployment_id}
    Set Suite Variable    ${deployment_endpoint}
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    ${deployemnt_jwt_token}=    Collections.Get From Dictionary    ${data}    jwtToken
    ${api_key}=    Generate_APIKEY    ${deployment_id}    key1
    Set Suite Variable    ${deployemnt_jwt_token}
    ${deployment_auth}=    Create Dictionary    x-auth-token=${api_key}    Content-Type=application/json
    Set Suite Variable    ${deployment_auth}

Generate_APIKEY
    [Arguments]    ${deployment_id}    ${api_key_name}    ${api_key_type}=admin
    ${api_key_details}=    Create Api Key    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    ${api_key_name}    ${api_key_type}
    log    ${api_key_details}
    ${details}=    Collections.Get From Dictionary    ${api_key_details}    data
    ${api_key_details}=    Collections.Get From Dictionary    ${details}    createAPIKey
    ${api_key}=    Collections.Get From Dictionary    ${api_key_details}    key
    [Return]    ${api_key}
