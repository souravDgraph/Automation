*** Settings ***
Documentation     Dgraph Docker Test Suite
Suite Setup       Start Dgraph In Docker    ${docker-file}
Test Setup      Monitor Health And State check
Suite Teardown    End Docker Execution    ${docker-file}    true
Default Tags    docker
Resource          ../../../resources/dgraph_commands.robot

*** Variables ***
${rdf_file}        1million.rdf.gz
${schema_file}     1million.schema
${docker-node}      2
${docker-file}      docker-${docker-node}node

*** Test Cases ***
TC_01 Docker - Verify Increment Operation
    [Documentation]    Verify the logs for successful execution of big dataset in live loader
    ...    *Author*: Krishna, Sourav, Vivetha and Sankalan
    [Tags]    regression    C698
    ${alpha_nodes_check}    Set Variable If     ${docker-node}==4   3   1
    Execute Increment Command   ${alpha_nodes_check}   100

TC_02 Docker - Import a big dataset with the live loader - Ubuntu or CentOS
    [Documentation]    Verify the logs for successful execution of big dataset in live loader
    ...    *Author*: Krishna, Sourav, Vivetha and Sankalan
    [Tags]    regression    C698  CI
    Execute Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_03 Docker - Perfrom NFS export on dgraph
    [Documentation]  Test Case to perform nfs export.
    ...    *Author*: Krishna, Sourav and Sankalan
    [Tags]      regression   WEEKLY
    Export NFS data using admin endpoint    json    true

TC_04 Docker - Perform NFS backup and restore data
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

#TC_05 Docker - Perform parallel live and bulk load on data
#     [Documentation]    Perform live load data.
#     ...    *Author*: Sourav
#     [Tags]    regression   WEEKLY
#     Execute Parallel Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_06 Docker - Perform Increment backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY
     Clear Backup Folders   true
     Create NFS Backup    2
     Run Keyword If     ${is_latest_global_check}     Perform a restore on backup latest versions    1
     ...    ELSE    Perform a restore on backup by older dgraph versions
     Clear Backup Folders   true
     [Teardown]    NONE

TC_07 Docker - Perform parallel live loads.
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression   WEEKLY  CI
     Execute Multiple Parallel Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    2
     [Teardown]    NONE