*** Settings ***
Documentation     Dgraph Live Loading Test Suite
Suite Setup       Start Dgraph  local
Test Setup      Monitor Health And State check
Test Teardown     End All Process    true
Resource          ../../resources/dgraph_commands.robot
Library           Dgraph

*** Variables ***
${rdf_file}       1million.rdf.gz
${schema_file}    1million.schema

*** Test Cases ***
TC_01 Restore the empty backup previously taken
    [Documentation]    Verify the empty backup and restore operation for dgraph
    ...    *Author*: Krishna, Sourav and Sankalan
    [Tags]    regression    C700    C702
    Create NFS Backup      full
    perform a restore on backup


