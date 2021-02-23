*** Settings ***
Documentation     Dgraph Docker Test Suite
Suite Setup       Start Dgraph In Docker
Test Setup      Monitor Health And State check
Suite Teardown    End Docker    true
Default Tags    docker
Resource          ../../resources/dgraph_commands.robot
Library           DockerComposeLibrary    ${docker_compose_file}

*** Variables ***
${dir_path}=        ${CURDIR}/../..
${rdf_file}        1million.rdf.gz
${schema_file}     1million.schema
${docker-node}      4
${docker-file}      conf/docker-${docker-node}node
${docker_compose_file}      ${dir_path}/${docker-file}/docker-compose.yml

*** Test Cases ***
TC_01 Docker - Verify Increment Operation
    [Documentation]    Verify the logs for successful execution of big dataset in live loader
    ...    *Author*: Krishna, Sourav, Vivetha and Sankalan
    [Tags]    regression    C698
    ${alpha_nodes_check}    Set Variable If     ${docker-node}==4   3   1
    Execute Increment   ${alpha_nodes_check}   100

TC_02 Docker - Import a big dataset with the live loader - Ubuntu or CentOS
    [Documentation]    Verify the logs for successful execution of big dataset in live loader
    ...    *Author*: Krishna, Sourav, Vivetha and Sankalan
    [Tags]    regression    C698
    Execute Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

*** Keywords ***
Start Dgraph In Docker
    Docker Compose Up
    Sleep   30s

End Docker
    [Arguments]     ${is_clear_folder}
    Terminate All Processes
    Docker Compose Down
    @{dir}    Create List    p    t    w    out    alpha
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up list of folders in results dir    @{dir}