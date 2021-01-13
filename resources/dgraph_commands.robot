*** Settings ***
Library           OperatingSystem
Library           Process
Library           Dgraph
Library           JSONLibrary
Library           String
Library           Collections

*** Keywords ***
Start Dgraph
    [Arguments]    ${platform}
    [Documentation]    Start Dgraph alpha and Zero process with cwd pointing to results folder.
    # Dgraph alpha and zero command
    Run Keyword If    '${platform}' == 'docker'    Start Dgraph In Docker
    Run Keyword If    '${platform}' == 'docker'    Return From Keyword
    ${zero_command}    Get Dgraph Cli Command    zero
    ${result_z}=    Process.start Process    ${zero_command}    alias=zero    cwd=results    shell=yes    stdout=zero.txt
    Process Should Be Running    zero
    Wait For Process    timeout=10 s    on_timeout=continue
    ${alpha_command}    Get Dgraph Cli Command    alpha
    ${result_a}=    Process.start Process    ${alpha_command}    alias=alpha    stdout=alpha.txt    cwd=results    shell=yes
    Process Should Be Running    alpha
    Wait For Process    timeout=10 s    on_timeout=continue

Start Dgraph In Docker
    [Documentation]    Start Dgraph alpha and Zero process in Helm with cwd pointing to results folder.
    # Dgraph alpha and zero command
    ${dir_path}=    normalize path    ${CURDIR}/..
    log    ${dir_path}
    ${result_docker}=    Process.run Process    docker    --version    alias=docker    stdout=docker.txt    cwd=results    shell=yes
    log    ${result_docker.stdout}
    Should Be Equal As Integers    ${result_docker.rc}    0
    ${result_docker_compose}=    Process.run Process    docker-compose    --version    alias=docker_compose    stdout=docker_compose.txt    cwd=results    shell=yes
    Should Be Equal As Integers    ${result_docker_compose.rc}    0
    OperatingSystem.Create Directory    ${dir_path}/data
    Process.start Process    docker-compose    -f    ${dir_path}/conf/docker-compose.yml    up    alias=dc_up    cwd=results    shell=yes    stdout=docker_compose_up.txt
    Process Should Be Running    dc_up
    Wait For Process    timeout=10 s    on_timeout=continue

Start Dgraph Zero
    [Documentation]    Start Dgraph Zero process
    ${result_z}=    Process.start Process    dgraph    zero    2>&1    alias=zero    cwd=results    shell=yes    stdout=zero.txt    stderr=zero_err.txt
    Process Should Be Running    zero
    Wait For Process    timeout=10 s    on_timeout=continue

Start Dgraph Alpha for bulk loader
    [Arguments]    ${path}
    [Documentation]    Start Dgraph Alpha with bulk loader data
    ...    "path"- path of the backup file, "process_id" - process id trigged for this process.
    ${result_a}=    Process.start Process    dgraph    alpha    -p    ${path}    alias=alpha    stdout=alpha.txt    stderr=alpha_err.txt    shell=True    cwd=results
    Process Should Be Running    alpha
    Wait For Process    timeout=10 s    on_timeout=continue
    # End dgraph and zero process and clear the folders created in results

End All Process
    [Arguments]    ${is_clear_folder}
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    Terminate All Processes
    Sleep    5s
    @{zero_context}    Create List    All done. Goodbye!    Got connection request
    @{alpha_context}    Create List    Buffer flushed successfully.    Operation completed with id: opRestore
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders
    Verify file Content in results folder    zero    @{zero_context}
    Verify file Content in results folder    alpha    @{alpha_context}
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders

End Zero Process
    [Arguments]    ${is_clear_folder}
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    Terminate All Processes
    Sleep    5s
    @{zero_context}    Create List    All done. Goodbye!
    Verify file Content in results folder    zero    @{zero_context}
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders

End Aplha Process
    [Arguments]    ${is_clear_folder}
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    Terminate All Processes
    Sleep    5s
    @{alpha_context}    Create List    Buffer flushed successfully.
    Verify file Content in results folder    alpha    @{alpha_context}
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders
    # Bulk/Live Loader

Execute Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}    ${loader_type}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" and "loader_type" perform live/bulk loader.
    ...    rdf_filename, schema_filename ,loader_type- "live"/"bulk"
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${value}=       Get Tls Value
    ${conf_live_command}=        Get Dgraph Loader Command    ${dir_path}/test_data/datasets/${rdf_filename}    ${dir_path}/test_data/datasets/${schema_filename}       ${loader_type}
    ${result_loader}=      Run Keyword If      "${value}"=="True"       Process.start Process    ${conf_live_command}    alias=${loader_type}    stdout=${loader_type}.txt    shell=yes    cwd=results
    ...     ELSE    Process.start Process    dgraph    ${loader_type}    -f    ${dir_path}/test_data/datasets/${rdf_filename}    -s    ${dir_path}/test_data/datasets/${schema_filename}    alias=${loader_type}    stdout=${loader_type}.txt    shell=yes    cwd=results
    Process Should Be Running    ${loader_type}
    ${wait}=    Wait Until Keyword Succeeds    120x    10minute    Wait For Process    ${loader_type}
    Should Be Equal As Integers    ${result.rc}    0
    Wait Until Keyword Succeeds    120x    10minute    Process Should Be Stopped    ${loader_type}
    Sleep    60s
    ${loader_Text_File_Content}    Get File    ${dir_path}/results/${loader_type}.txt
    Run Keyword If    '${loader_type}' == 'live'    Should Contain    ${loader_Text_File_Content}    N-Quads:
    ...    ELSE    Run Keywords    Should Contain    ${loader_Text_File_Content}    100.00%
    ...    AND    Verify Bulk Loader output generated    ${dir_path}/results/out/0/p
    ...    AND    Start Dgraph Alpha for bulk loader    ${dir_path}/results/out/0/p
    ...    AND    End Aplha Process    true

Execute Parallel Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" and "loader_type" perform live/bulk loader.
    ...    rdf_filename, schema_filename ,loader_type- "live"/"bulk"
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${value}=       Get Tls Value
    @{loader_type}=       Create List       live       bulk
    FOR    ${i}    IN    @{loader_type}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel  ${i}
        ${conf_live_command}=        Get Dgraph Loader Command    ${dir_path}/test_data/datasets/${rdf_filename}    ${dir_path}/test_data/datasets/${schema_filename}       ${i}
        ${result_loader}=      Run Keyword If      "${value}"=="True"       Process.start Process    ${conf_live_command}    alias=${loader_alias}    stdout=${loader_alias}.txt    shell=yes    cwd=results
        ...     ELSE    Process.start Process    dgraph    ${i}    -f    ${dir_path}/test_data/datasets/${rdf_filename}    -s    ${dir_path}/test_data/datasets/${schema_filename}    alias=${loader_alias}    stdout=${loader_alias}.txt    shell=yes    cwd=results
        Process Should Be Running    ${loader_alias}
    END
    FOR    ${i}    IN    @{loader_type}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel  ${i}
        ${wait}=    Wait For Process    handle=${loader_alias}
        Wait Until Keyword Succeeds    120x    10minute    Process Should Be Stopped    handle=${loader_alias}
        Sleep    60s
        ${loader_Text_File_Content}    Get File    ${dir_path}/results/${loader_alias}.txt
        Run Keyword If    '${i}' == 'live'    Should Contain    ${loader_Text_File_Content}    N-Quads:
        ...    ELSE    Run Keywords    Should Contain    ${loader_Text_File_Content}    100.00%
        ...    AND    Verify Bulk Loader output generated    ${dir_path}/results/out/0/p
        ...    AND    Start Dgraph Alpha for bulk loader    ${dir_path}/results/out/0/p
        ...    AND    End Aplha Process    true
    END

Execute Multiple Parallel Live Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}    ${num_threads}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" and "num_threads" perform multiple parallel live loading.
    ...    rdf_filename, schema_filename , num_threads
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${value}=       Get Tls Value
    FOR    ${i}    IN RANGE   ${num_threads}
        Log    Running thread -- ${i}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    live    ${i}
        ${conf_live_command}=        Get Dgraph Loader Command    ${dir_path}/test_data/datasets/${rdf_filename}    ${dir_path}/test_data/datasets/${schema_filename}       live
        ${result_loader}=      Run Keyword If      "${value}"=="True"       Process.start Process    ${conf_live_command}    alias=${loader_alias}    stdout=${loader_alias}.txt    shell=yes    cwd=results
        ...     ELSE    Process.start Process    dgraph    live    -f    ${dir_path}/test_data/datasets/${rdf_filename}    -s    ${dir_path}/test_data/datasets/${schema_filename}    alias=${loader_alias}    stdout=${loader_alias}.txt    shell=yes    cwd=results
        Process Should Be Running    ${loader_alias}
        Sleep    50s
    END
    FOR    ${i}    IN RANGE   ${num_threads}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    live    ${i}
        ${wait}=    Wait For Process    handle=${loader_alias}
        Process Should Be Stopped    handle=${loader_alias}
        Sleep    60s
        ${loader_Text_File_Content}    Grep File    ${dir_path}/results/${loader_alias}.txt    Number of N-Quads processed
        Should Contain    ${loader_Text_File_Content}    Number of N-Quads processed
    END

Execute Loader with rdf and schema parameters with configurations
[Arguments]    ${rdf_filename}    ${schema_filename}    ${loader_type}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" and "loader_type" perform live/bulk loader.
    ...    rdf_filename, schema_filename ,loader_type- "live"/"bulk"
    Run Keyword If    Get Tls Value    Get Dgraph Live Loader Command    ${dir_path}/test_data/datasets/${rdf_filename}    ${dir_path}/test_data/datasets/${schema_filename}
    # Backup Keywords

Create NFS Backup
    [Arguments]    ${url}    ${appenders}    ${is_clear_folder}
    [Documentation]    Accepts params: "{URL}","{appenders}" & "{is_clear_folder}"
    ...    Keyword to create a NFS backup i.e to save backup to local folder
    ${root_path}=    normalize path    ${CURDIR}/..
    ${backup_path}=    Join Path    ${root_path}/backup
    Run Keyword If    '${is_clear_folder}' == 'full'    clear all the folder in a directory    ${backup_path}
    connect request server    ${url}
    ${res}=    Post Nfs Backup Restore Command    ${appenders}    ${backup_path}    backup
    log    ${res.text}
    Verify file exists in a directory with parent folder name    ${backup_path}
    # Restore Keywords

Perform a restore on backup
    [Arguments]    ${url}
    [Documentation]    Performs an restore operation on the default location i.e "backup" dir.
    ${root_dir}=    normalize path    ${CURDIR}/..
    ${path}=    Join Path    ${root_dir}/backup
    @{dirs_backup}=    List Directories In Directory    ${path}
    ${restore_dir}=    Set Variable    ${dirs_backup}[0]
    ${restore_dir}=    Join Path    ${root_dir}/backup/${restore_dir}
    ${result_restore}=    Run Keyword If    "https" in "${url}"    Post Nfs Backup Restore Command    /admin    ${restore_dir}    restore
    ...    ELSE    Run Keywords    Start Process    dgraph    restore    -p    ${restore_dir}    -l    ${restore_dir}    -z    localhost:5080    alias=restore    stdout=restorebackup.txt    shell=yes    cwd=results
    ...    AND    Process Should Be Running    zero
    ...    AND    Process Should Be Running    alpha
    ...    AND    Process Should Be Running    restore
    ...    AND    Wait For Process    restore
    ...    AND    Process Should Be Stopped    restore
    ...    AND    Sleep    5s
    ...    AND    Verify retore file Content in results folder    restorebackup    ${restore_dir}

Perform a restore on backup present at other location
    [Arguments]    ${url}    ${path}
    [Documentation]    Performs an restore operation on the other location i.e "{path}" dir.
    @{dirs_backup}=    List Directories In Directory    ${path}
    ${restore_dir}=    Set Variable    ${dirs_backup}[0]
    ${restore_dir}=    Join Path    ${root_dir}/backup/${restore_dir}
    ${result_restore}=    Run Keyword If    "https" in "${url}"    Post Nfs Backup Restore Command    /admin    ${restore_dir}    restore
    ...    ELSE    Run Keywords    Start Process    dgraph    restore    -p    ${restore_dir}    -l    ${restore_dir}    -z    localhost:5080    alias=restore    stdout=restorebackup.txt    shell=yes    cwd=results
    ...    AND    Process Should Be Running    zero
    ...    AND    Process Should Be Running    alpha
    ...    AND    Process Should Be Running    restore
    ...    AND    Wait For Process    restore
    ...    AND    Process Should Be Stopped    restore
    ...    AND    Sleep    5s
    ...    AND    Verify retore file Content in results folder    restorebackup    ${restore_dir}
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
    [Arguments]    ${path}
    [Documentation]    Keyword to verify bulk loader files output
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
    Run Keyword If    ${list_size}>0    Empty Directory    ${path}

Create Directory
    [Arguments]    ${path}
    [Documentation]    Keyword to create a directory
    Create Directory    ${path}

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
    [Arguments]    ${file_name}    @{context}
    [Documentation]    Keyword for checking content in .txt files generated in results folder
    ...    [Arguments] -> "file_name" -file name ex: alpha for alpha.txt | "cotent" -content you want to check in file
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${file_context}=    Get File    ${dir_path}/results/${file_name}.txt
    Should Contain Any    ${file_context}    @{context}
