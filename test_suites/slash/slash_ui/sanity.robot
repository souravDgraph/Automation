*** Settings ***
Documentation     This Suite contains the sanity test cases for Slash UI
Suite Setup       Run Keywords     Setup     AND     Create Backend     
Suite Teardown    Run Keywords     Delete Backend    ${BACKEND_NAME}     AND    Close Browser    ${Browser_Alias}
Library           Slash
Variables         ../../../conf/slash/variables.py

*** Variables ***
${Browser_Alias}    Browser1
${API_key_name}     test
${card_number}     4242424242424242
${expiry_date}     424
${cvc}       242
${postal}      42424

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
    View Graphql Endpoint      ${Browser_Alias}      ${BACKEND_ZONE}.${CLOUD_PROVIDER}.stage.thegaas.com/graphql

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
    Click Launch New Backend      ${Browser_Alias}        20
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
    Delete Api Key      ${Browser_Alias}      ${API_key_name}

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
    [Teardown]     Create Backend

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

User should be able to add schema
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click Schema in menu
    ...    Switch to UI mode
    ...    Add type and Field
    ...    Change Field Name
    ...    Deploy Schema
    Click Schema In Menu     ${Browser_Alias}
    Click Switch To Ui Mode      ${Browser_Alias}
    Add Type     ${Browser_Alias}
    Change Type Name     ${Browser_Alias}      UntitledType0      User
    Add Field     ${Browser_Alias}       User
    Change Field Name      ${Browser_Alias}      User      untitledfield      name
    Deploy Schema      ${Browser_Alias}
    Click Switch To Text Mode     ${Browser_Alias}
    ${schema}=    Get Deployed Schema      ${Browser_Alias}
    Run Keyword If     '${schema}'!='${SCHEMA1}'    Fail

User should be able to edit and update schema
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click Schema in menu
    ...    Switch to UI mode
    ...    Add type and Field
    ...    Change Field Name and Type
    ...    Deploy Schema
    Click Overview In Menu    ${Browser_Alias}
    Click Schema In Menu     ${Browser_Alias}
    Click Switch To Ui Mode      ${Browser_Alias}
    Add Field     ${Browser_Alias}         User
    Change Field Name      ${Browser_Alias}      User      untitledfield      age
    Change Field Type       ${Browser_Alias}      User      age      String     Int
    Deploy Schema      ${Browser_Alias}
    Click Switch To Text Mode     ${Browser_Alias}
    ${schema}=    Get Deployed Schema      ${Browser_Alias}
    Run Keyword If     '${schema}'!='${SCHEMA2}'    Fail

Drop unused fields from Schema
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click Schema in menu
    ...    Switch to UI mode
    ...    Remove field
    ...    Deploy Schema
    ...    Select Unused field
    ...    Drop the unused field
    ...    Validate removed field
    Click Overview In Menu    ${Browser_Alias}
    Click Schema In Menu     ${Browser_Alias}
    Click Switch To Ui Mode      ${Browser_Alias}
    Remove Field      ${Browser_Alias}      User     age    
    Deploy Schema      ${Browser_Alias}
    Click Settings In Menu     ${Browser_Alias}
    Click Schema In Menu     ${Browser_Alias}
    Click Switch To Ui Mode      ${Browser_Alias}
    Click Drop Data Button     ${Browser_Alias}
    Select Unused Field      ${Browser_Alias}       User.age
    Click Drop Button      ${Browser_Alias}
    Check Dropped Field Is Not Visible      ${Browser_Alias}      User.age

Take Manual Backups
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click Settings in menu
    ...    Click backup tab
    ...    Click create backup button
    Click Settings In Menu      ${Browser_Alias}
    Click Backups Tab      ${Browser_Alias}
    ${date_time}=     Click Create Backup Button       ${Browser_Alias}
    Click General Tab      ${Browser_Alias}
    Click Backups Tab      ${Browser_Alias}
    Verify Backup Created     ${Browser_Alias}     incremental     ${date_time}

List Backups
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click Settings in menu
    ...    Click backup tab
    Click Settings In Menu      ${Browser_Alias}
    Click Backups Tab      ${Browser_Alias}
    ${is_backup_listed}=    Verify List Backups     ${Browser_Alias}
    Run Keyword If    '${is_backup_listed}'!='True'    Fail

Add Card And Verify Billing page
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click launch new button
    ...    fill backend details
    ...    click launch button
    ...    add card 
    ...    monitor backend
    ...    click avatar and billing button
    Click Launch New Backend      ${Browser_Alias}     20
    Fill Backend Details      ${Browser_Alias}      Shared       Slash GraphQL
    Click Launch Button      ${Browser_Alias}
    Add Card     ${Browser_Alias}       ${card_number}      ${expiry_date}      ${cvc}      ${postal}
    Monitor Backend Creation      ${Browser_Alias}     Shared     70
    Click Avatar    ${Browser_Alias}
    Click Billing Button     ${Browser_Alias}
    ${is_billing_info_correct}=    Verify Billing Information      ${Browser_Alias}     ${TOTAL_AMOUNT}     ${BILLING_DESCRIPTION}      ${BILLING_AMOUNT}
    Run Keyword If      '${is_billing_info_correct}'!='True'     Fail
    [Teardown]      Delete Backend       Shared

Cancel Subscription
    [Documentation]
    ...    List of tests covered
    ...
    ...    click avatar 
    ...    click billing button
    ...    cancel subscription
    Click Avatar    ${Browser_Alias}
    Click Billing Button     ${Browser_Alias}
    Cancel Subscription      ${Browser_Alias}

Should be able to run a mutation
    [Documentation]
    ...    List of tests covered
    ...
    ...    click api explorer
    ...    select query type
    ...    click add query type button
    ...    add value to field
    ...    click execure query button
    ...    remove query button
    Click Api Explorer In Menu      ${Browser_Alias}
    Select Query Type       ${Browser_Alias}        mutation
    Click Add Query Type Button        ${Browser_Alias}       mutation
    Expand Add Query        ${Browser_Alias}        add       User
    Add Value To Field        ${Browser_Alias}        name        santhosh
    Click Execute Query Button       ${Browser_Alias}
    Click Remove Query Button        ${Browser_Alias}       mutation
    Verify Query Data      ${QUERY_RESULT1}      User

Should be able to query and return response
    [Documentation]
    ...    List of tests covered
    ...
    ...    click api explorer
    ...    select query type
    ...    click add query type button
    ...    add value to field
    ...    click execure query button
    ...    remove query button
    Click Api Explorer In Menu      ${Browser_Alias}
    Select Query Type       ${Browser_Alias}        query
    Click Add Query Type Button        ${Browser_Alias}       query
    Expand Add Query        ${Browser_Alias}        query       User
    Select Search Fields     ${Browser_Alias}        ${FIELD_NAMES}
    Click Execute Query Button       ${Browser_Alias}
    Click Remove Query Button        ${Browser_Alias}       query
    Verify Query Data      ${QUERY_RESULT1}      User

Drop data from schema
    [Documentation]
    ...    List of tests covered
    ...
    ...    click api explorer
    ...    select query type
    ...    click add query type button
    ...    add value to field
    ...    click execure query button
    ...    remove query button
    ...    click schema and click drop data button
    ...    click drop all data button
    Click Api Explorer In Menu      ${Browser_Alias}
    Select Query Type       ${Browser_Alias}        mutation
    Click Add Query Type Button        ${Browser_Alias}       mutation
    Expand Add Query        ${Browser_Alias}        add       User
    Add Value To Field        ${Browser_Alias}        name        santhosh
    Click Execute Query Button       ${Browser_Alias}
    Click Remove Query Button        ${Browser_Alias}       mutation
    Click Schema In Menu     ${Browser_Alias}
    Click Drop Data Button      ${Browser_Alias}
    Click Drop All Data Button      ${Browser_Alias}
    Verify Query Data      ${QUERY_RESULT}      User

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    Login     ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}

Create Backend
    Click Launch New Backend      ${Browser_Alias}     20
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      ${BACKEND_NAME}     70

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
