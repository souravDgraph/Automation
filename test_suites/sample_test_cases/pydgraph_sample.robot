*** Settings ***
Documentation     Dgraph Live Loading Test Suite
Suite Setup       Start Dgraph
Suite Teardown    End All Process    false
Resource          ../../resources/dgraph_commands.robot
Library           Common

*** Variables ***
${rdf_file}       1million.rdf.gz
${schema_file}    1million.schema

*** Test Cases ***
Import a big dataset with the live loader - Ubuntu or CentOS
    [Documentation]    Verify the logs for successful execution of big dataset in live loader
    ...    *Author*: Krishna, Sourav, Vivetha and Sankalan
    [Tags]    regression    C698
    #Execute Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    live
    Pyd Create Acl And Mtls Connection    localhost:9080
    Pyd Set Schema    ${schema_file}
    Pyd Get Data    "{queryall (func: has(director.film)) {name director.film actor.film} }"
