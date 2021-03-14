*** Settings ***
Documentation     Dgraph Live Loading Test Suite
Suite Setup        Start Dgraph
Suite Teardown     End All Process    false
Test Setup      Monitor Health And State check
Test Teardown   Monitor zero and alpha process
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
    ...    *Author*: Krishna, Sourav and Sankalan
    [Tags]      regression
    Export NFS data using admin endpoint    json    true

TC_04 Perform NFS backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Krishna and Sankalan
     [Tags]    regression   C702    C700
     Create NFS Backup      1
     perform a restore on backup    0
     Clear Backup Folders   true

TC_05 Perform parallel live and bulk load on data
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   CI
     Execute Parallel Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_06 Perform Increment backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Sourav
     [Tags]    regression   CI
     Create NFS Backup    2
     perform a restore on backup    1
     Clear Backup Folders   true

TC_07 Perform parallel live loads.
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   CI
     Execute Multiple Parallel Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    2
