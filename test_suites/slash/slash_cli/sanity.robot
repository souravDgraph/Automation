*** Settings ***
Documentation     This is a simple test with Robot Framework
Suite Setup
Suite Teardown
Test Setup
Test Teardown
Default Tags      Sanity
Library           SlashAPI
Library           Collections
Variables         ../../../conf/slash/slash_cli/variables.py
Library           SlashCLI

*** Variables ***
${Environment}    Prod
${Backend_name}    Test

*** Test Cases ***
List Backends
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]    Create Backend
    ${deployments}=    SlashCLI.Get Deployments
    log    ${deployments}
    Should Contain    ${deployments}    ${deployment_id}
    [Teardown]    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    ${DELETE_DEPLOYMENT}

Create second backend for a non paid user
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]    Create Backend
    SlashCLI.Create Deployment    ${Environment}    ${Backend_name}    slash-graphql    ap-south-1    expected_output_text=${MAX_DEPLOYMENT_ERROR}    expected_return_code=2
    [Teardown]    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    ${DELETE_DEPLOYMENT}

Get Schema from a Deployment before adding schema
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]    Create Backend
    SlashCLI.Get Schema From Deployment    ${Environment}    ${deployment_id}    expected_output_text=${NO_SCHEMA_ERROR}    expected_return_code=1
    [Teardown]    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    ${DELETE_DEPLOYMENT}

Get Lambda from a Deployment before adding Lambda
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]    Create Backend
    Get Lambda    ${Environment}    ${deployment_id}
    [Teardown]    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    ${DELETE_DEPLOYMENT}

Delete a non existing deployment
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]    Create Backend
    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    ${DELETE_DEPLOYMENT}
    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    ${DELETE_DEPLOYMENT}    expected_return_code=2
    [Teardown]

Get Lambda of a non existing deployment
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]    Create Backend
    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    ${DELETE_DEPLOYMENT}
    Get Lambda    ${Environment}    ${deployment_id}
    Get Lambda    ${Environment}    ${deployment_id}
    [Teardown]

Get Schema of a non existing deployment
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]    Create Backend
    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    ${DELETE_DEPLOYMENT}
    SlashCLI.Get Schema From Deployment    ${Environment}    ${deployment_id}    expected_output_text=${No_BACKEND_ERROR}    expected_return_code=2
    [Teardown]

List backups on a newly created backend
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]    Create Backend
    List Backups    ${Environment}    ${deployment_id}    2
    [Teardown]    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    ${DELETE_DEPLOYMENT}

Create slash backend with dgraph cloud options
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]    Create Backend
    SlashCLI.Create Deployment    ${Environment}    ${Backend_name}    slash-graphql    ap-south-1    expected_output_text=${MAX_DEPLOYMENT_ERROR}    expected_return_code=2
    [Teardown]    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    ${DELETE_DEPLOYMENT}

List backups of a non existing backend
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]    Create Backend
    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    ${DELETE_DEPLOYMENT}
    List Backups    ${Environment}    ${deployment_id}    ${NO_BACKEND_ERROR}    2
    [Teardown]

Create a shared backend with ACL oprtion
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]
    SlashCLI.Create Deployment    ${Environment}    ${Backend_name}    slash-graphql    ap-south-1    acl=true    expected_output_text=${ACL_INVALID_INPUT_ERROR}    expected_return_code=2
    [Teardown]

Create a shared backend with HA oprtion
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]
    SlashCLI.Create Deployment    ${Environment}    ${Backend_name}    slash-graphql    ap-south-1    dgraphHA=true    expected_output_text=${HA_INVALID_INPUT_ERROR}    expected_return_code=2
    [Teardown]

Create a shared backend with jaeger oprtion
    [Documentation]    List of test cases covered
    ...    \ -> Create deployment
    ...    -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    [Setup]
    SlashCLI.Create Deployment    ${Environment}    ${Backend_name}    slash-graphql    ap-south-1    jaeger=true    expected_output_text=${JAEGER_INVALID_INPUT_ERROR}    expected_return_code=2
    [Teardown]

*** Keywords ***
Create Backend
    ${endpoint}=    SlashCLI.Create Deployment    ${Environment}    ${Backend_name}    slash-graphql    ap-south-1    expected_output_text=${DEPLOYMENT_LAUNCH_MESSAGE}
    ${deployment_id}=    Get Deployment Id With Endpoint    ${Environment}    ${endpoint}
    Set Suite Variable    ${deployment_id}
