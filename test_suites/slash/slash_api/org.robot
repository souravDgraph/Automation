*** Settings ***
Documentation     This is a simple test with Robot Framework
Suite Setup       Run Keywords    Create Session For Organization  ${HEADER}    https://api.stage.thegaas.com    AND    Create Organization And Fetch Organization Id
...               AND     Create Backend    
Suite Teardown    Delete Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
Test Setup        
Test Teardown
Library           SlashAPI
Library           Collections
Variables         ../../../conf/slash/slash_api/variables.py

*** Variables ***
${Session_alias}    Session1
${user_email}       krishna+test1@dgraph.io
${org_name}     test


*** Test Cases ***
#Create Organization
#    #Create Organization    test7    200
#    ${res}=     Get Organizations List
#    log     ${res}

TC01 Create Organization and Manage organization for deployment
    [Documentation]  Test case to handle api functionality for organization
    [Tags]      regression
    Add Org To Deployment   ${BACKEND_NAME}     ${org_uid}
    Add New Member To Existing Organization    ${org_uid}    ${user_email}
    Remove Member From Existing Organization    ${org_uid}    ${user_email}
    Add Org To Deployment   ${BACKEND_NAME}     ${org_uid}
    Remove Org From Deployment   ${BACKEND_NAME}

TC_02 Check if member is already part of organization
    [Documentation]  Test case to check if memeber is already part of organization
    [Tags]      regression
    ${check}=   Check If Member Is Already Existing In Organization    ${org_uid}    ${user_email}
    log     ${check}

Organization Member Trying to Delete Backend
    [Documentation]
    ...    List of tests covered
    ...
    ...    Add new member to organization
    ...    Add organization to deployment
    ...    Delete deployment with organization member auth
    Add New Member To Existing Organization    ${org_uid}    ${user_email}
    Add Org To Deployment   ${BACKEND_NAME}     ${org_uid}
    Delete Deployment    ${Session_alias}    ${URL}    ${USER2_HEADER}    ${deployment_id}    expected_response=401
    Remove Member From Existing Organization    ${org_uid}    ${user_email}
    Remove Org From Deployment   ${BACKEND_NAME}

Organization Member Trying to Modify Backend
    [Documentation]
    ...    List of tests covered
    ...
    ...    Add new member to organization
    ...    Create Backend
    ...    Add organization to deployment
    ...    Modify deployment with organization member auth
    Add New Member To Existing Organization    ${org_uid}    ${user_email}
    Add Org To Deployment   ${BACKEND_NAME}     ${org_uid}
    Update Deployment    ${Session_alias}    ${URL}    ${USER2_HEADER}    ${deployment_id}    expected_response_text=Not Authorized to update the Deployment: ${deployment_id}
    Remove Member From Existing Organization    ${org_uid}    ${user_email}
    Remove Org From Deployment   ${BACKEND_NAME}

Organization Member Trying to Fetch Backend After Removed From Organization
    [Documentation]
    ...    List of tests covered
    ...
    ...    Add new member to organization
    ...    Add organization to deployment
    ...    Fetch Schema
    ...    Remove Member from organization
    ...    Fetch schema with organization member auth
    Add New Member To Existing Organization    ${org_uid}    ${user_email}
    Add Org To Deployment   ${BACKEND_NAME}     ${org_uid}
    ${deployment_auth}=    Create Dictionary    x-auth-token=${USER2_HEADER}    Content-Type=application/json
    Remove Member From Existing Organization    ${org_uid}    ${user_email}
    Get Schema From Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}     expected_response=401
    Remove Org From Deployment   ${BACKEND_NAME}

*** Keywords ***
Create Backend
    ${auth_token}=    Login    ${Session_alias}    ${URL}    ${HEADERS}    ${USER_NAME1}    ${PASSWORD}
    ${USER2_HEADER}=    Create Dictionary    Authorization=Bearer ${auth_token}    Content-Type=application/json
    Set Suite Variable    ${USER2_HEADER}
    ${auth_token}=    Login    ${Session_alias}    ${URL}    ${HEADERS}    ${USER_NAME}    ${PASSWORD}
    ${HEADER}=    Create Dictionary    Authorization=Bearer ${auth_token}    Content-Type=application/json
    Set Suite Variable    ${HEADER}
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}      free
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    ${endpoint}=    Collections.Get From Dictionary    ${data}    url
    ${deployment_endpoint}=    Catenate    SEPARATOR=    https://    ${endpoint}
    Get Deployment Health    ${Session_alias}    ${deployment_endpoint}    ${HEADER}
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    Set Suite Variable    ${deployment_id}
    Set Suite Variable    ${deployment_endpoint}
    ${deployment_jwt_token}=    Collections.Get From Dictionary    ${data}    jwtToken
    Set Suite Variable    ${deployment_jwt_token}
    ${deployment_auth}=    Create Dictionary    x-auth-token=${deployment_jwt_token}    Content-Type=application/json
    Set Suite Variable    ${deployment_auth}

Create Organization And Fetch Organization Id
    ${org_details}=     Create Organization    ${org_name}
    log     ${org_details}
    ${details}=    Collections.Get From Dictionary    ${org_details}    data
    ${organization}=    Collections.Get From Dictionary    ${details}    createOrganization
    ${org_uid}=    Collections.Get From Dictionary    ${organization}    uid
    Set Suite Variable      ${org_uid}
