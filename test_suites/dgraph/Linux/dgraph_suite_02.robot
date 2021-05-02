*** Settings ***
Documentation     Dgraph Cross Version Backup and Restore Suite
Suite Teardown    Terminate and Create Backup of Dgraph Execution    false
Resource          ../../../resources/dgraph_commands.robot
Library           Dgraph
Library           String

*** Variables ***
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
    Start Dgraph
    Create NFS Backup    2
    Terminate and Create Backup of Dgraph Execution     ${TRUE}
    Build Dgraph Version    ${current_version}
    Start Dgraph
    Run Keyword If     ${LATEST_VERSION_CHECK}     Perform a restore on backup latest versions    1
     ...    ELSE    Perform a restore on backup by older dgraph versions
    Terminate and Create Backup of Dgraph Execution     false
