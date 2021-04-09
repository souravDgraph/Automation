*** Settings ***
Documentation     This suite contains the super admin test cases for Slash UI
Suite Setup       Run Keywords     Setup     AND     Create Backend
Suite Teardown    Run Keywords     Delete Backend     AND    Close Browser    ${Browser_Alias}
Library           Slash
Variables         ../../../conf/slash/variables.py

*** Variables ***
${Browser_Alias}    Browser1
${API_key_name}     test
${Invalid_User_Email}      user@gmail.com

*** Test Cases ***
Validate Default Super Admin Landing Page
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click Super Admin item 
    ...    Validate the search deployment input fields
    Click Super Admin In Menu      ${Browser_Alias}
    Validate Search Deployment Fields      ${Browser_Alias}      ${SEARCH_DEPLOYMENT_FIELDS}
    Click Settings In Menu      ${Browser_Alias}

Search Deployment with user email
    [Documentation]
    ...    List of tests covered
    ...
    ...    Click Super Admin item 
    ...    Search Deployment with user email
    ...    validate the deployment details
    ...    search deployment with invalid user email
    ...    validate the response
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Validate Deployment Detail Labels     ${Browser_Alias}      ${DEPLOYMENT_LABELS}      ${BACKEND_NAME}
    Validate Deployment Detail Links     ${Browser_Alias}       ${DEPLOYMENT_LINKS}      ${BACKEND_NAME}
    Search Deployment     ${Browser_Alias}     User Email     ${Invalid_User_Email}
    Validate Response For Invalid Search     ${Browser_Alias}
    Click Settings In Menu      ${Browser_Alias}

Validate tooltip message for Dgraph Lambda Script Field
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Deployment Field Tooltip Message      ${Browser_Alias}      Dgraph Lambda Script      Dgraph Lambda is a serverless platform for running JS on Slash GraphQL (or Dgraph).

Validate tooltip message for Do Not Freeze Field
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Deployment Field Tooltip Message      ${Browser_Alias}         Do Not Freeze         Defaults to False. Set this to True to the prevent the cluster from freezing due to inactivity.
    Validate Deployment Field Values       ${Browser_Alias}          Do Not Freeze        ${VALUES}        

Validate tooltip message for Dgraph HA
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Deployment Field Tooltip Message      ${Browser_Alias}       Dgraph HA         Defaults to False. Set this to True for dgraph HA. (Note: You cannot go from HA to non-HA)
    Validate Deployment Field Values       ${Browser_Alias}          Dgraph HA        ${VALUES}        

Validate tooltip message for Deployment Mode
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Deployment Field Tooltip Message      ${Browser_Alias}       Deployment Mode       Defaults to GraphQL
    Validate Deployment Field Values       ${Browser_Alias}          Deployment Mode        ${DEPLOYMENT_MODE_VALUES}        https://dgraph.io/docs/slash-graphql/admin/backend-modes/

Validate tooltip message for Deployment Size
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Deployment Field Tooltip Message      ${Browser_Alias}       Deployment Size        Defaults to Small
    Validate Deployment Field Values       ${Browser_Alias}          Deployment Size        ${DEPLOYMENT_SIZE_VALUES}        https://discuss.dgraph.io/t/slash-deployment-sizing/10635

Validate tooltip message for Backup Interval
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Deployment Field Tooltip Message      ${Browser_Alias}       Backup Interval       Defaults to 4 hours. Backend data backup frequency
    Validate Deployment Field Values       ${Browser_Alias}           Backup Interval        4h         https://godoc.org/github.com/robfig/cron

Validate tooltip message for Backup Bucket Format
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Deployment Field Tooltip Message      ${Browser_Alias}       Backup Bucket Format       Defaults to '%Y-%U'. Backup bucket folder name and full backup frequency. Every folder will result in a full backup.
    Validate Deployment Field Values       ${Browser_Alias}        Backup Bucket Format        %Y-%U        http://www.strfti.me/

Validate tooltip message for Enable Jaeger Tracing
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Deployment Field Tooltip Message      ${Browser_Alias}        Enable Jaeger Tracing       Enabled Jaeger Tracing
    Validate Deployment Field Values       ${Browser_Alias}          Enable Jaeger Tracing        ${VALUES}        

Validate fields that have alert message needs to be present
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Fields Alert Message     ${Browser_Alias}       ${DEPLOYMENT_FIELDS}

Validate Default values needs to be present
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Default Value Present For Fields      ${Browser_Alias}       ${DEPLOYMENT_FIELDS_VALUES_DICT}     ${BACKEND_NAME}

Validate edit deployment details UI
    [Documentation]
    ...    List of tests covered
    ...
    Search Deployment And Modify       Do Not Freeze        False       True
    Click Update Button      ${Browser_Alias}
    Validate Alert        ${Browser_Alias}       Successfully Updated the backend
    Click Back Button     ${Browser_Alias}
    Search Deployment And Modify       Do Not Freeze        True       False
    Click Update Button      ${Browser_Alias}
    Validate Alert        ${Browser_Alias}       Successfully Updated the backend

Validate Enabling Jaeger Tracing Field
    [Documentation]
    ...    List of tests covered
    ...
    Search Deployment And Modify       Enable Jaeger Tracing        False       True
    Click Update Button      ${Browser_Alias}
    Validate Alert        ${Browser_Alias}       Successfully Updated the backend
    Click Back Button     ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Deployment Field Value     ${Browser_Alias}       Enable Jaeger Tracing      True

Validate Enabling Dgraph HA Field
    [Documentation]
    ...    List of tests covered
    ...
    Search Deployment And Modify       Dgraph HA        False       True
    Click Update Button      ${Browser_Alias}
    Validate Alert        ${Browser_Alias}       Successfully Updated the backend
    Click Back Button     ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Deployment Field Value     ${Browser_Alias}       Dgraph HA      True

Validate Protect Deployment
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Click Protect Button      ${Browser_Alias}
    Validate Alert        ${Browser_Alias}       Deployment has been updated
    Click Update Button For Protect Deployment     ${Browser_Alias}
    Validate Alert        ${Browser_Alias}       Something went wrong
    Click Back Button     ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Unprotect Button Present      ${Browser_Alias}
    Click Unprotect Button      ${Browser_Alias}
    Validate Alert        ${Browser_Alias}       Deployment has been updated

Validate Unprotect Deployment
    [Documentation]
    ...    List of tests covered
    ...
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Click Protect Button      ${Browser_Alias}
    Validate Alert        ${Browser_Alias}       Deployment has been updated
    Click Update Button For Protect Deployment     ${Browser_Alias}
    Validate Alert        ${Browser_Alias}       Something went wrong
    Click Back Button     ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Unprotect Button Present      ${Browser_Alias}
    Click Unprotect Button      ${Browser_Alias}
    Validate Alert        ${Browser_Alias}       Deployment has been updated
    Change Deployment Field Value      ${Browser_Alias}      Do Not Freeze      False      True
    Click Update Button      ${Browser_Alias}
    Validate Alert        ${Browser_Alias}       Successfully Updated the backend
    Check Do Not Freeze Value      ${Browser_Alias}      True

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}

Create Backend
    Click Launch New Backend      ${Browser_Alias}     20
    Fill Backend Details      ${Browser_Alias}      ${BACKEND_NAME}
    Click Launch Button      ${Browser_Alias}
    Monitor Backend Creation      ${Browser_Alias}      70

Delete Backend
    Click Settings In Menu      ${Browser_Alias}
    Click General Tab      ${Browser_Alias}
    Delete Deployment     ${Browser_Alias}     ${BACKEND_NAME}
    Check Deployment Is Deleted     ${Browser_Alias}     ${BACKEND_NAME}
    
Search Deployment And Modify
    [Arguments]    ${deployment_field_name}        ${old_value}      ${new_value}
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Deployment Field Value     ${Browser_Alias}       ${deployment_field_name}      ${old_value}
    Change Deployment Field Value      ${Browser_Alias}      ${deployment_field_name}      ${old_value}      ${new_value}
