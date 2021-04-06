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
    Validate Search Deployment Fields      ${Browser_Alias}
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
    Validate Deployment Detail Labels     ${Browser_Alias}      ${BACKEND_NAME}
    Validate Deployment Detail Links     ${Browser_Alias}       ${BACKEND_NAME}
    Search Deployment     ${Browser_Alias}     User Email     ${Invalid_User_Email}
    Validate Response For Invalid Search     ${Browser_Alias}
    Click Settings In Menu      ${Browser_Alias}

Validate tooltip message for Dgraph Lambda Script Field
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Dgraph Lambda Script Field Tooltip Message      ${Browser_Alias}

Validate tooltip message for Do Not Freeze Field
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Do Not Freeze Field Tooltip Message       ${Browser_Alias}
    Validate Do Not Freeze Field Values       ${Browser_Alias}

Validate tooltip message for Dgraph HA
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Dgraph Ha Field Tooltip Message      ${Browser_Alias}
    Validate Dgraph Ha Field Values      ${Browser_Alias}

Validate tooltip message for Deployment Mode
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Deployment Mode Field Tooltip Message      ${Browser_Alias}
    Validate Deployment Mode Field Values       ${Browser_Alias}

Validate tooltip message for Deployment Size
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Deployment Size Field Tooltip Message      ${Browser_Alias}
    Validate Deployment Size Field Values      ${Browser_Alias}

Validate tooltip message for Backup Interval
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Backup Interval Field Tooltip Message      ${Browser_Alias}
    Validate Backup Interval Field Values       ${Browser_Alias}

Validate tooltip message for Backup Bucket Format
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Backup Bucket Format Field Tooltip Message      ${Browser_Alias}
    Validate Backup Bucket Format Field Values      ${Browser_Alias}

Validate tooltip message for Enable Jaeger Tracing
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Jaeger Tracing Field Tooltip Message      ${Browser_Alias}
    Validate Jaeger Tracing Field Values       ${Browser_Alias}

Validate fields that have alert message needs to be present
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Validate Fields Alert Message     ${Browser_Alias}

Validate Default values needs to be present
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Default Value Present For Fields       ${Browser_Alias}     ${BACKEND_NAME}

Validate edit deployment details UI
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Change Do Not Freeze Field      ${Browser_Alias}      False      True
    Click Update Button      ${Browser_Alias}
    Click Back Button     ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Do Not Freeze Value      ${Browser_Alias}      True
    Change Do Not Freeze Field      ${Browser_Alias}      True      False
    Click Update Button      ${Browser_Alias}

Validate Enabling Jaeger Tracing Field
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Change Jaeger Tracing Field       ${Browser_Alias}       True
    Click Update Button      ${Browser_Alias}
    Click Back Button     ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Jaeger Tracing Value      ${Browser_Alias}     True

Validate Enabling Dgraph HA Field
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Change Dgraph Ha Field       ${Browser_Alias}      False     True
    Click Update Button      ${Browser_Alias}
    Click Back Button     ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Dgraph Ha Value      ${Browser_Alias}      True

Validate Protect Deployment
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Click Protect Button      ${Browser_Alias}
    Click Update Button For Protect Deployment     ${Browser_Alias}
    Click Back Button     ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Unprotect Button Present      ${Browser_Alias}
    Click Unprotect Button      ${Browser_Alias}

Validate Unprotect Deployment
    [Documentation]
    ...    List of tests covered
    ...
    ...    
    Click Super Admin In Menu      ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Click Protect Button      ${Browser_Alias}
    Click Update Button For Protect Deployment     ${Browser_Alias}
    Click Back Button     ${Browser_Alias}
    Search Deployment     ${Browser_Alias}     User Email     ${USER_NAME}
    Click Edit Button      ${Browser_Alias}      ${BACKEND_NAME}
    Check Unprotect Button Present      ${Browser_Alias}
    Click Unprotect Button      ${Browser_Alias}
    Change Do Not Freeze Field      ${Browser_Alias}      False      True
    Click Update Button      ${Browser_Alias}
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
    