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
create Dgraph cloud deployment with default options
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

create Dgraph cloud deployment with HA
    [Documentation]    List of tests covered
    ...
    ...    - Create Dgraph cloud Deployment with HA enabled
    [Tags]    C236    Sanity
    [Template]
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    dedicated    true
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}    deploymentType=dedicated    size=medium    alphaStorage=40    dgraphHA=true
    ${backend_id}=    Collections.Get From Dictionary    ${data}    uid
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${backend_id}
    [Teardown]

create Dgraph cloud deployment with ACL enabled
    [Documentation]    List of tests covered
    ...
    ...    - Create Dgraph cloud Deploymentwith ACL enabled
    [Tags]    C236    Sanity
    [Template]
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    dedicated    true    aclEnabled=true
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}    deploymentType=dedicated    size=medium    alphaStorage=40    dgraphHA=true    aclEnabled=true
    ${backend_id}=    Collections.Get From Dictionary    ${data}    uid
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${backend_id}
    [Teardown]

create Dgraph cloud deployment with Jaeger enabled
    [Documentation]    List of tests covered
    ...
    ...    - Create Dgraph cloud Deployment with Jaeger enabled
    [Tags]    C236    Sanity
    [Template]
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    dedicated    jaegerEnabled=true
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}    deploymentType=dedicated    size=medium    alphaStorage=40    jaegerEnabled=true
    ${backend_id}=    Collections.Get From Dictionary    ${data}    uid
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${backend_id}
    [Teardown]

create Dgraph cloud deployment with Jaeger size and sampling time
    [Documentation]    List of tests covered
    ...
    ...    - Create Dgraph cloud Deployment with specified jaeger deployment options
    [Tags]    C236    Sanity
    [Template]
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    dedicated    jaegerEnabled=true    jaegerSize=1    jaegerTrace=0.02
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}    deploymentType=dedicated    size=medium    alphaStorage=40    jaegerEnabled=true    jaegerSize=1    jaegerTrace=0.02
    ${backend_id}=    Collections.Get From Dictionary    ${data}    uid
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${backend_id}
    [Teardown]

create Dgraph cloud deployment with defined storage
    [Documentation]    List of tests covered
    ...
    ...    - Create Dgraph cloud Deployment with user defined storage
    [Tags]    C236    Sanity
    [Template]
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    dedicated    alphaStorage=80
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}    deploymentType=dedicated    size=medium    alphaStorage=80
    ${backend_id}=    Collections.Get From Dictionary    ${data}    uid
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${backend_id}
    [Teardown]

create Dgraph cloud deployment with different backend tier
    [Documentation]    List of tests covered
    ...
    ...    - Create Dgraph cloud Deployment by picking a non default backend tire
    [Tags]    C236    Sanity
    [Template]
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    dedicated    size=large    alphaStorage=40
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}    deploymentType=dedicated    size=large    alphaStorage=40
    ${backend_id}=    Collections.Get From Dictionary    ${data}    uid
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${backend_id}
    [Teardown]

create Dgraph cloud deployment with Jaeger size and default deployment values
    [Documentation]    List of tests covered
    ...
    ...    - Create Dgraph cloud Deployment with non default Jeager deployment size
    [Tags]    C236    Sanity
    [Template]
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    dedicated    jaegerEnabled=true
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}    deploymentType=dedicated    size=medium    alphaStorage=40    jaegerEnabled=true
    ${backend_id}=    Collections.Get From Dictionary    ${data}    uid
    Delete Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${backend_id}
    [Teardown]

create Dgraph cloud deployment with all options enabled
    [Documentation]    List of tests covered
    ...
    ...    - Create Dgraph cloud Deployment with all the options enabled
    [Tags]    C236    Sanity
    [Template]
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    dedicated    size=large    alphaStorage=90    dgraphHA=true    aclEnabled=true    jaegerEnabled=true    jaegerSize=1    jaegerTrace=0.02
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}    deploymentType=dedicated    size=large    alphaStorage=90    dgraphHA=true    aclEnabled=true    jaegerEnabled=true    jaegerSize=1    jaegerTrace=0.02
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
    ...    - Update dgraph cloud deployment ACL
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
    ...    - Update dgraph cloud deployment size
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
    ...    - Update dgraph cloud deployment mode
    [Tags]    C236    Sanity
    [Template]
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    deploymentMode=readonly
    ${deployment_details}=    Get Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    ${deployment_mode}=    get deployment attribute data    ${deployment_details}    deploymentMode
    Should Be Equal    ${deployment_mode}    readonly
    [Teardown]

Update Enable jaeger with deployment options
    [Documentation]    List of tests covered
    ...
    ...    - Update dgraph cloud deployment jaeger with options
    [Tags]    C236    Sanity
    [Template]
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    jaegerEnabled=true    jaegerSize=1    jaegerTrace=0.02
    ${deployment_details}=    Get Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    ${jaeger_size}=    get deployment attribute data    ${deployment_details}    jaegerSize
    ${jaeger_size}=    Convert To String    ${jaeger_size}
    Should Be Equal    ${jaeger_size}    1
    ${jaeger_trace}=    get deployment attribute data    ${deployment_details}    jaegerTrace
    ${jaeger_trace}=    Convert To String    ${jaeger_trace}
    Should Be Equal    ${jaeger_trace}    0.02
    [Teardown]

create Enable jaeger deployment and modified deployment options
    [Documentation]    List of tests covered
    ...
    ...    - Create dgraph cloud deployment with jaeger enabled and modify the jaeger depolyment options
    [Tags]    C236    Sanity
    [Template]
    ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${BACKEND_NAME}    ${BACKEND_ZONE}    dedicated    jaegerEnabled=true    jaegerSize=1    jaegerTrace=0.02
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}    deploymentType=dedicated    size=medium    alphaStorage=40    jaegerEnabled=true
    Update Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}    jaegerSize=0.5    jaegerTrace=0.01
    ${deployment_details}=    Get Deployment    ${Session_alias}    ${URL}    ${HEADER}    ${deployment_id}
    ${jaeger_size}=    get deployment attribute data    ${deployment_details}    jaegerSize
    ${jaeger_size}=    Convert To String    ${jaeger_size}
    Should Be Equal    ${jaeger_size}    0.5
    ${jaeger_trace}=    get deployment attribute data    ${deployment_details}    jaegerTrace
    ${jaeger_trace}=    Convert To String    ${jaeger_trace}
    Should Be Equal    ${jaeger_trace}    0.01
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
