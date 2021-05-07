*** Settings ***
Documentation     Dgraph Data Loading Test Suite with Learner Node
Suite Setup        Start Dgraph with learner node
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
     ...    *Author*: Sourav
     [Tags]    regression     NIGHTLY
     Execute Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    is_learner=${TRUE}

TC_04 Perform NFS backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Clear Backup Folders   ${TRUE}
     Create NFS Backup      3
     Perform a restore on backup latest versions    2

TC_05 Perfrom NFS export on dgraph
    [Documentation]  Test Case to perform nfs export.
    ...    *Author*: Sourav
    [Tags]      regression   WEEKLY
    Export NFS data using admin endpoint    json    ${TRUE}

TC_02 Perform parallel live and bulk load on data
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Execute Parallel Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    is_learner=${TRUE} 

TC_03 Perform parallel live loads.
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Execute Multiple Parallel Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    2     is_learner=${TRUE}

TC_04 Perform NFS backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Clear Backup Folders   ${TRUE}
     Create NFS Backup      3
     Perform a restore on backup latest versions    2

TC_05 Perfrom NFS export on dgraph
    [Documentation]  Test Case to perform nfs export.
    ...    *Author*: Sourav
    [Tags]      regression   WEEKLY
    Export NFS data using admin endpoint    json    ${TRUE}
