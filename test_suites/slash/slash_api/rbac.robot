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
${type}     User
${write_access}     write

*** Test Cases ***
Anonymous User Access the Type that Owner given Read Operations
    [Documentation]    
    ...    List of tests covered
    ...
    ...    
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${READ_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    Validate Rules For Deployment    ${rules}     ${type}
    Sleep    ${SLEEP_TIME} 
    ${deployment_auth}=    Create Dictionary    dg-auth=${User2_Auth}    Content-Type=application/json
    ${query_result}=    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY}
    Run Keyword If    ${query_result}=='${EMPTY}'    Fail
    ${aggregate_query_result}=    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${AGGREGATEQUERY}
    Run Keyword If    ${aggregate_query_result}=='${EMPTY}'    Fail
    ${get_query_result}=    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${GETQUERY}
    Run Keyword If    ${get_query_result}=='${EMPTY}'    Fail

Anonymous User Access the Type that the Owner not given Read Operation Access
    [Documentation]
    ...     List of tests covered
    ...
    ...
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${WRITE_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    Validate Rules For Deployment    ${rules}    ${type}    ${write_access}
    Sleep    ${SLEEP_TIME}   
    ${deployment_auth}=    Create Dictionary    dg-auth=${User2_Auth}    Content-Type=application/json
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY}     403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${AGGREGATEQUERY}     403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${GETQUERY}     403

Anonymous User Access the Type that the Owner not given Write Operation Access
    [Documentation]
    ...     List of tests covered
    ...
    ...
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${READ_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    Validate Rules For Deployment    ${rules}    ${type}
    Sleep    ${SLEEP_TIME}   
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
    Validate Rules For Deployment    ${rules}    ${type}
    Sleep    ${SLEEP_TIME} 
    ${deployment_auth}=    Create Dictionary    dg-auth=${User2_Auth}    Content-Type=application/json
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY}
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${WRITE_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    Validate Rules For Deployment    ${rules}    ${type}     ${write_access}
    Sleep    ${SLEEP_TIME} 
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${QUERY}     403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${AGGREGATEQUERY}     403
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${GETQUERY}     403

Anonymous User Access the Type that the Owner after removed the write access 
    [Documentation]    
    ...    List of tests covered
    ...
    ...    
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${WRITE_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    Validate Rules For Deployment    ${rules}    ${type}     ${write_access}
    Sleep    ${SLEEP_TIME} 
    ${deployment_auth}=    Create Dictionary    dg-auth=${User2_Auth}    Content-Type=application/json
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${MUTATION1}
    Update Rules To Deployment    ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}     ${READ_RULES}
    ${rules}=    Get Existing Rules     ${Session_alias}     ${URL}     ${HEADERS}     ${deployment_id}
    Validate Rules For Deployment    ${rules}    ${type}
    Sleep    ${SLEEP_TIME} 
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
    Validate Rules For Deployment    ${rules}    ${type}     ${write_access}
    Sleep    ${SLEEP_TIME}  
    ${deployment_auth}=    Create Dictionary    dg-auth=${User2_Auth}    Content-Type=application/json
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${MUTATION1}
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${UPDATE}
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${DELETE}

*** Keywords ***
Create Backend
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${BACKEND_NAME}    us-west-2
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
    Update Schema To Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${SCHEMA1}
    ${schema}=    Get Schema From Deployment    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}
    log    ${schema}
    Perform Operation To Database    ${Session_alias}    ${deployment_endpoint}    ${deployment_auth}    ${MUTATION1}
