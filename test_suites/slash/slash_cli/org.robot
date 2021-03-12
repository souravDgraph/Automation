*** Settings ***
Documentation       Organization Test Cases for Slash CLI
Suite Setup         Create Organization And Set Organization Id
Suite Teardown
Test Setup
Test Teardown
Library             Collections
Variables           ../../../conf/slash/slash_cli/variables.py
Library             SlashCLI

*** Variables ***
${Environment}    Prod
${org_name}       dgraph
${Backend_name}    test
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
    SlashCLI.Add Member To Organization     ${Environment}    ${org_uid}      ${member_email}     User ${member_email} successfully added to ${org_uid} organization.
    SlashCLI.Remove Member From Organization      ${Environment}     ${org_uid}      ${member_email}     Member ${member_email} successfully removed from ${org_name} organization.

Remove Non Existing Member From Organization
    [Documentation]
    ...     List of Tests Covered
    ...
    ...     Add a member to that organization
    ...     Remove non existing member from that organization (Failure Case)
    SlashCLI.Add Member To Organization     ${Environment}     ${org_uid}      ${member_email}       User ${member_email} successfully added to ${org_uid} organization.
    SlashCLI.Remove Member From Organization     ${Environment}    ${org_uid}      ${member_email}      Member ${member_email} successfully removed from ${org_name} organization.
    SlashCLI.Remove Member From Organization     ${Environment}    ${org_uid}     ${member_email}    ${USER_NOT_PRESENT_ERROR}      2
    
Update Backend With Existing Organization
    [Documentation]
    ...     List of Tests Covered
    ...
    ...     Create a deployment with organization
    ...     Create another organization
    ...     Update deployment with organization name
    ${endpoint}=    SlashCLI.Create Deployment    ${Environment}    ${Backend_name}    region=ap-south-1    organizationId=${org_uid}      expected_output_text=${DEPLOYMENT_LAUNCH_MESSAGE}
    ${deployment_id}=    Get Deployment Id With Endpoint    ${Environment}    ${endpoint}
    ${organization_list}=     SlashCLI.Get Organizations      ${Environment}
    SlashCLI.Create Organization     ${Environment}    ${org_name}      Organization ${org_name} created successfully.
    ${org_uid}=      Get Organization Id     ${Environment}     ${organization_list}
    SlashCLI.Update Deployment   ${Environment}     ${endpoint}     ${Backend_name}     organizationId=${org_uid}      expected_output_text=${UPDATE_DEPLOYMENT}
    SlashCLI.Delete Deployment    ${Environment}    ${deployment_id}       expected_output_text=${DELETE_DEPLOYMENT}

Add Non Existing Member To An Organization
    [Documentation]
    ...     List of Tests Covered
    ...     
    ...     Add Non Existing Member to Organization
    SlashCLI.Add Member To Organization     ${Environment}     ${org_uid}      santhosh+test1@dgraph.io     ${NO_USER_EXIST_ERROR}     2

Add Already Present Member To An Organization
    [Documentation]
    ...     List of Tests Covered
    ...
    ...     Add already present member to an organization
    SlashCLI.Add Member To Organization     ${Environment}     ${org_uid}      santhosh@dgraph.io      ${EXISTING_USER_ERROR}     2

Create Deployment With Non-Existing Organization
   [Documentation]
    ...     List of Tests Covered
    ...
    ...     Create a deployment with non-existing organization
    SlashCLI.Create Deployment    ${Environment}    ${Backend_name}    region=ap-south-1    organizationId=0x20000      expected_output_text=${NON_EXISTING_ORGANIZATION_ERROR}      expected_return_code=2

Add Member To Non-Existing Organization
    [Documentation]
    ...    List of Tests Covered
    ...
    ...    Add member to non-existing organization
    SlashCLI.Add Member To Organization     ${Environment}     0x20000      ${member_email}       ${NO_ORGANIZATION_ERROR}      expected_return_code=2

Remove Member To Non-Existing Organization
    [Documentation]
    ...    List of Tests Covered
    ...
    ...    Remove member from non-existing organization
    SlashCLI.Remove Member From Organization     ${Environment}    0x20000      ${member_email}      ${NO_ORGANIZATION_ERROR}      expected_return_code=2

*** Keywords ***
Create Organization And Set Organization Id
    ${organization_list}=     SlashCLI.Get Organizations      ${Environment}
    SlashCLI.Create Organization     ${Environment}    ${org_name}      Organization ${org_name} created successfully.
    ${org_uid}=      Get Organization Id     ${Environment}     ${organization_list}
    Set Suite Variable    ${org_uid}