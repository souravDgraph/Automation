*** Settings ***
Documentation     Dgraph Live Loading Test Suite with Learner Node
Suite Setup        Start Dgraph with learner node
Suite Teardown     Terminate and Create Backup of Dgraph Execution    false
Test Setup      Monitor Health And State check
Test Teardown   Monitor zero and alpha process  true
Resource          ../../../resources/dgraph_commands.robot
Library           Dgraph
Library           String

*** Variables ***
${rdf_file}       1million.rdf.gz
${schema_file}    1million.schema

*** Test Cases ***
TC_01 Perform live load data.
     [Documentation]    Perform live load operation on dataset.
     ...    *Author*: Sourav
     [Tags]    regression     NIGHTLY
     Execute Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    is_learner=true
     [Teardown]    NONE

TC_02 Perform NFS backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Clear Backup Folders   true
     Create NFS Backup      1
     log        ${is_latest_global_check}
     Run Keyword If     ${is_latest_global_check}     Perform a restore on backup latest versions    0
     ...    ELSE    Perform a restore on backup by older dgraph versions
     Clear Backup Folders   true
     [Teardown]    NONE

TC_03 Perform bulk load data.
     [Documentation]    Perform bulk load operatin on dataset.
     ...    *Author*: Sourav
     [Tags]    regression  NIGHTLY
     [Setup]  Monitor zero and alpha process  true
     Execute Bulk Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_04 Perform parallel live and bulk load on data
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Execute Parallel Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_05 Perform Increment backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Clear Backup Folders   true
     Create NFS Backup    2
     Run Keyword If     ${is_latest_global_check}     Perform a restore on backup latest versions    1
     ...    ELSE    Perform a restore on backup by older dgraph versions
     Clear Backup Folders   true
     [Teardown]    NONE

TC_06 Perform parallel live loads.
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Execute Multiple Parallel Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    2
     [Teardown]    NONE     
 
TC_07 Perfrom NFS export on dgraph
    [Documentation]  Test Case to perform nfs export.
    ...    *Author*: Sourav
    [Tags]      regression   WEEKLY
    Export NFS data using admin endpoint    json    true
    [Teardown]    NONE