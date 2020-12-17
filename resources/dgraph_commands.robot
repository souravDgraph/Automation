*** Settings ***
Library           OperatingSystem
Library           Process
Library           Dgraph
Library           JSONLibrary
Library           String

*** Keywords ***
Start Dgraph
    [Documentation]    Start Dgraph alpha and Zero process with cwd poiting to results folder.
    # Dgraph alpha and zero command
    ${result_z}=    Process.start Process    dgraph    zero    2>&1    alias=zero    cwd=results    shell=yes    stdout=zero.txt
    Process Should Be Running    zero
    Wait For Process    timeout=10 s    on_timeout=continue
    ${result_a}=    Process.start Process    dgraph    alpha    2>&1    alias=alpha    stdout=alpha.txt    cwd=results    shell=yes
    Process Should Be Running    alpha
    Wait For Process    timeout=10 s    on_timeout=continue

Start Dgraph Zero
    [Documentation]    Start Dgraph Zero process
    ${result_z}=    Process.start Process    dgraph    zero    2>&1    alias=zero    cwd=results    shell=yes    stdout=zero.txt    stderr=zeroerr.txt
    Process Should Be Running    zero
    Wait For Process    timeout=10 s    on_timeout=continue

Start Dgraph Alpha for bulk loader
    [Arguments]    ${path}
    [Documentation]    Start Dgraph Alpha with bulk loader data
    ...    "path"- path of the backup file, "process_id" - process id trigged for this process.
    ${result_a}=    Process.start Process    dgraph    alpha    -p    ${path}    alias=alpha    stdout=alpha.txt    stderr=alphaerr.txt    shell=True    cwd=results
    Process Should Be Running    alpha
    Wait For Process    timeout=10 s    on_timeout=continue
    # End dgraph and zero process and clear the folders created in results

End All Process
    [Arguments]    ${is_clear_folder}
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    Terminate All Processes
    Sleep    5s
    Verify file Content in results folder   zero    All done. Goodbye!
    Verify file Content in results folder   alpha    Buffer flushed successfully.
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders

End Zero Process
    [Arguments]    ${is_clear_folder}
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    Terminate All Processes
    Sleep    5s
    Verify file Content in results folder   zero    All done. Goodbye!
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders

End Aplha Process
    [Arguments]    ${is_clear_folder}
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    Terminate All Processes
    Sleep    5s
    Verify file Content in results folder    alpha    Buffer flushed successfully.
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders

# Bulk/Live Loader
Execute Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}    ${loader_type}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" and "loader_type" perform live/bulk loader.
    ...     rdf_filename, schema_filename ,loader_type- "live"/"bulk"
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${result_loader}=    Process.start Process    dgraph    ${loader_type}    -f    ${dir_path}/test_data/datasets/${rdf_filename}    -s    ${dir_path}/test_data/datasets/${schema_filename}    alias=${loader_type}    stdout=${loader_type}.txt    shell=yes    cwd=results
    Process Should Be Running    zero
    Run Keyword If    '${loader_type}' == 'live'    Process Should Be Running    alpha
    Process Should Be Running    ${loader_type}
    ${wait}=    Wait For Process    ${loader_type}
    Process Should Be Stopped       ${loader_type}
    Should Be Equal As Integers    ${wait.rc}    0
    Sleep    5s
    ${loader_Text_File_Content}    Get File    ${dir_path}/results/${loader_type}.txt
    Run Keyword If    '${loader_type}' == 'live'    Should Contain    ${loader_Text_File_Content}    N-Quads:
    ...    ELSE    Run Keywords    Should Contain    ${loader_Text_File_Content}    100.00%
    ...    AND    Verify Bulk Loader output generated    ${dir_path}/results/out/0/p
    ...    AND    Start Dgraph Alpha for bulk loader    ${dir_path}/results/out/0/p
    ...    AND    End Aplha Process    true


# Backup Keywords
Create NFS Backup
    [Arguments]    ${url}    ${appenders}
    [Documentation]    Accepts two params: "{URL}","{appenders}"
    ...    Keyword to create a NFS backup i.e to save backup to local folder
    ${root_path}=    normalize path    ${CURDIR}/..
    ${backup_path}=    Join Path    ${root_path}/backup
    clear all the folder in a directory    ${backup_path}
    connect server    ${url}
    ${res}=    post nfs command    ${appenders}    ${backup_path}
    log    ${res.text}
    Verify file exists in a directory with parent folder name    ${backup_path}

# Restore Keywords
Perform a restore on backup
    [Documentation]    Performs an restore operation on the default location i.e "backup" dir.
    ${root_dir}=    normalize path    ${CURDIR}/..
    ${path}=    Join Path    ${root_dir}/backup
    @{dirs_backup}=    List Directories In Directory    ${path}
    ${restore_dir}=    Set Variable    ${dirs_backup}[0]
    ${restore_dir}=    Join Path    ${root_dir}/backup/${restore_dir}
    ${result_restore}=    Start Process    dgraph    restore    -p    ${restore_dir}    -l    ${restore_dir}    -z    localhost:5080    alias=restore    stdout=restorebackup.txt    shell=yes    cwd=results
    Process Should Be Running    zero
    Process Should Be Running    alpha
    Process Should Be Running    restore
    ${wait}=    Wait For Process    restore
    Process Should Be Stopped       restore
    Should Be Equal As Integers    ${wait.rc}    0
    Sleep    5s
    Verify retore file Content in results folder    restorebackup    ${restore_dir}

Perform a restore on backup present at other location
    [Arguments]    ${path}
    [Documentation]    Performs an restore operation on the backup created.
    ...    Accepts one paramter "{path}" <- complete path including name of the folder of the backup file.
    ${result_restore}=    Start Process    dgraph    restore    -p    ${path}    -l    ${path}    -z    localhost:5080    alias=restore    stdout=restorebackup.txt    shell=yes    cwd=results
    Process Should Be Running    zero
    Process Should Be Running    alpha
    Process Should Be Running    restore
    ${wait}=    Wait For Process    restore
    Process Should Be Stopped       restore
    Should Be Equal As Integers    ${wait.rc}    0
    Sleep    5s
    Verify retore file Content in results folder    restorebackup    ${restore_dir}


# Validations:
Verify retore file Content in results folder
    [Arguments]    ${file_name}    ${path}
    [Documentation]    Keyword for validating content in restore.txt files generated in results folder
    ...    [Arguments] -> "file_name" -file name ex: alpha for alpha.txt | "cotent" -content you want to check in file
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${file_context}=    Get File    ${dir_path}/results/${file_name}.txt
    @{compare_context}=    Create List    Restoring backups from: ${path}    Writing postings to: ${path}    Updating Zero timestamp at: localhost:5080
    FOR    ${context}    IN    @{compare_context}
        Should Contain    ${file_context}    ${context}
    END

Verify Bulk Loader output generated
    [Documentation]     Keyword to verify bulk loader files output
    [Arguments]    ${path}
    @{count}=    List Files In Directory    ${path}
    ${list_size}    Get Length    ${count}
    Run Keyword If    ${list_size}<0    FAIL    “Files were not generated.”

# File operations keywords
clean up dgraph folders
    [Documentation]    Keyword to clear up the dgraph alpha and zero folder created.
    ${curr_dir}=    Normalize Path    ${CURDIR}/..
    @{dir}    Create List    p    t    w    zw    out
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

Verify file Content in results folder
    [Arguments]    ${file_name}    ${context}
    [Documentation]    Keyword for checking content in .txt files generated in results folder
    ...    [Arguments] -> "file_name" -file name ex: alpha for alpha.txt | "cotent" -content you want to check in file
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${file_context}=    Get File    ${dir_path}/results/${file_name}.txt
    Should Contain    ${file_context}    ${context}