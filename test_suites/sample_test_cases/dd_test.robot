*** Settings ***
Documentation    Data Driven Dgraph Live Loading Test Suite

Library     OperatingSystem
Library     String
Library     Process
Library     DataDriver      ../../../test_data/liveloading_datasets/liveload.csv
Resource    ../../resources/dgraph_commands.robot

Suite Setup     Start Dgraph
Suite Teardown  End All Process     true
Test Template   Template for live loader execution

*** Variables ***
${backup_path}      /Users/apple/Desktop/Dgraph_workspace/robot_framework/dgraph_framework/next

*** Test Cases ***
Import a big dataset with the live loader - Ubuntu or CentOS
    ${rdf_filename}     ${schema_filename}

Restore the backup previously taken - Ubuntu or CentOS
    [Documentation]    Verify the backup funcationality for dgraph
    ...    *Author*: Krishna, Sourav and Sankalan
    [Tags]    regression    C702
    Perfrom an empty NFS backup    ${backup_path}

*** Keywords ***
Template for live loader execution
    [Arguments]    ${rdf_filename}    ${schema_filename}
    ${P1}=    normalize path    ${CURDIR}/..
    ${result_live_loader}=    Process.start Process    dgraph    live    -f    ${P1}/test_data/datasets/${rdf_filename}    -s    ${P1}/test_data/datasets/${schema_filename}    2>&1    alias=live    stdout=liveloader.txt    shell=yes    cwd=results
    Process Should Be Running    zero
    Process Should Be Running    alpha
    Process Should Be Running    live
    Should Be Equal As Integers    ${result_live_loader}    3
    ${wait}=    Wait For Process    live
    Process Should Be Stopped
    Should Be Equal As Integers    ${wait.rc}    0
    Sleep    5s
    Log To Console    ${result_live_loader}
    ${Live_Text_File_Content}    Get File    ${P1}/results/liveloader.txt
    Should Contain    ${Live_Text_File_Content}    Finished writing xid map to DB

Perfrom an empty NFS backup
    [Documentation]     Perfoms an
    [Arguments]    ${backup_path}
    Create Session    backup    http://localhost:8080
    ${P1}=    normalize path    ${CURDIR}/..
    ${headers}=    create dictionary    Content-Type=multipart/form-data    Accept=text/plain
    ${data_params}=    ${backup_path}
    ${resp}    Post Request    backup    /admin/backup    data=${data_params}    headers=${headers}
    log    ${resp.json()}
    Request Should Be Successful    ${resp}
    Status Should Be    200    ${resp}