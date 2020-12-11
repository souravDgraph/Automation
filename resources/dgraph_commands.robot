*** Settings ***
Library           OperatingSystem
Library           Process
Library           RequestsLibrary
Library           JSONLibrary
Library           String

*** Keywords ***
# Dgraph alpha and zero command
Start Dgraph
    [Documentation]    Start Dgraph alpha and Zero process
    ${result_z}=    Process.start Process    dgraph    zero    2>&1    alias=zero    cwd=results    shell=yes    stdout=zero.txt
    Process Should Be Running    zero
    Wait For Process    timeout=10 s    on_timeout=continue
    Should Be Equal As Integers    ${result_z}    1
    ${result_a}=    Process.start Process    dgraph    alpha    2>&1    alias=alpha    stdout=alpha.txt    cwd=results    shell=yes
    Process Should Be Running    alpha
    Should Be Equal As Integers    ${result_a}    2
    Wait For Process    timeout=10 s    on_timeout=continue
    # End dgraph and zero process and clear the folders created in results

End All Process
    [Arguments]    ${is_clear_folder}
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    Terminate All Processes
    ${P1}=    normalize path    ${CURDIR}/..
    Sleep    5s
    ${Alpha_Text_Context}    Get File    ${P1}/results/alpha.txt
    Should Contain    ${Alpha_Text_Context}    Buffer flushed successfully.
    ${Zero_Text_Context}    Get File    ${P1}/results/zero.txt
    Should Contain    ${Zero_Text_Context}    All done. Goodbye!
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders

Execute Live Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}
    [Documentation]    Keyword to accept two params "rdf_filename","schema_filename" and perform live loader.
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

# Backup Keywords
Create NFS Backup
    [Arguments]    ${URL}    ${appenders}
    [Documentation]    Accepts three params: "{URL}","{appenders}" and "{backup_path}"
    ...    Keyword to create a NFS backup i.e to save backup to local folder
    ${P1}=    normalize path    ${CURDIR}/..
    ${backup_path}=     Join Path	${P1}	backup
    clear all the folder in a directory    ${backup_path}
    connect server    ${URL}
    ${res}=    post nfs command    ${appenders}    ${backup_path}
    log    ${res.text}
    Verify file exists in a directory with parent folder name    ${backup_path}

# Restore Keywords
Perform a restore on backup
    [Documentation]     Performs an restore operation on the default location of backup created.
    ${P1}=    normalize path    ${CURDIR}/..
    ${path}=     Join Path	${P1}	backup
    ${result_restore}=    Start Process    dgraph    restore    -p    ${path}/dgraph.202*    -l    ${path}/dgraph.202*    -z    localhost:5080    alias=restore    stdout=restorebackup.txt    shell=yes    cwd=results
    Process Should Be Running    zero
    Process Should Be Running    alpha
    Process Should Be Running    restore
    Should Be Equal As Integers    ${result_restore}    3
    ${wait}=    Wait For Process    restore
    Process Should Be Stopped	restore
    Should Be Equal As Integers    ${wait.rc}    0
    Sleep    5s
    ${Live_Text_File_Content}    Get File    ${P1}/results/restorebackup.txt
    Should Contain    ${Live_Text_File_Content}    Updating Zero timestamp at

Perform a restore on backup present at other location
    [Documentation]     Performs an restore operation on the backup created.
    ...     Accepts one paramter "{path}" <- path of the backup file.
    [Arguments]    ${path}
    ${P1}=    normalize path    ${CURDIR}/..
    ${result_restore}=    Start Process    dgraph    restore    -p    ${path}    -l    ${path}    -z    localhost:5080    alias=restore    stdout=restorebackup.txt    shell=yes    cwd=results
    Process Should Be Running    zero
    Process Should Be Running    alpha
    Process Should Be Running    restore
    Should Be Equal As Integers    ${result_restore}    3
    ${wait}=    Wait For Process    restore
    Process Should Be Stopped	restore
    Should Be Equal As Integers    ${wait.rc}    0
    Sleep    5s
    ${Live_Text_File_Content}    Get File    ${P1}/results/restorebackup.txt
    Should Contain    ${Live_Text_File_Content}    Updating Zero timestamp at

# File operations keywords
clean up dgraph folders
    [Documentation]    Keyword to clear up the dgraph alpha and zero folder created.
    ${curr_dir}=    Normalize Path    ${CURDIR}/..
    @{dir}    Create List    p    t    w    zw
    FOR    ${foldername}    IN    @{dir}
        Remove Directory    ${curr_dir}/results/${foldername}    recursive=True
    END
    Log    "All the folders were deleted."

Clear all the folder in a directory
    [Arguments]    ${path}
    [Documentation]    Keyword to clear all the folder in a directory
    ...    Accepts one argument "{path}" <- which indicates the path of the direcory
    @{dirs}=    List Directories In Directory    ${path}
    ${list_size}    Get Length    ${dirs}
    Run Keyword If    ${list_size}>0    Remove Directory    ${path}    recursive=True

Verify file exists in a directory with parent folder name
    [Arguments]    ${path}
    [Documentation]    Keyword to verify if a file exists in a directory
    ...    Accepts one argument "{path}" <- which indicates the path of the direcory
    ${rest}    ${folder_name}=    Split String From Right    ${path}    /    1
    @{dirs}=    List Directories In Directory    ${path}
    FOR    ${dir}    IN    @{dirs}
        directory should exist    ${folder_name.strip()}/${dir}
    END
