*** Settings ***
Documentation     Dgraph Live Loading Test Suite
Suite Setup        Start Dgraph    docker
Suite Teardown     End All Process    true
Resource          ../../../resources/dgraph_commands.robot
Library           Dgraph
Library           String

*** Variables ***
${URL}            http://localhost:8080
${rdf_file}       1million.rdf.gz
${schema_file}    1million.schema
${appenders}      /admin

*** Test Cases ***
TC_01 Perform liveload backup restore data.
     [Documentation]    Perform live load data.
     ...    *Author*: Krishna, Sourav and Sankalan
     [Tags]    regression   C698
     Execute Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}     live


TC_02 Perform NFS backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Krishna, Sourav and Sankalan
     [Tags]    regression   C702    C700
     Create NFS Backup  ${URL}    ${appenders}
     perform a restore on backup

