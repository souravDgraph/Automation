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
    Run Keyword And Return If    '${platform}' == 'docker'    Start Dgraph In Docker
    ${zero_command}    Generate Dgraph Zero Cli Command
    ${result_z}=    Process.start Process    ${zero_command}    alias=zero    cwd=results    shell=True    stdout=zero.txt
    Process Should Be Running    zero
    Wait For Process    timeout=10 s    on_timeout=continue
    ${alpha_command}    Generate Dgraph Alpha Cli Command
    ${result_a}=    Process.start Process    ${alpha_command}    alias=alpha    stdout=alpha.txt    cwd=results    shell=True
    Process Should Be Running    alpha
    Wait For Process    timeout=10 s    on_timeout=continue

Start Dgraph In Docker
    [Documentation]    Start Dgraph alpha and Zero process in Helm with cwd pointing to results folder.
    # Dgraph alpha and zero command
    ${dir_path}=    normalize path    ${CURDIR}/..
    log    ${dir_path}
    ${result_docker}=    Process.run Process    docker    --version    alias=docker    stdout=docker.txt    cwd=results    shell=True
    log    ${result_docker.stdout}
    Should Be Equal As Integers    ${result_docker.rc}    0
    ${result_docker_compose}=    Process.run Process    docker-compose    --version    alias=docker_compose    stdout=docker_compose.txt    cwd=results    shell=True
    Should Be Equal As Integers    ${result_docker_compose.rc}    0
    OperatingSystem.Create Directory    ${dir_path}/data
    Process.start Process    docker-compose    -f    ${dir_path}/conf/docker-compose.yml    up    alias=dc_up    cwd=results    shell=True    stdout=docker_compose_up.txt
    Process Should Be Running    dc_up
    Wait For Process    timeout=10 s    on_timeout=continue

Start Dgraph Zero
    [Arguments]    ${platform}
    [Documentation]    Start Dgraph Zero process
    Run Keyword And Return If    '${platform}' == 'docker'    Start Dgraph In Docker
    ${zero_command}    Generate Dgraph Zero Cli Command
    ${result_z}=    Process.start Process    ${zero_command}    alias=zero    cwd=results    shell=True    stdout=zero.txt    stderr=zero_err.txt
    Process Should Be Running    zero
    Wait For Process    timeout=10 s    on_timeout=continue

Start Dgraph Alpha
    [Arguments]    ${platform}
    [Documentation]    Start Dgraph alpha process.
    # Dgraph alpha and zero command
    Run Keyword And Return If    '${platform}' == 'docker'    Start Dgraph In Docker
    ${alpha_command}    Generate Dgraph Alpha Cli Command    alpha
    ${result_a}=    Process.start Process    ${alpha_command}    alias=alpha    stdout=alpha.txt    cwd=results    shell=True
    Process Should Be Running    alpha
    Wait For Process    timeout=20 s    on_timeout=continue

Start Dgraph Alpha for bulk loader
    [Arguments]    ${path}
    [Documentation]    Start Dgraph Alpha with bulk loader data
    ...    "path"- path of the backup file, "process_id" - process id trigged for this process.
    ${alpha_command}    Generate Dgraph Alpha Cli Command    ${path}
    ${result_a}=    Process.start Process    ${alpha_command}    alias=alpha    stdout=alpha.txt    stderr=alpha_err.txt    shell=True    cwd=results
    Process Should Be Running    alpha
    Wait For Process    timeout=20 s    on_timeout=continue
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
    Switch Process      zero
    Terminate Process   handle=zero
    Sleep    5s
    @{zero_context}    Create List    All done. Goodbye!
    Verify file Content in results folder    zero    @{zero_context}
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders

End Aplha Process
    [Arguments]    ${is_clear_folder}
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    Switch Process      alpha
    Terminate Process   handle=alpha
    Sleep    5s
    @{alpha_context}    Create List    Buffer flushed successfully.
    Verify file Content in results folder    alpha    @{alpha_context}
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders
    # Bulk/Live Loader

Execute Live Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" and "loader_type" perform live/bulk loader.
    ...    rdf_filename, schema_filename ,loader_type- "live"/"bulk"
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${value}=    Get Tls Value
    ${conf_live_command}=    Get Dgraph Loader Command    ${dir_path}/test_data/datasets/${rdf_filename}    ${dir_path}/test_data/datasets/${schema_filename}    live
    ${result_loader}=    Run Keyword If    "${value}"=="True"    Run Process    ${conf_live_command}    alias=live    stdout=live.txt    shell=True    cwd=results    timeout=10s    on_timeout=continue
    ...    ELSE    Run Process    dgraph    live    --alsologtostderr    -f    ${dir_path}/test_data/datasets/${rdf_filename}    -s    ${dir_path}/test_data/datasets/${schema_filename}    2>&1    alias=live    stdout=live.txt    cwd=results    timeout=100s    on_timeout=continue    shell=True
    Log    live.txt is log file name for this process.
    Switch Process    live
    Comment    Wait Until Keyword Succeeds    3x    10minute    Process Should Be Running    live
    Wait For Process    live    timeout=90min 30s
    Wait Until Keyword Succeeds    300x    10minute    Process Should Be Stopped    handle=live    error_message=live process is running.
    Sleep    100s
    ${loader_Text_File_Content}=    Grep File    ${dir_path}/results/live.txt    Number of N-Quads processed
    Log    ${loader_Text_File_Content}
    Should Contain    ${loader_Text_File_Content}    Number of N-Quads processed

Execute Bulk Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}
    [Documentation]    Keyword to accept two params "rdf_filename","schema_filename" perform bulk loader.
    ...    rdf_filename, schema_filename"bulk"
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${alpha_process_check}=    Is Process Running    alpha
    Run Keyword If    "${alpha_process_check}"=="True"    End Aplha Process    false
    ${value}=    Get Tls Value
    ${conf_bulk_command}=    Get Dgraph Loader Command    ${dir_path}/test_data/datasets/${rdf_filename}    ${dir_path}/test_data/datasets/${schema_filename}    bulk
    ${result_loader}=    Run Keyword If    "${value}"=="True"    Run Process    ${conf_bulk_command}    alias=bulk    stdout=bulk.txt    shell=True    cwd=results    timeout=10s    on_timeout=continue
    ...    ELSE    Run Process    dgraph    bulk    --alsologtostderr    -f    ${dir_path}/test_data/datasets/${rdf_filename}    -s    ${dir_path}/test_data/datasets/${schema_filename}    2>&1    alias=bulk    stdout=bulk.txt    cwd=results    timeout=100s    on_timeout=continue    shell=True
    Log    bulk.txt is log file name for this process.
    Wait For Process    bulk    timeout=90min 30s
    Wait Until Keyword Succeeds    300x    10minute    Process Should Be Stopped    handle=bulk    error_message=bulk process is running.
    Sleep    100s
    ${loader_Text_File_Content}=    Grep File    ${dir_path}/results/bulk.txt    100.00%
    Log    ${loader_Text_File_Content}
    Should Contain    ${loader_Text_File_Content}    100.00%
    Verify Bulk Loader output generated    ${dir_path}/results/out/0/p
    Start Dgraph Alpha for bulk loader    ${dir_path}/results/out/0/p
    End Aplha Process    false
    Start Dgraph Alpha    local

Execute Parallel Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" perform parallel live/bulk loader.
    ...    rdf_filename, schema_filename
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${value}=    Get Tls Value
    @{loader_type}=    Create List    live  bulk
    FOR    ${i}    IN    @{loader_type}
        ${alpha_process_check}=    Is Process Running    alpha
        Comment     Run Keyword If    "${alpha_process_check}"=="True" and "${i}" == "bulk"    End Aplha Process    false
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    ${i}
        ${conf_live_command}=    Get Dgraph Loader Command    ${dir_path}/test_data/datasets/${rdf_filename}    ${dir_path}/test_data/datasets/${schema_filename}    ${i}
        ${result_loader}=    Run Keyword If    "${value}"=="True"    Process.start Process    ${conf_live_command}    alias=${loader_alias}    stdout=${loader_alias}.txt    shell=True    cwd=results
        ...    ELSE    Process.start Process    dgraph    ${i}    -f    ${dir_path}/test_data/datasets/${rdf_filename}    -s    ${dir_path}/test_data/datasets/${schema_filename}    alias=${loader_alias}    stdout=${loader_alias}.txt    cwd=results
        Sleep    60s
        Log    ${loader_alias}.txt is log file name for this process.
        Comment     Switch Process    ${loader_alias}
        Comment     Wait Until Keyword Succeeds    3x    10minute    Process Should Be Stopped    ${loader_alias}
    END
    FOR    ${i}    IN    @{loader_type}
        ${alpha_process_check}=    Is Process Running    alpha
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    ${i}
        Switch Process    ${loader_alias}
        ${wait}=    Wait For Process    handle=${loader_alias}    timeout=90min 30s
        Wait Until Keyword Succeeds    300x    10minute    Process Should Be Stopped    ${loader_alias}    error_message=${loader_alias} process is running.
        Sleep    60s
        ${grep_context}=    Set Variable If    "${i}"=="bulk"    100.00%    Number of N-Quads processed
        ${loader_Text_File_Content}    Grep File    ${dir_path}/results/${loader_alias}.txt    ${grep_context}
        Run Keyword If    '${i}' == 'live'    Should Contain    ${loader_Text_File_Content}    ${grep_context}
        ...    ELSE    Run Keywords    Should Contain    ${loader_Text_File_Content}    100.00%
        ...    AND    Verify Bulk Loader output generated    ${dir_path}/results/out/0/p
        ...    AND    End Aplha Process    true
        ...    AND    Start Dgraph Alpha for bulk loader    ${dir_path}/results/out/0/p
        ...    AND    End Aplha Process    true
        ...    AND    Start Dgraph Alpha    local
    END
    ${alpha_process_check}=    Is Process Running    alpha

Execute Multiple Parallel Live Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}    ${num_threads}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" and "num_threads" perform multiple parallel live loading.
    ...    rdf_filename, schema_filename , num_threads
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${value}=    Get Tls Value
    FOR    ${i}    IN RANGE    ${num_threads}
        Log    Running thread -- ${i}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    live    ${i}
        ${conf_live_command}=    Get Dgraph Loader Command    ${dir_path}/test_data/datasets/${rdf_filename}    ${dir_path}/test_data/datasets/${schema_filename}    live
        ${result_loader}=    Run Keyword If    "${value}"=="True"    Process.start Process    ${conf_live_command}    alias=${loader_alias}    stdout=${loader_alias}.txt    shell=True    cwd=results
        ...    ELSE    Process.start Process    dgraph    live    -f    ${dir_path}/test_data/datasets/${rdf_filename}    -s    ${dir_path}/test_data/datasets/${schema_filename}    alias=${loader_alias}    stdout=${loader_alias}.txt    cwd=results
        Switch Process    ${loader_alias}
        Sleep    60s
        Comment    Wait Until Keyword Succeeds    3x    10minute    Process Should Be Running    ${loader_alias}
    END
    FOR    ${i}    IN RANGE    ${num_threads}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    live    ${i}
        Switch Process    ${loader_alias}
        ${wait}=    Wait For Process    handle=${loader_alias}    timeout=90min 30s
        Wait Until Keyword Succeeds    900x    5minute    Process Should Be Stopped    ${loader_alias}    error_message=${loader_alias} process is running.
        Sleep    60s
        ${loader_Text_File_Content}    Grep File    ${dir_path}/results/${loader_alias}.txt    Number of N-Quads processed
        Should Contain    ${loader_Text_File_Content}    Number of N-Quads processed
    END

Create NFS Backup
    [Arguments]    ${is_clear_folder}
    [Documentation]    Accepts params: "{URL}","{appenders}" & "{is_clear_folder}"
    ...    Keyword to create a NFS backup i.e to save backup to local folder
    ${root_path}=    normalize path    ${CURDIR}/..
    ${backup_path}=    Join Path    ${root_path}/backup
    Run Keyword If    '${is_clear_folder}' == 'full'    clear all the folder in a directory    ${backup_path}
    connect request server
    ${res}=    Backup Using Admin    ${backup_path}
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
    ${tls_check}=    Get Tls Value
    ${result_restore}=    Run Keyword If    "${tls_check}" == "True"    Restore Using Admin    ${restore_dir}
    ...    ELSE    Run Keywords    Start Process    dgraph    restore    -p    ${restore_dir}    -l    ${restore_dir}    -z    localhost:5080    alias=restore    stdout=restorebackup.txt    cwd=results
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
    ${result_restore}=    Run Keyword If    "https" in "${url}"    Restore Using Admin    ${restore_dir}
    ...    ELSE    Run Keywords    Start Process    dgraph    restore    -p    ${restore_dir}    -l    ${restore_dir}    -z    localhost:5080    alias=restore    stdout=restorebackup.txt    cwd=results
    ...    AND    Process Should Be Running    zero
    ...    AND    Process Should Be Running    alpha
    ...    AND    Process Should Be Running    restore
    ...    AND    Wait For Process    restore
    ...    AND    Process Should Be Stopped    restore
    ...    AND    Sleep    5s
    ...    AND    Verify retore file Content in results folder    restorebackup    ${restore_dir}
    # Validations:

Verify restore file Content in results folder
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
    @{dir}    Create List    p    t    w    zw    out   alpha
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

Grip and Verify file Content in results folder
    [Arguments]    ${file_name}    ${grep_text}
    [Documentation]    Keyword for checking content in .txt files generated in results folder
    ...    [Arguments] -> "file_name" -file name ex: alpha for alpha.txt | "cotent" -content you want to check in file
    ${grep_file}    Grep File    ${dir_path}/results/${file_name}.txt    ${grep_text}
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${file_context}=    Get File    ${grep_file}
    Should Contain    ${file_context}    ${grep_text}
