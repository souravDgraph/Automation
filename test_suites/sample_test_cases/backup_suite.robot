*** Settings ***
Documentation     Dgraph Live Loading Test Suite
Test Setup        Start Dgraph
Test Teardown     End All Process    true
Resource          ../../resources/dgraph_commands.robot
Library           Dgraph
Library           String

*** Variables ***
${URL}            http://localhost:8080
${backup_path}    /Users/apple/Desktop/Dgraph_workspace/robot_framework/Automation/backup
${rdf_file}       1million.rdf.gz
${schema_file}    1million.schema
${appenders}      /admin

*** Test Cases ***
TC_01 Restore the empty backup previously taken
    [Documentation]    Verify the empty backup and restore operation for dgraph
    ...    *Author*: Krishna, Sourav and Sankalan
    [Tags]    regression    C700    C702
    Create NFS Backup    ${URL}    ${appenders}
    perform a restore on backup


#TC_02 Perform liveload backup restore data.main
#     [Documentation]    Perform live load, backup and restore data.
#     ...    *Author*: Krishna, Sourav and Sankalan
#     [Tags]    regression   C702    C698    C700
#     Execute Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}     live
#     Create NFS Backup  ${URL}    ${appenders}
#     perform a restore on backup


