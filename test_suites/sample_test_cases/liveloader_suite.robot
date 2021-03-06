*** Settings ***
Documentation     Dgraph Live Loading Test Suite
Suite Setup       Start Dgraph  local
Test Setup      Monitor Health And State check
Suite Teardown    End All Process   true

Resource          ../../resources/dgraph_commands.robot

*** Variables ***
${rdf_file}        1million.rdf.gz
${schema_file}     1million.schema

*** Test Cases ***
Import a big dataset with the live loader - Ubuntu or CentOS
    [Documentation]    Verify the logs for successful execution of big dataset in live loader
    ...    *Author*: Krishna, Sourav, Vivetha and Sankalan
    [Tags]    regression    C698
    Execute Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}
