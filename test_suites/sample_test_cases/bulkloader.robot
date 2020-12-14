*** Settings ***
Documentation     Dgraph Live Loading Test Suite
Suite Setup       Start Dgraph Zero
Suite Teardown    End Zero Process   true
Library           OperatingSystem
Library           String
Library           Process
Resource          ../../resources/dgraph_commands.robot

*** Variables ***
${rdf_file}        1million.rdf.gz
${schema_file}     1million.schema

*** Test Cases ***
Import a big dataset with the Bulk loader - Ubuntu or CentOS
    [Documentation]    Verify the logs for successful execution of big dataset in bulk loader
    ...    *Author*: Krishna, Sourav, Vivetha and Sankalan
    [Tags]    regression    C698
    Execute Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}      bulk
