*** Settings ***
Documentation     Dgraph Live Loading Test Suite with ludicrous mode
Suite Setup        Start Dgraph Ludicrous Mode
Suite Teardown     End All Process    true
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
     [Tags]    regression   C698
     Execute Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_02 Perform bulk load data.
     [Documentation]    Perform bulk load operatin on dataset.
     ...    *Author*: Sourav
     [Tags]    regression
     Execute Bulk Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_03 Perfrom NFS export on dgraph
    [Documentation]  Test Case to perform nfs export.
    [Tags]      regression   WEEKLY
    Export NFS data using admin endpoint    rdf    true

TC_04 Perform NFS backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Krishna, Sourav and Sankalan
     [Tags]    regression   C702    C700   WEEKLY
     Create NFS Backup      full
     perform a restore on backup

TC_05 Perform parallel live and bulk load on data
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Execute Parallel Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_06 Perform Increment backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Create NFS Backup    full
     Create NFS Backup    increment
     perform a restore on backup

TC_07 Perform parallel live loads.
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Execute Multiple Parallel Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    2
