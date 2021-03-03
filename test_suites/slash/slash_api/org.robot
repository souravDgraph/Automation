*** Settings ***
Documentation     This is a simple test with Robot Framework
Suite Teardown
Test Setup        Run Keywords    Create Session For Organization  ${HEADERS}    ${URL}    AND    Create Organization And Fetch Organization Id
Test Teardown
Library           SlashAPI
Variables         ../../../conf/slash/slash_api/variables.py

*** Variables ***
${backend_name}     Pokemon
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
#    Remove Org From Deployment   Pokemon
    Add Org To Deployment   ${backend_name}     ${org_uid}
    Add New Member To Existing Organization    ${org_uid}    ${user_email}
    Remove Member From Existing Organization    ${org_uid}    ${user_email}
    Add Org To Deployment   ${backend_name}     ${org_uid}
    Remove Org From Deployment   ${backend_name}

TC_02 Check if member is already part of organization
    [Documentation]  Test case to check if memeber is already part of organization
    [Tags]      regression
    ${check}=   Check If Member Is Already Existing In Organization    ${org_uid}    ${user_email}
    log     ${check}

*** Keywords ***
Create Organization And Fetch Organization Id
 	${org_details}=		Create Organization	   ${org_name}
 	log 	${org_details}
 	${details}=    Collections.Get From Dictionary    ${org_details}    data
    ${organization}=    Collections.Get From Dictionary    ${details}    createOrganization
    ${org_uid}=    Collections.Get From Dictionary    ${organization}    uid
 	Set Suite Variable		${org_uid}