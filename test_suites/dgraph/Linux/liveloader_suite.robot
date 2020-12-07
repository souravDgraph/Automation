*** Settings ***
Documentation     Dgraph Live Loading Test Suite
Suite Setup       Start Dgraph
Suite Teardown    End All Process
Library           OperatingSystem
Library           String
Library           Process
Resource          ../../../resources/dgraph_commands.robot

*** Test Cases ***
Import a big dataset with the live loader - Ubuntu or CentOS
    [Documentation]    Verify the logs for successful execution of big dataset in live loader
    ...    *Author*: Krishna, Sourav, Vivetha and Sankalan
    [Tags]    regression    C698
    Execute Live Loader with rdf and schema parameters    1million.rdf.gz    1million.schema
