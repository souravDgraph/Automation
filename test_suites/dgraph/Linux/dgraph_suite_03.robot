*** Settings ***
Documentation     Dgraph Live Loading Test Suite with ludicrous mode
Suite Setup        Start Dgraph Ludicrous Mode
Suite Teardown     Terminate and Create Backup of Dgraph Execution    false
Test Setup      Monitor Health And State check
Test Teardown   Monitor zero and alpha process  true
Default Tags    ludicrous
Resource          ../../../resources/dgraph_commands.robot
Library           Dgraph
Library           String

*** Variables ***
${rdf_file}       1million.rdf.gz
${schema_file}    1million.schema


*** Test Cases ***
TC_01 Perform live load data.
     [Documentation]    Perform live load operation on dataset.
     ...    *Author*: Krishna, Sourav and Sankalan
     [Tags]    regression   C698     CI  NIGHTLY
     Execute Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_02 Perform bulk load data.
     [Documentation]    Perform bulk load operatin on dataset.
     ...    *Author*: Sourav
     [Tags]    regression   CI  NIGHTLY
     Execute Bulk Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_03 Perfrom NFS export on dgraph
    [Documentation]  Test Case to perform nfs export.
    ...    *Author*: Krishna, Sourav and Sankalan
    [Tags]      regression   WEEKLY
    Export NFS data using admin endpoint    json    true

TC_04 Perform NFS backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Krishna and Sankalan
     [Tags]    regression   C702    C700   WEEKLY
     Clear Backup Folders   true
     Create NFS Backup      1
     log        ${is_latest_global_check}
     Run Keyword If     ${is_latest_global_check}     Perform a restore on backup latest versions    0
     ...    ELSE    Perform a restore on backup by older dgraph versions
     Clear Backup Folders   true
     [Teardown]    NONE

TC_05 Perform parallel live and bulk load on data
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Execute Parallel Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_06 Perform Increment backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Clear Backup Folders   true
     Create NFS Backup    2
     Run Keyword If     ${is_latest_global_check}     Perform a restore on backup latest versions    1
     ...    ELSE    Perform a restore on backup by older dgraph versions
     Clear Backup Folders   true
     [Teardown]    NONE

TC_07 Perform parallel live loads.
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Execute Multiple Parallel Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    2
