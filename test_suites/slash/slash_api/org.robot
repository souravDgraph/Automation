*** Settings ***
Documentation     This is a simple test with Robot Framework
Suite Teardown
Test Setup        Create Session For Organization  ${HEADERS}    ${URL}
Test Teardown
Library           SlashAPI
Variables         ../../../conf/slash/slash_api/variables.py

*** Variables ***

*** Test Cases ***
#Create Organization
#    #Create Organization    test7    200
#    ${res}=     Get Organizations List
#    log     ${res}

Test Case to Manage Organization
#    Remove Org From Deployment   Pokemon
    Add Org To Deployment   Pokemon     test 5
    Add New Member To Existing Organization    test 5    krishna+test1@dgraph.io
    Remove Member From Existing Organization    test 5    krishna+test1@dgraph.io
    Add Org To Deployment   Pokemon     test6
    Remove Org From Deployment   Pokemon


