*** Settings ***
Documentation     Dgraph Live Loading Test Suite
Suite Teardown    End All Process    false
Resource          ../../../resources/dgraph_commands.robot
Library           Dgraph
Library           String

*** Variables ***
${URL}            http://localhost:8080
${rdf_file}       1million.rdf.gz
${schema_file}    1million.schema
${appenders}      /admin
${prev_version}    v20.07.3-rc1
${current_version}    v20.11.1-rc2

*** Test Cases ***
TC_01 Perform cross version backup and restore.
    [Documentation]    Perform cross version backup and restore
    ...    *Author*: Sourav
    [Tags]    regression
    Build Dgraph Version    ${prev_version}
    Start Dgraph    local
    Create NFS Backup    full
    Create NFS Backup    increment
    End All Process    true
    Build Dgraph Version    ${current_version}
    Start Dgraph    local
    perform a restore on backup
    End All Process    false
