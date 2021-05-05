*** Settings ***
Documentation     This Suite contains the sanity test cases for Slash UI
Suite Setup       Run Keywords     Setup     AND     Create Backend      ${BACKEND_NAME}     Starter     AND      Add And Deploy Schema     ${type_name}     ${field_name}      ${SCHEMA1}     AND      Create Organization    Labs
Suite Teardown    Run Keywords     Delete Backend     ${BACKEND_NAME}     AND    Close Browser    ${Browser_Alias}
Library           Slash
Variables         ../../../conf/slash/variables.py

*** Variables ***
${Browser_Alias}    Browser1
${API_key_name}     test
${card_number}     4242424242424242
${invalid_card_number}     4242424242424241
${expiry_date}     424
${cvc}       242
${postal}      42424
${type_name}     User
${field_name}       name

*** Test Cases ***
User should be able to create backend and navigate to schema page
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the schema for the backend
    Click Schema In Menu     ${Browser_Alias}

User should be able to navigate to API Explorer
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the api explorer for the backend
    Click Api Explorer In Menu      ${Browser_Alias}

User should be able to navigate to Settings tab
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the settings for the backend
    Click Settings In Menu      ${Browser_Alias}

User should be able to view the graphql endpoint in Overview
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the overview for the backend
    ...    View the graphql endpoint
    Click Overview In Menu       ${Browser_Alias}
    View Graphql Endpoint      ${Browser_Alias}      ${BACKEND_ZONE}.aws.stage.thegaas.com/graphql

User should be able to view the location of the deployment
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the overview for the backend
    ...    View the location
    Click Overview In Menu       ${Browser_Alias}
    View Deployment Zone      ${Browser_Alias}       ${BACKEND_ZONE}
    
User should not be able to create more than one backend
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the launch new backend button
    ...    Check the starter product is disabled
    Click Launch New Backend      ${Browser_Alias}
    Check Starter Product Disabled       ${Browser_Alias}

User should be able to add new API key
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the settings for the backend
    ...    Click the api key tab
    ...    Create new api key
    ...    Verify api key generated
    Click Settings In Menu      ${Browser_Alias}
    Click Api Key Tab      ${Browser_Alias}
    Create New Api Key      ${Browser_Alias}       ${API_key_name}
    Verify Api Key Generated     ${Browser_Alias}     ${API_key_name}

User should be able to delete API Key
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the settings for the backend
    ...    Click the api key tab and create new api key
    ...    Verify Api key generated
    ...    Delete the API key
    Click Settings In Menu      ${Browser_Alias}
    Click Api Key Tab      ${Browser_Alias}
    Create New Api Key      ${Browser_Alias}       ${API_key_name}
    Verify Api Key Generated     ${Browser_Alias}     ${API_key_name}
    Delete Api Key      ${Browser_Alias}      ${API_key_name}

User should be able to delete a backend
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the settings for the backend
    ...    Click the general tab
    ...    Delete the deployment
    ...    Check the deployment is deleted
    Click Settings In Menu      ${Browser_Alias}
    Click General Tab      ${Browser_Alias}
    Delete Deployment     ${Browser_Alias}     ${BACKEND_NAME}
    Check Deployment Is Deleted     ${Browser_Alias}     ${BACKEND_NAME}
    [Teardown]     Create Backend        ${BACKEND_NAME}        Starter

User should be able signout from the logout button in the header
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the avatar button
    ...    Click logout button
    Click Avatar    ${Browser_Alias}
    Click Logout Button    ${Browser_Alias}
    [Teardown]     Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}

User should be able to view the documentation
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click the documentation for the backend
    Click Documentation In Menu     ${Browser_Alias}

Toggle between the deployments make sure all the fields show correct values
    [Documentation]
    ...    List of tests covered
    ...   
    ...
    Create Backend       Test      Shared  
    Click Overview In Menu      ${Browser_Alias}
    Verify Backend Details      ${Browser_Alias}        ${BACKEND_ZONE}.aws.stage.thegaas.com/graphql       Shared       ${BACKEND_ZONE}      25 GB        Test  
    Change Backend     ${Browser_Alias}      Test       Test Backend
    Verify Backend Details      ${Browser_Alias}        ${BACKEND_ZONE}.aws.stage.thegaas.com/graphql       Starter       ${BACKEND_ZONE}      25 GB        Test Backend
    Change Backend     ${Browser_Alias}      Test Backend       Test
    [Teardown]      Delete Backend      Test 

Clone Back-end and data should be duplicated on a new deployment
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Avatar      ${Browser_Alias}
    Click Billing Button      ${Browser_Alias}
    ${has_active_subscription}=       Run Keyword And Return Status      Has Active Subscription      ${Browser_Alias}
    log      ${has_active_subscription}
    Click Settings In Menu      ${Browser_Alias}
    Click Clone Backend       ${Browser_Alias}
    Fill Clone Backend Details       ${Browser_Alias}      Test Clone      Shared      
    Click Clone Button       ${Browser_Alias}
    Run Keyword If      '${has_active_subscription}'=='False'      Add Card      ${Browser_Alias}      ${card_number}      ${expiry_date}      ${cvc}      ${postal}
    Monitor Backend Creation      ${Browser_Alias}      Test Clone      70
    Verify Backend Details      ${Browser_Alias}        ${BACKEND_ZONE}.aws.stage.thegaas.com/graphql       Shared       ${BACKEND_ZONE}      25 GB        Test Clone
    Click Schema In Menu     ${Browser_Alias}
    ${schema}=    Get Deployed Schema      ${Browser_Alias}
    Run Keyword If     '${schema}'!='${SCHEMA1}'    Fail
    Verify Query Data      ${QUERY_RESULT2}      User
    [Teardown]      Delete Backend        Test Clone

Clone Back-end with organization and data should be duplicated on a new deployment
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Avatar      ${Browser_Alias}
    Click Billing Button      ${Browser_Alias}
    ${has_active_subscription}=       Run Keyword And Return Status      Has Active Subscription      ${Browser_Alias}
    Click Settings In Menu      ${Browser_Alias}
    Update Backend Organization      ${Browser_Alias}      Lab
    Click Clone Backend       ${Browser_Alias}
    Fill Clone Backend Details       ${Browser_Alias}      Test Clone      Shared      
    Click Clone Button       ${Browser_Alias}
    Run Keyword If      '${has_active_subscription}'=='False'      Add Card      ${Browser_Alias}      ${card_number}      ${expiry_date}      ${cvc}      ${postal}
    Monitor Backend Creation      ${Browser_Alias}      Test Clone      70
    Verify Backend Details      ${Browser_Alias}        ${BACKEND_ZONE}.aws.stage.thegaas.com/graphql       Shared       ${BACKEND_ZONE}      25 GB        Lab / Test Clone
    Click Schema In Menu     ${Browser_Alias}
    ${schema}=    Get Deployed Schema      ${Browser_Alias}
    Run Keyword If     '${schema}'!='${SCHEMA1}'    Fail
    Verify Query Data      ${QUERY_RESULT2}      User
    Delete Backend       Test Clone
    Click Schema In Menu     ${Browser_Alias}
    Remove Backend Organization      ${Browser_Alias}    

Clone Back-end with another organization and data should be duplicated on a new deployment
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Avatar      ${Browser_Alias}
    Click Billing Button      ${Browser_Alias}
    ${has_active_subscription}=       Run Keyword And Return Status      Has Active Subscription      ${Browser_Alias}
    Create Organization      Test
    Click Settings In Menu      ${Browser_Alias}
    Update Backend Organization      ${Browser_Alias}      Lab
    Click Clone Backend       ${Browser_Alias}
    Fill Clone Backend Details       ${Browser_Alias}      Test Clone      Shared      organization=Test
    Click Clone Button       ${Browser_Alias}
    Run Keyword If      '${has_active_subscription}'=='False'      Add Card      ${Browser_Alias}      ${card_number}      ${expiry_date}      ${cvc}      ${postal}
    Monitor Backend Creation      ${Browser_Alias}      Test Clone     70
    Verify Backend Details      ${Browser_Alias}        ${BACKEND_ZONE}.aws.stage.thegaas.com/graphql       Shared       ${BACKEND_ZONE}      25 GB        Test / Test Clone
    Click Schema In Menu     ${Browser_Alias}
    ${schema}=    Get Deployed Schema      ${Browser_Alias}
    Run Keyword If     '${schema}'!='${SCHEMA1}'    Fail
    Verify Query Data      ${QUERY_RESULT2}      User
    Delete Backend        Test Clone
    Click Settings In Menu     ${Browser_Alias}
    Remove Backend Organization      ${Browser_Alias}    

Should be able to define authorisation in the schema
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Schema In Menu      ${Browser_Alias}
    Click Switch To Ui Mode      ${Browser_Alias}
    Change Field Name      ${Browser_Alias}      User      id      username
    Add Type     ${Browser_Alias}
    Change Type Name     ${Browser_Alias}      UntitledType0      Task
    Add Field     ${Browser_Alias}       Task
    Change Field Name      ${Browser_Alias}      Task      untitledfield      title
    Add Field     ${Browser_Alias}       Task
    Change Field Name      ${Browser_Alias}      Task      untitledfield      user
    Change Field Type       ${Browser_Alias}      Task      user      String     User
    Select Type    ${Browser_Alias}        Task
    Click Add Rules Button      ${Browser_Alias}
    Add Rules      ${Browser_Alias}       Query       ${RULES}
    Click Update Button     ${Browser_Alias}
    Click Switch To Text Mode      ${Browser_Alias}
    ${is_schema_deployed}=     Deploy Schema      ${Browser_Alias}       ${SCHEMA3}
    Run Keyword If      '${is_schema_deployed}'!='True'     Fail
    ${schema}=    Get Deployed Schema      ${Browser_Alias}
    Run Keyword If     '${schema}'!='${SCHEMA3}'    Fail

Add payment details - Negative
    [Documentation]
    ...    List of tests covered
    ...
    ...
    Click Avatar      ${Browser_Alias}
    Click Billing Button      ${Browser_Alias}
    ${has_active_subscription}=       Run Keyword And Return Status      Has Active Subscription      ${Browser_Alias}
    Run Keyword If      '${has_active_subscription}'=='True'      Cancel Subscription      ${Browser_Alias}
    Click Launch New Backend      ${Browser_Alias}     20
    Fill Backend Details      ${Browser_Alias}      Test       Shared
    Click Launch Button      ${Browser_Alias}
    Add Invalid Card     ${Browser_Alias}       ${invalid_card_number}

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}

Create Backend
    [Arguments]       ${backend_name}      ${instance_type}
    Click Avatar      ${Browser_Alias}
    Click Billing Button      ${Browser_Alias}
    ${has_active_subscription}=       Run Keyword And Return Status      Has Active Subscription      ${Browser_Alias}
    Click Launch New Backend      ${Browser_Alias}     20
    Fill Backend Details      ${Browser_Alias}      ${backend_name}      ${instance_type}
    Click Launch Button      ${Browser_Alias}
    Run Keyword If      '${has_active_subscription}'=='False' and '${instance_type}'!='Starter'    Add Card      ${Browser_Alias}      ${card_number}      ${expiry_date}      ${cvc}      ${postal}
    Monitor Backend Creation      ${Browser_Alias}       ${backend_name}      70

Delete Backend
    [Arguments]       ${backend_name}
    Click Settings In Menu      ${Browser_Alias}
    Click General Tab      ${Browser_Alias}
    Delete Deployment     ${Browser_Alias}     ${backend_name}
    Check Deployment Is Deleted     ${Browser_Alias}     ${backend_name}

Verify Query Data
    [Arguments]      ${query_result}       ${type_name}
    Click Api Explorer In Menu      ${Browser_Alias}
    Select Query Type       ${Browser_Alias}        query
    Click Add Query Type Button        ${Browser_Alias}       query
    Expand Add Query        ${Browser_Alias}        query       ${type_name}
    Select Search Fields     ${Browser_Alias}        ${FIELD_NAMES}
    Click Execute Query Button       ${Browser_Alias}
    ${data}=    Get Query Result     ${Browser_Alias}
    Run Keyword If     ${data}!=${query_result}    Fail
    Click Remove Query Button        ${Browser_Alias}       query

Add And Deploy Schema
    [Arguments]      ${type_name}       ${field_name}      ${SCHEMA1} 
    Click Schema In Menu     ${Browser_Alias}
    Click Switch To Ui Mode      ${Browser_Alias}
    Add Type     ${Browser_Alias}
    Change Type Name     ${Browser_Alias}      UntitledType0      ${type_name}
    Add Field     ${Browser_Alias}       ${type_name}
    Change Field Name      ${Browser_Alias}      ${type_name}      untitledfield      ${field_name}
    Click Switch To Text Mode      ${Browser_Alias}
    ${is_schema_deployed}=     Deploy Schema      ${Browser_Alias}       ${SCHEMA1}
    Run Keyword If      '${is_schema_deployed}'!='True'     Fail
    ${schema}=    Get Deployed Schema      ${Browser_Alias}
    Run Keyword If     '${schema}'!='${SCHEMA1}'    Fail

Create Organization
    [Arguments]      ${org_name}
    Click Avatar      ${Browser_Alias}
    Click Organization Button      ${Browser_Alias}
    Click Create Organization Button      ${Browser_Alias}
    Add Organization        ${Browser_Alias}      ${org_name}
