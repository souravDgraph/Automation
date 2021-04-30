*** Settings ***
Documentation     Dgraph Docker Test Suite
Suite Setup       Start Dgraph 2-node In Docker with bulk data    ${dgraph_docker_version}   ${container_name}    ${None}
Test Setup      Monitor Health And State check
Test Teardown    Retrigger Docker File       ${dgraph_docker_version}   ${container_name}    ${None}     true
Suite Teardown    Terminate Docker Execution and Create Backup of Dgraph Execution    ${container_name}    true
Default Tags    docker
Resource          ../../../resources/dgraph_docker_commands.robot

*** Variables ***
${rdf_file}        1million.rdf.gz
${schema_file}     1million.schema
${alpha-node}      1
${zero-node}      1

# alpha container to interact and perform all the dgraph operations on
${container_name}   alpha1

${dgraph_docker_version}   master

*** Test Cases ***
TC_01 Docker - Perform parallel Live and Bulk Load.
     [Documentation]    Perform live and Bulk load data.
     ...    *Author*: Sourav, Krishna
     [Tags]    regression   WEEKLY  CI
     Docker Execute Parallel Loader with rdf and schema parameters    ${dgraph_docker_version}   ${container_name}      ${rdf_file}    ${schema_file}    zero1   alpha1
     [Teardown]    NONE

TC_02 Docker - Verify Increment Operation
    [Documentation]    Verify the logs for successful execution of big dataset in live loader
    ...    *Author*: Krishna, Sourav, Vivetha and Sankalan
    [Tags]    regression    C698
    Docker Execute Increment Command   ${alpha-node}

TC_03 Docker - Import a big dataset with the live loader - Ubuntu or CentOS
    [Documentation]    Verify the logs for successful execution of big dataset in live loader
    ...    *Author*: Krishna, Sourav, Vivetha and Sankalan
    [Tags]    regression    C698  CI
    Docker Execute Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}      zero1   alpha1
    [Teardown]    NONE

TC_04 Docker - Perfrom NFS export on dgraph
    [Documentation]  Test Case to perform nfs export.
    ...    *Author*: Krishna, Sourav and Sankalan
    [Tags]      regression   WEEKLY
    Docker Export NFS data using admin endpoint    json    true   alpha1
    [Teardown]    NONE

TC_05 Docker - Perform NFS backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Krishna and Sankalan
     [Tags]    regression   C702    C700   WEEKLY
     Clear Backup Folders   true
     Docker Create NFS Backup      1    alpha1
     Run Keyword If     ${DGRAPH_LATEST_VERSION_CHECK}     Docker Perform a restore on backup latest versions    0      alpha1      zero1
     ...    ELSE    Docker Perform a restore on backup by older dgraph versions     alpha1      zero1
     Clear Backup Folders   true

TC_06 Docker - Import a big dataset with the Bulk loader - Ubuntu or CentOS
    [Documentation]    Verify the logs for successful execution of big dataset in bulk loader
    ...    *Author*: Krishna, Sourav, Vivetha and Sankalan
    [Tags]    regression    C698  CI
    Docker Execute Bulk Loader for Docker with rdf and schema parameters    ${dgraph_docker_version}   ${container_name}      ${rdf_file}    ${schema_file}     zero1
    [Teardown]    NONE

TC_07 Docker - Perform Increment backup and restore on bulk data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Krishna and Sankalan
     [Tags]    regression   C702    C700   WEEKLY
     Clear Backup Folders   true
     Docker Create NFS Backup      3    alpha1
     Run Keyword If     ${DGRAPH_LATEST_VERSION_CHECK}     Docker Perform a restore on backup latest versions    2      alpha1      zero1
     ...    ELSE    Docker Perform a restore on backup by older dgraph versions     alpha1      zero1
     Clear Backup Folders   true

TC_08 Docker - Perform parallel live loads.
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav, Krishna
     [Tags]    regression   WEEKLY  CI
     Docker Execute Multiple Parallel Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    2    zero1   alpha1
     [Teardown]    NONE

TC_09 Docker - Perform Increment backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Sourav, Krishna
     [Tags]    regression   WEEKLY
     Clear Backup Folders   true
     Docker Create NFS Backup    2      alpha1
     Run Keyword If     ${DGRAPH_LATEST_VERSION_CHECK}     Docker Perform a restore on backup latest versions    1      alpha1      zero1
     ...    ELSE    Docker Perform a restore on backup by older dgraph versions      alpha1      zero1
     Clear Backup Folders   true