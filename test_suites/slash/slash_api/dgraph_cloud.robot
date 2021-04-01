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
create Dgraph cloud deployment
    [Documentation]    List of tests covered
    ...
    ...    - Create Dgraph cloud Deployment
    [Tags]    C236    Sanity
    [Template]
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    dedicated
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}    deploymentType=dedicated    size=medium    alphaStorage=40
    ${backend_id}=    Collections.Get From Dictionary    ${data}    uid
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${backend_id}
    [Teardown]

update Deployment name
    [Documentation]    List of tests covered
    ...
    ...    - Update dgraph cloud deployment name
    [Tags]    C236    Sanity
    [Template]
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    updated
    ${deployment_details}=    Get Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    ${deployment_name}=    get deployment attribute data    ${deployment_details}    name
    Should Be Equal    ${deployment_name}    updated
    [Teardown]

update Deployment HA
    [Documentation]    List of tests covered
    ...
    ...    - Update dgraph cloud deployment HA
    [Tags]    C236    Sanity
    [Template]
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    dgraphHA=true
    ${deployment_details}=    Get Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    ${deployment_HA}=    get deployment attribute data    ${deployment_details}    dgraphHA
    Should Be Equal    ${deployment_HA}    true
    [Teardown]

Update deployment jaeger
    [Documentation]    List of tests covered
    ...
    ...    - Update dgraph cloud deployment jaeger
    [Tags]    C236    Sanity
    [Template]
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    jaegerEnabled=true
    ${deployment_details}=    Get Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    ${jaeger}=    get deployment attribute data    ${deployment_details}    jaegerEnabled
    Should Be Equal    ${jaeger}    true
    [Teardown]

Update deployment ACL
    [Documentation]    List of tests covered
    ...
    ...    - Update dgraph cloud deployment jaeger
    [Tags]    C236    Sanity
    [Template]
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    aclEnabled=true
    ${deployment_details}=    Get Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    ${backup_interval}=    get deployment attribute data    ${deployment_details}    aclEnabled
    Should Be Equal    ${backup_interval}    true
    [Teardown]

Update deployment size
    [Documentation]    List of tests covered
    ...
    ...    - Update dgraph cloud deployment jaeger
    [Tags]    C236    Sanity
    [Template]
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    size=large
    ${deployment_details}=    Get Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    ${size}=    get deployment attribute data    ${deployment_details}    size
    Should Be Equal    ${size}    large
    [Teardown]

update Deployment mode
    [Documentation]    List of tests covered
    ...
    ...    - Update dgraph cloud deployment name
    [Tags]    C236    Sanity
    [Template]
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    deploymentMode=readonly
    ${deployment_details}=    Get Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    ${deployment_mode}=    get deployment attribute data    ${deployment_details}    deploymentMode
    Should Be Equal    ${deployment_mode}    readonly
    [Teardown]

*** Keywords ***
Create Backend
    ${auth_token}=    Login    ${Session_alias}    ${URL}    ${HEADERS}    ${USER_NAME}    ${PASSWORD}
    ${HEADER}=    Create Dictionary    Authorization=Bearer ${auth_token}    Content-Type=application/json
    Set Suite Variable    ${HEADER}
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    dedicated
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}    deploymentType=dedicated    size=medium    alphaStorage=40
    ${endpoint}=    Collections.Get From Dictionary    ${data}    url
    ${deployment_endpoint}=    Catenate    SEPARATOR=    https://    ${endpoint}
    Get Deployment Health    ${Session_alias}    ${deployment_endpoint}    ${HEADER}
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    Set Suite Variable    ${deployment_id}
    Set Suite Variable    ${deployment_endpoint}
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    ${deployemnt_jwt_token}=    Collections.Get From Dictionary    ${data}    jwtToken
    Set Suite Variable    ${deployemnt_jwt_token}
    ${deployment_auth}=    Create Dictionary    x-auth-token=${deployemnt_jwt_token}    Content-Type=application/json
    Set Suite Variable    ${deployment_auth}

get deployment attribute data
    [Arguments]    ${deployment_details}    ${attribute}
    ${data}=    Collections.Get From Dictionary    ${deployment_details}    data
    ${deployments}=    Collections.Get From Dictionary    ${data}    getDeploymentByID
    ${attribute_data}=    Collections.Get From Dictionary    ${deployments}    ${attribute}
    [Return]    ${attribute_data}
