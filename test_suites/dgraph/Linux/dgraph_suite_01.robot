*** Settings ***
Documentation     Dgraph Live Loading Test Suite
Suite Setup        Start Dgraph    local
Suite Teardown     End All Process    true
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
     [Tags]    regression   CI   C698
     Execute Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_02 Perform bulk load data.
     [Documentation]    Perform bulk load operatin on dataset.
     ...    *Author*: Sourav
     [Tags]    regression   CI
     Execute Bulk Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_03 Perform NFS backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Krishna, Sourav and Sankalan
     [Tags]    regression   C702    C700
     Create NFS Backup      full
     perform a restore on backup
#
#TC_04 Perform parallel live and bulk load on data
#     [Documentation]    Perform live load data.
#     ...    *Author*: Sourav
#     [Tags]    regression
#     Execute Parallel Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}
#
#TC_05 Perform Increment backup and restore data
#     [Documentation]    Perform NFS backup and restore data.
#     ...    *Author*: Sourav
#     [Tags]    regression
#     Create NFS Backup    full
#     Create NFS Backup    increment
#     perform a restore on backup
#
#TC_06 Perform parallel live loads.
#     [Documentation]    Perform live load data.
#     ...    *Author*: Sourav
#     [Tags]    regression
#     Execute Multiple Parallel Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    2
