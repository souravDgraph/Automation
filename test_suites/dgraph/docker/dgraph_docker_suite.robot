*** Settings ***
Documentation     Dgraph Docker Test Suite
Suite Setup       Start Dgraph In Docker    ${docker-file}
Test Setup      Monitor Health And State check
Suite Teardown    End Docker Execution    ${docker-file}    false
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
    [Tags]    regression    C698
    Execute Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}