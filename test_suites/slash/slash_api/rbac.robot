*** Settings ***
Documentation     It contains RBAC test cases for Slash API
Suite Setup       Run Keywords    Create Backend     AND     Add Schema and Mutation
Suite Teardown    Delete Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${deployment_id}  
Test Setup        
Test Teardown
Library           SlashAPI
Library           Collections
Variables         ../../../conf/slash/slash_api/variables.py

*** Variables ***
${Session_alias}    Session1
${User2_Auth}     eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJzL3Byb3h5IiwiZHVpZCI6IjB4MjEwMjEiLCJleHAiOjE2MTYwNzY3ODIsImlzcyI6InMvYXBpIn0.h-IbsGz5vF_UyNiQk5GXlCYbZ9NbiG7TC_O9WDGGvW8
${SCHEMA}     type User {id: ID!  firstName: String! lastName: String!} type Todo {id: ID!  Name: String!}
${QUERY}        {"query":"query MyQuery {  queryUser {id  firstName  lastName }}","variables":null,"operationName":"MyQuery"}
${AGGREGATE}        {"query":"query MyQuery {aggregateUser { count  }}","variables":null,"operationName":"MyQuery"}
${GETQUERY}      {"query":"query MyQuery { getUser(id: \\"0x4\\") { firstName   id   lastName  }}","variables":null,"operationName":"MyQuery"}
${UPDATE}        {"query":"mutation MyMutation {  updateUser(input: {filter: {id: \\"0x4\\"}, set: {firstName: \\"user2\\"}}) {   numUids }}","variables":null,"operationName":"MyMutation"}
${DELETE}        {"query":"mutation MyMutation { deleteUser(filter: {id: \\"0x4\\"}) { msg }}","variables":null,"operationName":"MyMutation"}

*** Test Cases ***
Anonymous User Access the Type that Owner given Read Operations
    [Documentation]    
    ...    List of tests covered
    ...
    ...    
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${READ_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    log     ${rules}
    Sleep    10 minutes  
    ${deployment_auth}=    Create Dictionary    dg-auth=${User2_Auth}    Content-Type=application/json
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY}
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${AGGREGATE}
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${GETQUERY}

Anonymous User Access the Type that the Owner not given Read Operation Access
    [Documentation]
    ...     List of tests covered
    ...
    ...
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${WRITE_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    log     ${rules}
    Sleep    10 minutes  
    ${deployment_auth}=    Create Dictionary    dg-auth=${User2_Auth}    Content-Type=application/json
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY}     403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${AGGREGATE}     403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${GETQUERY}     403

Anonymous User Access the Type that the Owner not given Write Operation Access
    [Documentation]
    ...     List of tests covered
    ...
    ...
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${READ_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    log     ${rules}
    Sleep    10 minutes  
    ${deployment_auth}=    Create Dictionary    dg-auth=${User2_Auth}    Content-Type=application/json
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${MUTATION1}     403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${UPDATE}        403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${DELETE}        403

Anonymous User Access the Type that the Owner after removed the read access 
    [Documentation]    
    ...    List of tests covered
    ...
    ...    
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${READ_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    log     ${rules}
    Sleep    10 minutes
    ${deployment_auth}=    Create Dictionary    dg-auth=${User2_Auth}    Content-Type=application/json
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY}
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${WRITE_RULES}
    Sleep    10 minutes
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY}     403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${AGGREGATE}     403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${GETQUERY}     403

Anonymous User Access the Type that the Owner after removed the write access 
    [Documentation]    
    ...    List of tests covered
    ...
    ...    
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${WRITE_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    log     ${rules}
    Sleep    10 minutes
    ${deployment_auth}=    Create Dictionary    dg-auth=${User2_Auth}    Content-Type=application/json
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${MUTATION1}
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${READ_RULES}
    Sleep    10 minutes
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${MUTATION1}     403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${UPDATE}      403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${DELETE}      403

Anonymous User Access the Type that Owner given Write Operations
    [Documentation]    
    ...    List of tests covered
    ...
    ...    
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${WRITE_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    log     ${rules}
    Sleep    10 minutes  
    ${deployment_auth}=    Create Dictionary    dg-auth=${User2_Auth}    Content-Type=application/json
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${MUTATION1}
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${UPDATE}
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${DELETE}

*** Keywords ***
Create Backend
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${BACKEND_NAME}    us-west-2     free
    ${endpoint}=    Collections.Get From Dictionary    ${data}    url
    ${deployment_endpoint}=    Catenate    SEPARATOR=    https://    ${endpoint}
    Get Deployment Health    ${Session_alias}    ${deployment_endpoint}    ${HEADERS}
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    Set Suite Variable    ${deployment_id}
    Set Suite Variable    ${deployment_endpoint}
    ${deployment_jwt_token}=    Collections.Get From Dictionary    ${data}    jwtToken
    Set Suite Variable    ${deployment_jwt_token}
    ${deployment_auth}=    Create Dictionary    x-auth-token=${deployment_jwt_token}    Content-Type=application/json
    Set Suite Variable    ${deployment_auth}

Add Schema and Mutation
    Update Schema To Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${SCHEMA}
    ${schema}=    Get Schema From Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    log    ${schema}
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${MUTATION1}
