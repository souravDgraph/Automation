*** Settings ***
Documentation     This is a simple test with Robot Framework
Suite Teardown
Test Setup        Create Session For Organization  ${HEADERS}    ${URL}
Test Teardown
Library           SlashAPI
Variables         ../../../conf/slash/slash_api/variables.py

*** Variables ***
${backend_name}     Pokemon
${user_email}       krishna+test1@dgraph.io
${org_name}     test 5

*** Test Cases ***
#Create Organization
#    #Create Organization    test7    200
#    ${res}=     Get Organizations List
#    log     ${res}

TC01 Create Organization and Manage organization for deployment
    [Documentation]  Test case to handle api functionality for organization
    [Tags]      regression
#    Remove Org From Deployment   Pokemon
    Add Org To Deployment   ${backend_name}     ${org_name}
    Add New Member To Existing Organization    ${org_name}    ${user_email}
    Remove Member From Existing Organization    ${org_name}    ${user_email}
    Add Org To Deployment   ${backend_name}     ${org_name}
    Remove Org From Deployment   ${backend_name}

TC_02 Check if member is already part of organization
    [Documentation]  Test case to check if memeber is already part of organization
    [Tags]      regression
    ${check}=   Check If Member Is Already Existing In Organization    ${org_name}    ${user_email}
    log     ${check}

