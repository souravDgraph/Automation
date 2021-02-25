*** Settings ***
Documentation       Organization Test Cases for Slash CLI
Suite Setup         Create Organization And Set Organization Id
Suite Teardown
Test Setup
Test Teardown
Library             Collections
Variables           ../../../conf/slash/slash_api/variables.py
Library             SlashCLI

*** Variables ***
${Environment}    Prod
${org_name}       test6
${member_email}   krishna@dgraph.io

*** Test Cases ***
Get all Organizations
    [Documentation]     
    ...     List of Tests Covered
    ... 
    ...     Fetch all the organizations
    SlashCLI.Get Organizations      ${Environment}
    
Remove Member from Organization
    [Documentation]
    ...     List of Tests Covered
    ...
    ...     Add a member to that organization
    ...     Remove that member from that organization
    SlashCLI.Add Member To Organization     ${Environment}    ${org_uid}      ${member_email}
    SlashCLI.Remove Member From Organization      ${Environment}     ${org_uid}      ${member_email}

Remove Non Existing Member From Organization
    [Documentation]
    ...     List of Tests Covered
    ...
    ...     Add a member to that organization
    ...     Remove non existing member from that organization (Failure Case)
    SlashCLI.Add Member To Organization     ${Environment}     ${org_uid}      ${member_email}
    SlashCLI.Remove Member From Organization     ${Environment}    ${org_uid}      ${member_email}
    SlashCLI.Remove Member From Organization     ${Environment}    ${org_uid}     ${member_email}    2
    
Update Backend With Existing Organization
    [Documentation]
    ...     List of Tests Covered
    ...
    ...     Create a deployment with organization
    ...     Create another organization
    ...     Update deployment with organization name
    ${endpoint}=    SlashCLI.Create Deployment    ${Environment}    ${Backend_name}    ${BACKEND_ZONE}    ${org_uid}
    ${deployment_id}=    Get Deployment Id With Endpoint    ${Environment}    ${endpoint}
    SlashCLI.Create Organization     ${Environment}    test20
    ${org_uid}=     Get Organization Id     ${Environment}      test20
    SlashCLI.Update Deployment   ${Environment}     ${endpoint}     ${org_uid}
    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}

Add Non Existing Member To An Organization
    [Documentation]
    ...     List of Tests Covered
    ...     
    ...     Add Non Existing Member to Organization
    SlashCLI.Add Member To Organization     ${Environment}     ${org_uid}      santhosh+test1@dgraph.io     2

Add Already Present Member To An Organization
    [Documentation]
    ...     List of Tests Covered
    ...
    ...     Add already present member to an organization
    SlashCLI.Add Member To Organization     ${Environment}     ${org_uid}      santhosh@dgraph.io       2

*** Keywords ***
Create Organization And Set Organization Id
    SlashCLI.Create Organization     ${Environment}    ${org_name}
    ${org_uid}=     Get Organization Id     ${Environment}      ${org_name}
    Set Suite Variable    ${org_uid}