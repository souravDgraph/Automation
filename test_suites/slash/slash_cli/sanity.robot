*** Settings ***
Documentation     This is a simple test with Robot Framework
Suite Setup
Suite Teardown
Test Setup
Test Teardown
Default Tags      Sanity
Library           SlashAPI
Library           Collections
Variables         ../../../conf/slash/slash_api/variables.py
Library           SlashCLI

*** Variables ***
${Environment}    Prod
${Backend_name}    Test

*** Test Cases ***
Create , get and delete deployment
    [Documentation]    List of test cases covered
    ...     \ -> Create deployment
    ...     -> Delete Deployment
    ...    -> Delete Non existing Deploymnet
    ...    -> Get deployments
    ...    -> Get Deployment ID with endpoint
    ...    -> Get schema from a deployment (Negative case where schema is not added)
    SlashCLI.Get Deployments
    ${endpoint}=    SlashCLI.Create Deployment    ${Environment}    ${Backend_name}    ${BACKEND_ZONE}
    ${deployment_id}=    Get Deployment Id With Endpoint    ${Environment}    ${endpoint}
    SlashCLI.Get Schema From Deployment    ${Environment}    ${deployment_id}    1
    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}
    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}    expected_return_code=2
    SlashCLI.Get Schema From Deployment    ${Environment}    ${deployment_id}    expected_return_code=2

*** Keywords ***
