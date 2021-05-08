*** Settings ***
Documentation     Dgraph Data Loading Test Suite
Suite Setup        Start Dgraph
Suite Teardown     Terminate and Create Backup of Dgraph Execution    ${FALSE}
Test Setup      Monitor Health And State check
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
     [Tags]    regression   NIGHTLY    CI
     Execute Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_02 Perform bulk load data.
     [Documentation]    Perform bulk load operatin on dataset.
     ...    *Author*: Sourav
     [Tags]    regression  CI  NIGHTLY
     Execute Bulk Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}       alpha_offset_bulk=${20}

TC_03 Perform parallel live and bulk load on data
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Execute Parallel Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}   alpha_offset_bulk=${30}

TC_04 Perform parallel live loads.
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Execute Multiple Parallel Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    2

TC_05 Perform Increment backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Clear Backup Folders   ${TRUE}
     Create NFS Backup    3
     Perform a restore on backup latest versions    2
     Clear Backup Folders   ${TRUE}
 
TC_06 Perfrom NFS export on dgraph
    [Documentation]  Test Case to perform nfs export.
    ...    *Author*: Krishna, Sourav and Sankalan
    [Tags]      regression   WEEKLY
    Export NFS data using admin endpoint    json    ${TRUE}
