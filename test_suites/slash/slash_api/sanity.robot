*** Settings ***
Documentation     This is a simple test with Robot Framework
Suite Setup       Create Backend
Suite Teardown    Delete Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${deployment_id}
Test Setup
Test Teardown
Default Tags      Sanity
Library           SlashAPI
Library           Collections
Variables         ../../../conf/slash/slash_api/variables.py

*** Variables ***
${deployment_id}    ${EMPTY}
${Session_alias}    Session1
${deployment_endpoint}    ${EMPTY}
${deployemnt_jwt_token}    ${EMPTY}
${deployment_auth}    ${EMPTY}
${api_key_uid}    ${EMPTY}

*** Test Cases ***
Create Deployment
    [Documentation]    List of tests covered
    ...
    ...    - Create Deployment
    ...    \ \ \ \ - Delete Deployment
    [Tags]    C236    Sanity
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    ${backend_id}=    Collections.Get From Dictionary    ${data}    uid
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${backend_id}

Get deployments
    [Documentation]    List of tests covered
    ...
    ...    - Get Deployments
    ...    \ \ \ \ - Deployments health API
    [Tags]    C224    Sanity
    ${deployments}=    Get Deployments    ${Session_alias}    ${URL}    ${HEADERS}
    log    ${deployments}
    sleep    200
    Get Deployment Health    ${Session_alias}    ${deployment_endpoint}    ${HEADERS}

Update Deployment mode
    Update Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${deployment_id}    test-edit    deployment_mode=flexible
    Get Deployment Health    ${Session_alias}    ${deployment_endpoint}    ${HEADERS}

create manual backup
    Backup Ops    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    create
    sleep    60

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
    ${api_key_details}=    Create Api Key    ${Session_alias}    ${URL}    ${HEADERS}    ${deployment_id}    test
    log    ${api_key_details}
    ${api_key_uid}=    Collections.Get From Dictionary    ${api_key_details}    uid
    Get Api Key    ${Session_alias}    ${URL}    ${HEADERS}    ${deployment_id}
    Delete Api Key    ${Session_alias}    ${URL}    ${HEADERS}    ${deployment_id}    ${api_key_uid}

freeze deployment
    Freeze Ops    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    false    true
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    Set Suite Variable    ${deployment_id}
    ${deployment_url}=    Collections.Get From Dictionary    ${data}    url
    Get Deployment Health    ${Session_alias}    https://${deployment_url}    ${HEADERS}
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${deployment_id}

*** Keywords ***
Create Backend
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    Set Suite Variable    ${deployment_id}
    ${endpoint}=    Collections.Get From Dictionary    ${data}    url
    ${deployment_endpoint}=    Catenate    SEPARATOR=    https://    ${endpoint}
    Set Suite Variable    ${deployment_endpoint}
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    ${deployemnt_jwt_token}=    Collections.Get From Dictionary    ${data}    jwtToken
    Set Suite Variable    ${deployemnt_jwt_token}
    ${deployment_auth}=    Create Dictionary    x-auth-token=${deployemnt_jwt_token}
    Set Suite Variable    ${deployment_auth}
