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
Create Deployment
    [Documentation]    List of tests covered
    ...
    ...    - Create Deployment
    ...    \ \ \ \ - Delete Deployment
    [Tags]    C236    Sanity
    [Template]
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    ${backend_id}=    Collections.Get From Dictionary    ${data}    uid
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${backend_id}
    [Teardown]

Get deployments
    [Documentation]    List of tests covered
    ...
    ...    - Get Deployments
    ...    \ \ \ \ - Deployments health API
    [Tags]    C224    Sanity
    ${deployments}=    Get Deployments    ${Session_alias}    ${URL}    ${HEADER}
    log    ${deployments}
    Get Deployment Health    ${Session_alias}    ${deployment_endpoint}    ${HEADER}

Update Deployment mode
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    test-edit    deployment_mode=flexible
    Get Deployment Health    ${Session_alias}    ${deployment_endpoint}    ${HEADER}

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
    Comment    ${deployment_auth}=    Create Dictionary    x-auth-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJzL3Byb3h5IiwiZHVpZCI6IjB4MTBhNDAxIiwiZXhwIjoxNjExNTYwMzg0LCJpc3MiOiJzL2FwaSJ9.NvLjMPzfdkaYO6puXErMIsJjr7x9FkvS7Px2BzfZ0ns
    ${backups} =    Backup Ops    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    list
    log    ${backups}

create , get and delete API key
    [Documentation]    List of tests covered
    ...
    ...    - Create API key
    ...    \ \ \ \ - Delete API Key
    ...    - Get API key
    ${api_key_details}=    Create Api Key    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    test
    log    ${api_key_details}
    ${details}=    Collections.Get From Dictionary    ${api_key_details}    data
    ${api_key_details}=    Collections.Get From Dictionary    ${details}    createAPIKey
    ${api_key_uid}=    Collections.Get From Dictionary    ${api_key_details}    uid
    Get Api Key    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    Delete Api Key    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    ${api_key_uid}    API Key Deleted Successfully.

freeze deployment
    Freeze Ops    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    false    true

Create and use Multiple API Keys
    [Documentation]    List of Tests Covered
    ...
    ...    Create 6 API keys
    ...    Update Schema with API key1
    ...    Get Schema with API key2
    ...    Add mutation with API key3
    ...    Drop data from database with API key4
    ...    Drop schema with API key5
    ...    Get Schema with API key6
    @{api_keys_uid}=    Create List
    &{api_keys}=    Create Dictionary
    FOR    ${i}    IN RANGE    1    7
        ${api_key_uid}    ${api_key}    Create API Keys    ${deployment_id}    test${i}
        Append To List    ${api_keys_uid}    ${api_key_uid}
        Set To Dictionary    ${api_keys}    test${i}    ${api_key}
        log    ${api_key_uid}
        log    ${api_key}
    END
    ${deployment_auth}=    Create Dictionary    x-auth-token=${api_keys}[test1]    Content-Type=application/json
    Update Schema To Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${Schema}
    ${deployment_auth}=    Create Dictionary    x-auth-token=${api_keys}[test2]    Content-Type=application/json
    ${schema}=    Get Schema From Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    Run Keyword If    '${schema}'=='${EMPTY}'    Fail
    ${deployment_auth}=    Create Dictionary    x-auth-token=${api_keys}[test3]    Content-Type=application/json
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${mutation_query_1}
    ${deployment_auth}=    Create Dictionary    x-auth-token=${api_keys}[test4]    Content-Type=application/json
    Drop Data From Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    ${deployment_auth}=    Create Dictionary    x-auth-token=${api_keys}[test5]    Content-Type=application/json
    Drop Data From Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${True}
    ${deployment_auth}=    Create Dictionary    x-auth-token=${api_keys}[test6]    Content-Type=application/json
    ${schema}=    Get Schema From Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    FOR    ${api_key_uid}    IN    @{api_keys_uid}
        Delete API Keys    ${api_key_uid}
    END

update Deployment name
    [Documentation]    List of tests covered
    ...
    ...    - Update deployment name
    [Tags]    C236    Sanity
    [Template]
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    updated
    ${deployment_details}=    Get Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    ${deployment_name}=    get deployment attribute data    ${deployment_details}    name
    Should Be Equal    ${deployment_name}    updated
    [Teardown]

update Deployment type from free to shared
    [Documentation]    List of tests covered
    ...
    ...    - Update deployment name
    [Tags]    C236    Sanity
    [Template]
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    deploymentType=shared
    ${deployment_details}=    Get Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    ${type}=    get deployment attribute data    ${deployment_details}    deploymentType
    Should Be Equal    ${type}    shared
    [Teardown]

Update Schema with Non-Existing API Key
    [Documentation]
    ...    List of Tests Covered
    ...
    ...    Create API Key
    ...    Update Schema with API Key
    ...    Delete API Key
    ...    Update Schema with that API Key
    ${api_key_uid}     ${api_key}      Create API Keys      ${deployment_id}      test
    ${deployment_auth}=    Create Dictionary    x-auth-token=${api_key}    Content-Type=application/json
    Update Schema To Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${Schema}
    Delete API Keys    ${api_key_uid}
    Update Schema To Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${Schema}      401


*** Keywords ***
Create Backend
    ${auth_token}=    Login    ${Session_alias}    ${URL}    ${HEADERS}    ${USER_NAME}    ${PASSWORD}
    ${HEADER}=    Create Dictionary    Authorization=Bearer ${auth_token}    Content-Type=application/json
    Set Suite Variable    ${HEADER}
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    free
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    ${endpoint}=    Collections.Get From Dictionary    ${data}    url
    ${deployment_endpoint}=    Catenate    SEPARATOR=    https://    ${endpoint}
    Get Deployment Health    ${Session_alias}    ${deployment_endpoint}    ${HEADERS}
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    Set Suite Variable    ${deployment_id}
    Set Suite Variable    ${deployment_endpoint}
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    ${deployemnt_jwt_token}=    Collections.Get From Dictionary    ${data}    jwtToken
    Set Suite Variable    ${deployemnt_jwt_token}
    ${deployment_auth}=    Create Dictionary    x-auth-token=${deployemnt_jwt_token}    Content-Type=application/json
    Set Suite Variable    ${deployment_auth}

Create API Keys
    [Arguments]    ${deployment_id}    ${api_name}
    ${api_key_details}=    Create Api Key    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    ${api_name}
    ${details}=    Collections.Get From Dictionary    ${api_key_details}    data
    ${api_key_details}=    Collections.Get From Dictionary    ${details}    createAPIKey
    ${api_key_uid}=    Collections.Get From Dictionary    ${api_key_details}    uid
    ${api_key}=    Collections.Get From Dictionary    ${api_key_details}    key
    [Return]    ${api_key_uid}    ${api_key}

Delete API Keys
    [Arguments]    ${api_key_uid}
    Delete Api Key    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    ${api_key_uid}    API Key Deleted Successfully.

get deployment attribute data
    [Arguments]    ${deployment_details}    ${attribute}
    ${data}=    Collections.Get From Dictionary    ${deployment_details}    data
    ${deployments}=    Collections.Get From Dictionary    ${data}    getDeploymentByID
    ${attribute_data}=    Collections.Get From Dictionary    ${deployments}    ${attribute}
    [Return]    ${attribute_data}
