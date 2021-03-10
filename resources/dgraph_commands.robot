*** Settings ***
Library           OperatingSystem
Library           Process
Library           Dgraph
Library           JSONLibrary
Library           String
Library           Collections

*** Variables ***
${is_latest}
${docker_exe_string}

*** Keywords ***
Start Dgraph
    [Documentation]    Start Dgraph alpha and Zero process with cwd pointing to results folder.
    # Dgraph alpha and zero command
    ${zero_command}    Generate Dgraph Zero Cli Command
    ${result_z}=    Process.start Process    ${zero_command}    alias=zero    cwd=results    shell=True    stdout=zero.txt      stderr=zero_err.txt
    Process Should Be Running    zero
    Wait For Process    timeout=10 s    on_timeout=continue
    ${alpha_command}    Generate Dgraph Alpha Cli Command
    ${result_a}=    Process.start Process    ${alpha_command}    alias=alpha    stdout=alpha.txt    cwd=results    shell=True       stderr=alpha_err.txt
    Process Should Be Running    alpha
    Wait For Process    timeout=10 s    on_timeout=continue
    ${version}=     Get Dgraph Details      Dgraph version
    ${branch}=     Get Dgraph Details      Branch
    ${version}=  Set Variable If      'release' in  '${branch}'    Replace String     ${branch}      release/    ${EMPTY}
    ${check}=   check dgraph version    ${version}
    Set Suite Variable      ${is_latest}    ${check}

Start Dgraph Ludicrous Mode
    [Arguments]
    [Documentation]    Start Dgraph alpha and Zero process with cwd pointing to results folder.
    # Dgraph alpha and zero command
    ${zero_command}    Generate Dgraph Zero Cli Command
    ${result_z}=    Process.start Process    ${zero_command}    alias=zero    cwd=results    shell=True    stdout=zero.txt      stderr=zero_err.txt
    Process Should Be Running    zero
    Wait For Process    timeout=10 s    on_timeout=continue
    ${alpha_command}    Generate Dgraph Alpha Cli Command       ludicrous_mode=enabled
    ${result_a}=    Process.start Process    ${alpha_command}    alias=alpha    stdout=alpha.txt    cwd=results    shell=True       stderr=alpha_err.txt
    Process Should Be Running    alpha
    Wait For Process    timeout=10 s    on_timeout=continue
    ${version}=     Get Dgraph Version Details
    ${check}=   check dgraph version    ${version}
    Set Suite Variable      ${is_latest}    ${check}

Start Dgraph In Docker
    [Arguments]     ${folder_name}
    [Documentation]    Start Dgraph alpha and Zero process in Helm with cwd pointing to results folder.
    ${dir_path}=    normalize path    ${CURDIR}/..
    log    ${dir_path}
    ${result_docker}=    Process.Run Process    docker    --version    alias=docker    stdout=docker.txt    cwd=results    shell=True
    log    ${result_docker.stdout}
    ${result_docker_compose}=    Process.start Process    docker-compose    --version    alias=docker_compose    stdout=docker_compose.txt    cwd=results    shell=True
    OperatingSystem.Create Directory    ${dir_path}/data
    Process.start Process    docker-compose    -f    ${dir_path}/conf/${folder_name}/docker-compose.yml    up    alias=dc_up    cwd=results    shell=True    stdout=docker_compose_up.txt
    Process Should Be Running    dc_up
    Wait For Process    timeout=40 s    on_timeout=continue
    Set Dgraph Version from docker  ${folder_name}

End Docker Execution
    [Arguments]     ${folder_name}      ${is_clear_folder}
    Terminate All Processes
    ${dir_path}=    normalize path    ${CURDIR}/..
    Process.start Process    docker-compose    -f    ${dir_path}/conf/${folder_name}/docker-compose.yml    down    alias=dc_down    cwd=results    shell=True    stdout=docker_compose_down.txt
    Process Should Be Running    dc_down
    Wait For Process    timeout=10 s    on_timeout=continue
    @{dir}    Create List    p    t    w    out    alpha
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up list of folders in results dir    @{dir}

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
    ${result_a}=    Process.start Process    ${alpha_command}    alias=alpha    stdout=alpha_bulk.txt    stderr=alpha_bulk_err.txt    shell=True    cwd=results
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
    @{alpha_context}    Create List    Buffer flushed successfully.     Raft node done.    Operation completed with id: opRestore
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders
    Verify file Content in results folder    zero    @{zero_context}
    Verify file Content in results folder    alpha    @{alpha_context}
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders

End Zero Process
    [Arguments]    ${is_clear_folder}
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    Switch Process    zero
    Terminate Process    handle=zero
    Sleep    5s
    @{zero_context}    Create List    All done. Goodbye!
    Verify file Content in results folder    zero    @{zero_context}
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders

End Aplha Process
    [Arguments]    ${is_clear_folder}
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    Switch Process    alpha
    Terminate Process    handle=alpha
    Sleep    5s
    @{alpha_context}    Create List    Buffer flushed successfully.     Raft node done.
    Verify file Content in results folder    alpha    @{alpha_context}
    @{dir}    Create List    p    t    w    out    alpha
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up list of folders in results dir    @{dir}

Get Dgraph Details
    [Documentation]  Keyword to get dgraph details from dgraph version
    [Arguments]     ${key}
    Start Process   dgraph  version     alias=version    stdout=dgraph_version.txt    stderr=dgraph_version_err.txt    shell=True    cwd=results
    Wait For Process    timeout=30 s
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${dgraph_Text_File_Content}=    Grep File    ${dir_path}/results/dgraph_version.txt     ${key}*
    ${key}     ${value}=    Split String    ${dgraph_Text_File_Content}     :
    ${value}=   Replace String  ${value}    ${space}     ${empty}
    [Return]    ${value}

Get Dgraph Docker Version Details
    [Documentation]  Keyword to get dgraph version details
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${dgraph_Text_File_Content}=    Grep File    ${dir_path}/results/dgraph_version.txt     Dgraph version*
    ${key}     ${value}=    Split String    ${dgraph_Text_File_Content}     :
    ${value}=   Replace String  ${value}    ${space}     ${empty}
    [Return]    ${value}

Get Dgraph Docker Branch Details
    [Documentation]  Keyword to get dgraph version details
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${dgraph_Text_File_Content}=    Grep File    ${dir_path}/results/dgraph_version.txt     Branch*
    ${key}     ${value}=    Split String    ${dgraph_Text_File_Content}     :
    ${value}=   Replace String  ${value}    ${space}     ${empty}
    [Return]    ${value}

Set Dgraph Version from docker
    [Arguments]     ${folder_name}
    [Documentation]     Keyword to get the dgraph version from docker
    ${docker_process}=     Run Process   docker       exec    ${folder_name}_zero0_1   dgraph  version     alias=version   stdout=dgraph_version.txt    shell=True    cwd=results
    ${version}=     Get Dgraph Docker Version Details
    ${branch}=      Get Dgraph Docker Branch Details
    ${version}=  Set Variable If      'release' in  '${branch}'    Replace String     ${branch}      release/    ${EMPTY}
    ${check}=   Set Execution To Docker     ${version}      ${branch}
    Set Suite Variable      ${is_latest}        ${check}
    Set Suite Variable      ${docker_exe_string}    docker exec ${folder_name}_alpha0_1

Execute Live Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" and "loader_type" perform live/bulk loader.
    ...    rdf_filename, schema_filename ,loader_type- "live"/"bulk"
    ${dir_path}=    normalize path    ${CURDIR}/..
    Trigger Loader Process      live     ${rdf_filename}    ${schema_filename}    live
    Verify process to be stopped    live
    ${loader_Text_File_Content}=    Grep File    ${dir_path}/results/live.txt    N-Quads processed per second
    Log    ${loader_Text_File_Content}
    Should Contain    ${loader_Text_File_Content}    N-Quads processed per second

Execute Bulk Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}
    [Documentation]    Keyword to accept two params "rdf_filename","schema_filename" perform bulk loader.
    ...    rdf_filename, schema_filename"bulk"
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${alpha_process_check}=    Is Process Running    alpha
    Run Keyword If    "${alpha_process_check}"=="True"    End Aplha Process    false
    Trigger Loader Process      bulk     ${rdf_filename}    ${schema_filename}    bulk
    Verify process to be stopped    bulk
    ${loader_Text_File_Content}=    Grep File    ${dir_path}/results/bulk.txt    100.00%
    Log    ${loader_Text_File_Content}
    Verify Bulk Process     ${loader_Text_File_Content}

Trigger Loader Process
    [Arguments]     ${loader_alias}     ${rdf_filename}    ${schema_filename}     ${loader_name}
    [Documentation]     Keyword to only trigger live loader process
    ${dir_path}=    normalize path    ${CURDIR}/..
    log     ${docker_exe_string}
    ${path}=    Set Variable If      '${docker_exe_string}' != ''   /Automation     ${dir_path}
    ${conf_loder_command}=    Get Dgraph Loader Command    ${path}/test_data/datasets/${rdf_filename}    ${path}/test_data/datasets/${schema_filename}       ${loader_name}     is_latest_version=${is_latest}  docker_string=${docker_exe_string}
    ${result_loader}=   Process.start Process    ${conf_loder_command}    alias=${loader_alias}    stdout=${loader_alias}.txt    stderr=${loader_alias}_err.txt    shell=True    cwd=results

Verify Bulk Process
    [Arguments]     ${loader_Text_File_Content}
    [Documentation]     Keyword to verify bulk loader output
    ${dir_path}=    normalize path    ${CURDIR}/..
    Should Contain    ${loader_Text_File_Content}    100.00%
    Verify Bulk Loader output generated    ${dir_path}/results/out/0/p
    End Aplha Process    true
    Start Dgraph Alpha for bulk loader    ${dir_path}/results/out/0/p
    End Aplha Process    true
    Start Dgraph Alpha    local

Execute Parallel Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" perform parallel live/bulk loader.
    ...    rdf_filename, schema_filename
    ${dir_path}=    normalize path    ${CURDIR}/..
    @{loader_type}=    Create List    live    bulk
    FOR    ${i}    IN    @{loader_type}
        ${alpha_process_check}=    Is Process Running    alpha
        Comment    Run Keyword If    "${alpha_process_check}"=="True" and "${i}" == "bulk"    End Aplha Process    false
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    ${i}
        Trigger Loader Process     ${loader_alias}     ${rdf_filename}    ${schema_filename}    ${i}
        Wait For Process    timeout=30 s
        Log    ${loader_alias}.txt is log file name for this process.
    END
    FOR    ${i}    IN    @{loader_type}
        ${alpha_process_check}=    Is Process Running    alpha
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    ${i}
        ${result_check}=    Run Keyword And Return Status    Wait Until Keyword Succeeds    3x    5minute    Grep and Verify file Content in results folder    ${loader_alias}    Error while processing schema file
        Run Keyword And Return If    "${result_check}" == "True"    Fail    Error while processing schema file
        Verify process to be stopped    ${loader_alias}
        ${grep_context}=    Set Variable If    "${i}"=="bulk"    100.00%    N-Quads processed per second
        ${loader_Text_File_Content}    Grep File    ${dir_path}/results/${loader_alias}.txt    ${grep_context}
        Run Keyword If    '${i}' == 'live'    Should Contain    ${loader_Text_File_Content}    ${grep_context}
        ...    ELSE     Verify Bulk Process     ${loader_Text_File_Content}
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
        Trigger Loader Process      ${loader_alias}     ${rdf_filename}    ${schema_filename}    live
        Sleep    60s
        Check if parallel process is triggered      ${loader_alias}     ${rdf_filename}    ${schema_filename}       live
        Comment    Wait Until Keyword Succeeds    3x    10minute    Process Should Be Running    ${loader_alias}
    END
    FOR    ${i}    IN RANGE    ${num_threads}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    live    ${i}
        ${result_check}=    Run Keyword And Return Status    Grep and Verify file Content in results folder    ${loader_alias}    Error while processing schema file
        Run Keyword And Return If    "${result_check}" == "PASS"    Fail    Error while processing schema file
        Verify process to be stopped    ${loader_alias}
        Grep and Verify file Content in results folder    ${loader_alias}    N-Quads processed per second
    END

Execute Increment Command
    [Arguments]     ${num_threads}      ${alpha_offset}
    [Documentation]  Keyword to verify increment..
    FOR    ${i}    IN RANGE    ${num_threads}
        ${alpha_offset}    Set Variable If     ${i}>=1     ${alpha_offset}      0
        ${inc_alias}=    Catenate    SEPARATOR=_    parallel    increment    ${i}
        ${inc_command}  Get dgraph increment command    is_latest_version=${is_latest}  docker_string=${docker_exe_string}      alpha_offset=${alpha_offset}
        ${result_i}=    Process.start Process   ${inc_command}    alias=${inc_alias}    cwd=results/inc_logs    shell=True    stdout=${inc_alias}.txt    stderr=${inc_alias}_err.txt
        Wait For Process    ${inc_alias}    timeout=10 s
    END
    FOR    ${i}    IN RANGE    ${num_threads}
        ${dir_path}=    normalize path    ${CURDIR}/..
        ${inc_alias}=    Catenate    SEPARATOR=_    parallel    increment    ${i}
        Terminate Process   ${inc_alias}
        Sleep   5s
        ${grep_file}=    Grep File    ${dir_path}/results/inc_logs/${inc_alias}.txt    1
        Should Contain    ${grep_file}    1
    END

Create NFS Backup
    [Arguments]    ${is_clear_folder}
    [Documentation]    Accepts params: "{is_clear_folder}"
    ...    Keyword to create a NFS backup i.e to save backup to local folder
    ${root_path}=    normalize path    ${CURDIR}/..
    ${backup_path}=    Join Path    ${root_path}/backup
    Run Keyword If    '${is_clear_folder}' == 'full'    clear all the folder in a directory    ${backup_path}
    connect request server
    ${res}=    Backup Using Admin    ${backup_path}
    log    ${res.text}
    Verify file exists in a directory with parent folder name    ${backup_path}

Export NFS data using admin endpoint
    [Arguments]    ${data_type}     ${is_clear_folder}
    [Documentation]    Accepts params: "{is_clear_folder}", "{data_type}"
    ...    Keyword to export dgraph data to either json/rdf format in local
    ${root_path}=    normalize path    ${CURDIR}/..
    ${export_path}=    Join Path    ${root_path}/export
    Run Keyword If    '${is_clear_folder}' == 'true'    clear all the folder in a directory    ${export_path}
    connect request server
    ${res}=    Export Nfs Data Admin    data_format=${data_type}    destination=${export_path}
    log    ${res.text}
    Verify file exists in a directory with parent folder name    ${export_path}


Perform a restore on backup
    [Documentation]    Performs an restore operation on the default location i.e "backup" dir.
    Connect request server
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
    ...    AND    Verify Restore File Content In Results Folder    restorebackup    ${restore_dir}

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
    ...    AND    Verify Restore File Content In Results Folder    restorebackup    ${restore_dir}
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
    @{dir}    Create List    p    t    w    zw    out    alpha
    FOR    ${foldername}    IN    @{dir}
        Remove Directory    ${curr_dir}/results/${foldername}    recursive=True
    END
    Log    "All the folders created by alpha and zero were deleted."

clean up list of folders in results dir
    [Arguments]    @{dir}
    [Documentation]    Keyword to clear up the dgraph alpha and zero folder created.
    ${curr_dir}=    Normalize Path    ${CURDIR}/..
    FOR    ${foldername}    IN    @{dir}
        Remove Directory    ${curr_dir}/results/${foldername}    recursive=True
    END
    Log    "All the folders were deleted."

clean up a perticular folders
    [Arguments]    ${folder_name}
    [Documentation]    Keyword to clear up a perticular folder created.
    ${curr_dir}=    Normalize Path    ${CURDIR}/..
    @{dir}    Create List    p    t    w    zw    out    alpha
    Remove Directory    ${curr_dir}/results/${folder_name}    recursive=True
    Log    " ${folder_name} folder is deleted."

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

Grep and Verify file Content in results folder
    [Arguments]    ${file_name}    ${grep_text}
    [Documentation]    Keyword for grepping and checking content in .txt files generated in results folder
    ...    [Arguments] -> "file_name" -file name ex: alpha for alpha.txt | "cotent" -content you want to check in file
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${grep_file}=    Grep File    ${dir_path}/results/${file_name}.txt    ${grep_text}
    Should Contain    ${grep_file}    ${grep_text}

Monitor zero and alpha process
    [Documentation]    Keyword to monitor zero and alpha process to run
    ${alpha_process_check}=    Is Process Running    alpha
    ${zero_process_check}=    Is Process Running    zero
    Run Keyword If    "${alpha_process_check}"=="False"    Start Dgraph Alpha    false
    Run Keyword If    "${zero_process_check}"=="False"    Start Dgraph Zero    false

Monitor health and state check
    [Documentation]   Keyword to check the health and state of the connection.
    connect request server
    Monitor health check
    Monitor State Check

Monitor health check
    [Documentation]   Keyword to check the health of the connection.
    connect request server
    ${appender}=    Set Variable      /health
    ${response}=    Health Check    ${appender}
    log     ${response}
    Run Keyword If      "${response}" != "healthy"      Fail    Health check is un-healthy

Monitor State Check
    [Documentation]  Keyword to check the state of the process.
    connect request server
    ${state_resposne}=  State Check     /state
    ${leader}=    Get Value From Json   ${state_resposne}   $..members..leader
    ${am_dead}=    Get Value From Json   ${state_resposne}   $..members..amDead
    Should Be Equal As Strings  ${leader[0]}   True
    Should Be Equal As Strings  ${am_dead[0]}   False

Verify process to be stopped
    [Arguments]    ${process_alias}
    [Documentation]    Keyword to check if the process is still running and wait till process completes.
    log    Process which is runing ${process_alias}
    ${process_check}=    Is Process Running    ${process_alias}
    Sleep   30s
    Run Keyword If    '${process_check}'=='False'    Return From Keyword
    FOR    ${i}    IN RANGE    99999
        log    ${i}
        Wait For Process    ${process_alias}
        ${process_check}=    Is Process Running    ${process_alias}
        Exit For Loop If    '${process_check}'=='False'
    END
    Log    ${process_alias} Process is stopped
    Comment    Wait Until Keyword Succeeds    600x    5minute    Process Should Be Stopped    handle=${process_alias}    error_message=${error_message} is still running

Build Dgraph Version
    [Arguments]    ${version}
    [Documentation]    Keyword builds Dgraph to a specific version
    ${rc}    ${output}=    OperatingSystem.Remove Directory    dgraph    recursive=True
    ${rc}    ${output}=    OperatingSystem.Run And Return Rc And Output    pwd
    ${rc}    ${clone}=    OperatingSystem.Run And Return Rc And Output    git clone https://github.com/dgraph-io/dgraph.git
    log    ${clone}
    ${checkout_output}=    Process.Run Process    git    checkout    ${version}    alias=checkout_alias    cwd=dgraph    shell=True
    log    ${checkout_output}
    Should Be Equal As Integers    ${checkout_output.rc}    0
    ${make_output}=    Process.Run Process    make    install    alias=make_alias    cwd=dgraph    shell=True
    log    ${make_output}
    Should Be Equal As Integers    ${make_output.rc}    0
    ${output} =    OperatingSystem.Run    dgraph version
    ${version_output} =    Get Lines Containing String    ${output}    version    case_insensitive
    log    ${version_output}
    should contain    ${version_output}    ${version}

Check if parallel process is triggered
    [Arguments]    ${loader_alias}     ${rdf_filename}    ${schema_filename}  ${loader_name}
    [Documentation]     Keyword to retry live loading for couple of times.
    ${result_check}=    Run Keyword And Return Status   Grep and Verify file Content in results folder      ${loader_alias}    Please retry operation
    ${process_check}=    Is Process Running    ${loader_alias}
    log  ${loader_alias}
    Run Keyword If    "${process_check}"=="True" and "${result_check}"=="True"    Terminate Process     ${loader_alias}
    Run Keyword If  '${result_check}'=='True'  Run Keywords     Sleep   30s
    ...     AND     Trigger Loader Process     ${loader_alias}     ${rdf_filename}    ${schema_filename}   ${loader_name}
    ...     AND     Check if parallel process is triggered      ${loader_alias}     ${rdf_filename}    ${schema_filename}   ${loader_name}