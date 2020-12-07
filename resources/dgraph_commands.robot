*** Settings ***
Library           OperatingSystem
Library           Process

*** Keywords ***
Start Dgraph
    ${result_z}=    Process.start Process    dgraph    zero    2>&1    alias=zero    cwd=results    shell=yes    stdout=zero.txt
    Process Should Be Running    zero
    Wait For Process    timeout=10 s    on_timeout=continue
    Should Be Equal As Integers    ${result_z}    1
    ${result_a}=    Process.start Process    dgraph    alpha    2>&1    alias=alpha    stdout=alpha.txt    cwd=results    shell=yes
    Process Should Be Running    alpha
    Should Be Equal As Integers    ${result_a}    2
    Wait For Process    timeout=10 s    on_timeout=continue

End All Process
    Terminate All Processes
    ${P1}=    normalize path    ${CURDIR}/..
    Sleep    5s
    ${Alpha_Text_Context}    Get File    ${P1}/results/alpha.txt
    Should Contain    ${Alpha_Text_Context}    Buffer flushed successfully.
    ${Zero_Text_Context}    Get File    ${P1}/results/zero.txt
    Should Contain    ${Zero_Text_Context}    All done. Goodbye!

Execute Live Loader with rdf and schema parameters
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
