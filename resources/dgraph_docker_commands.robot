*** Settings ***
Library           OperatingSystem
Library           Process
Library           Dgraph
Library           JSONLibrary
Library           String
Library           Collections
Library           DateTime

*** Variables ***
${DGRAPH_LATEST_VERSION_CHECK}
${DOCKER_STRING}
${DOCKER_COMPOSE_UP_COUNT}   0
${GLOBAL_IS_DOCKER_EXE}     ${FALSE}
${GLOBAL_BACKUP_DIR_FOLDER}
${GLOBAL_YAML_COUNTER}  1

*** Keywords ***

Start Dgraph n-node In Docker
    [Documentation]  Keyword to start dgraph in docker setup.
    [Arguments]     ${no_of_alphas}     ${no_of_zeros}    ${dgraph_version}     ${container_name}
    Create Backup Folder
    ${dir_path}=    normalize path    ${CURDIR}/..
    log    ${dir_path}
    ${docker_command}   get zero and alpha docker cli command     bulk_path=${bulk_data_path}      container_name=${container_name}     dgraph_version=${dgraph_version}     zero_count=${no_of_zeros}   alpha_count=${no_of_alphas}
    ${result_docker}=    Start Process    ./${docker_command}       alias=gen_file  stderr=gen_file_err.txt   cwd=utilities    shell=True
    ${docker_compose_up}=    Start Process    docker-compose    up       alias=docker_compose_up  stdout=docker_compose_up.txt    stderr=docker_compose_up_err.txt    cwd=conf    shell=True
    Wait For Process    timeout=30 s    on_timeout=continue
    Set Dgraph Version from docker      ${container_name}
    Set Suite Variable  ${GLOBAL_IS_DOCKER_EXE}     ${TRUE}

Start Dgraph 2-node In Docker with bulk data
    [Documentation]  Keyword to start dgraph with alpha pointing to bulk loader data in docker setup.
    [Arguments]    ${dgraph_version}     ${container_name}      ${bulk_data_path}
    Create Backup Folder
    ${dir_path}=    normalize path    ${CURDIR}/..
    log    ${dir_path}
    ${docker_command}   get zero and alpha docker cli command     bulk_path=${bulk_data_path}      container_name=${container_name}     dgraph_version=${dgraph_version}     zero_count=1   alpha_count=1
    ${result_docker}=    Start Process    ./${docker_command}       alias=gen_file  stdout=gen_file.txt    stderr=gen_file_err.txt    cwd=utilities    shell=True
    ${docker_compose_up}=    Start Process    docker-compose    up       alias=docker_compose_up  stdout=docker_compose_up_${DOCKER_COMPOSE_UP_COUNT}.txt    stderr=docker_compose_up_err_${DOCKER_COMPOSE_UP_COUNT}.txt    cwd=results    shell=True
    Wait For Process    timeout=30 s    on_timeout=continue
    Set Dgraph Version from docker      ${container_name}
    ${DOCKER_COMPOSE_UP_COUNT}  Evaluate    ${DOCKER_COMPOSE_UP_COUNT}+1
    Set Suite Variable  ${DOCKER_COMPOSE_UP_COUNT}  ${DOCKER_COMPOSE_UP_COUNT}
    Set Suite Variable  ${GLOBAL_IS_DOCKER_EXE}     ${TRUE}

Retrigger Docker File
    [Arguments]    ${dgraph_version}     ${container_name}      ${bulk_data_path}      ${is_clear_folder}
    [Documentation]     Monitor Zero and Alpha for docker execution
    Run Keyword And Continue On Failure     End Docker Execution    ${container_name}
    IF    ${is_clear_folder}
        Backup Yaml File
        Backup directories created while execution
    END
    Start Dgraph 2-node In Docker with bulk data  ${dgraph_version}     ${container_name}      ${bulk_data_path}

End Docker Execution
    [Documentation]  Keyword to end docker execution
    [Arguments]     ${container_name}
    ${dir_path}=    normalize path    ${CURDIR}/..
    Terminate All Processes
    ${result_docker}=    Start Process    docker-compose    down       alias=docker_compose_down  stdout=docker_compose_down.txt    stderr=docker_compose_down_err.txt    cwd=results    shell=True
    Wait For Process    timeout=20 s    on_timeout=continue
    @{compose_error_context}  Create List     Error: unknown flag     panic: runtime error:   runtime.goexit
    ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify alpha and zero contents in results folder    docker_compose_up    @{compose_error_context}
    Run Keyword And Return If      ${passed}       Fail       Captured errors in docker compose
    @{compose_context}  Create List     Gracefully stopping...      Buffer flushed successfully.
    Wait Until Keyword Succeeds     5x    5 sec   Verify alpha and zero contents in results folder    docker_compose_up    @{compose_context}

Terminate Docker Execution and Create Backup of Dgraph Execution
    [Arguments]     ${container_name}      ${is_clear_folder}
    Run Keyword And Continue On Failure    END DOCKER EXECUTION     ${container_name}
    Backup alpha and zero logs
    Backup Yaml File
    Backup directories created while execution
    Run Keyword If    ${is_clear_folder}    clean up dgraph folders

Monitor health and state check
    [Documentation]   Keyword to check the health and state of the connection.
    Monitor health check
    Monitor State Check

Monitor health check
    [Documentation]   Keyword to check the health of the connection.
    connect request server  is_docker=${GLOBAL_IS_DOCKER_EXE}
    ${response}=    Health status Check    /health
    log     ${response}
    Run Keyword If      "${response}" != "healthy"      Fail    Health check is un-healthy

Monitor State Check
    [Documentation]  Keyword to check the state of the process.
    connect request server    is_docker=${GLOBAL_IS_DOCKER_EXE}
    ${state_resposne}=  State Check     /state
    ${leader}=    Get Value From Json   ${state_resposne}   $..members..leader
    ${am_dead}=    Get Value From Json   ${state_resposne}   $..members..amDead
    Should Be Equal As Strings  ${leader[0]}   True
    Should Be Equal As Strings  ${am_dead[0]}   False

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
    [Arguments]     ${container_name}
    [Documentation]     Keyword to get the dgraph version from docker
    ${docker_process}=     Run Process   docker       exec    ${container_name}   dgraph  version     alias=version   stdout=dgraph_version.txt    shell=True    cwd=results
    ${version}=     Get Dgraph Docker Version Details
    ${branch}=      Get Dgraph Docker Branch Details
    ${version}=  Run Keyword If      'release' in '${branch}'      Replace String     ${branch}      release/    ${EMPTY}
    ...     ELSE    Set Variable    ${version}
    ${check}=   Set Execution To Docker     ${version}      ${branch}
    Set Suite Variable      ${DGRAPH_LATEST_VERSION_CHECK}        ${check}
    Set Suite Variable      ${DOCKER_STRING}    docker exec ${container_name}

Trigger Loader Process for Docker
    [Arguments]     ${loader_alias}     ${rdf_filename}    ${schema_filename}     ${loader_name}    ${zero_host}    ${alpha_host}
    [Documentation]     Keyword to only trigger live loader process
    ${dir_path}=    normalize path    ${CURDIR}/..
    log     ${DOCKER_STRING}
    ${path}=    Set Variable     ${dir_path}    
    ${out_dir}=    Set Variable IF     'bulk' in '${loader_alias}'     ${dir_path}/results/out   ${None}    
    ${conf_loder_command}=    Get Dgraph Loader Command    ${path}/test_data/datasets/${rdf_filename}    ${path}/test_data/datasets/${schema_filename}       ${loader_name}     is_latest_version=${DGRAPH_LATEST_VERSION_CHECK}  docker_string=${DOCKER_STRING}    zero_host_name=${zero_host}     alpha_host_name=${alpha_host}     out_dir=${out_dir}
    ${result_loader}=   Start Process    ${conf_loder_command}    alias=${loader_alias}    stdout=${loader_alias}.txt    stderr=${loader_alias}_err.txt    shell=True    cwd=results

Docker Execute Live Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}    ${zero_host}    ${alpha_host}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" perform live loader.
    ...    rdf_filename, schema_filename
    ${dir_path}=    normalize path    ${CURDIR}/..
    Trigger Loader Process for Docker     live     ${rdf_filename}    ${schema_filename}    live    ${zero_host}    ${alpha_host}
    Verify process to be stopped    live
    ${loader_Text_File_Content}=    Grep File    ${dir_path}/results/live.txt    N-Quads processed per second
    Log    ${loader_Text_File_Content}
    Should Contain    ${loader_Text_File_Content}    N-Quads processed per second

Docker Execute Bulk Loader for Docker with rdf and schema parameters
    [Arguments]    ${dgraph_version}     ${container_name}      ${rdf_filename}    ${schema_filename}   ${zero_host}
    [Documentation]    Keyword to accept two params "rdf_filename","schema_filename" perform bulk loader.
    ...    rdf_filename, schema_filename"bulk"
    ${dir_path}=    normalize path    ${CURDIR}/..
    Trigger Loader Process for Docker      bulk     ${rdf_filename}    ${schema_filename}    bulk   ${zero_host}    alpha_host_name=None
    Verify process to be stopped    bulk
    ${loader_Text_File_Content}=    Grep File    ${dir_path}/results/bulk.txt    Total:
    Log    ${loader_Text_File_Content}
    Docker Verify Bulk Process     ${dgraph_version}     ${container_name}       ${loader_Text_File_Content}

Docker Verify Live loader trigger properly or not
    [Documentation]  Keyword to verify live loader to trigger properly
    [Arguments]  ${loader_alias}    ${rdf_filename}    ${schema_filename}     ${loader_name}    ${zero_host}    ${alpha_host}
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${status}   Run Keyword And Return Status   Wait Until Keyword Succeeds    3x    10 sec    Grep and Verify file Content in results folder    ${loader_alias}    N-Quads:
    ${tcp_error}=    Run Keyword And Return Status   Wait Until Keyword Succeeds    2x    60 sec    Grep and Verify file Content in results folder    ${loader_alias}    Error while dialing dial tcp
    IF  ${status}==${FALSE} or ${tcp_error}
        ${retry_check}=    Run Keyword And Return Status   Wait Until Keyword Succeeds    2x    60 sec    Grep and Verify file Content in results folder    ${loader_alias}    Please retry
        Terminate Process   ${loader_alias}
        Trigger Loader Process for Docker     ${loader_alias}     ${rdf_filename}    ${schema_filename}     ${loader_name}     ${zero_host}    ${alpha_host}
        Wait For Process    ${loader_alias}    timeout=10 s
        @{alpha_error_context}  Create List     Error: unknown flag     panic: runtime error:   runtime.goexit      runtime.throw
        ${check}    Run Keyword And Return Status   verify alpha and zero contents in results folder   docker_compose_up    @{alpha_error_context}
        Run Keyword If   ${check}   FAIL    Found Issues in alpha during live load
        ${check}    Run Keyword And Return Status   Docker Verify Live loader trigger properly or not  ${loader_alias}     ${rdf_filename}    ${schema_filename}     ${loader_name}    ${zero_host}    ${alpha_host}
        Return From Keyword If   ${check}
        ...     ELSE    FAIL    Some issue with live loader
    END


Docker Verify Bulk Process
    [Arguments]     ${dgraph_version}     ${container_name}     ${loader_Text_File_Content}
    [Documentation]     Keyword to verify bulk loader output files generated along with
     ...    altering zero and alpha instances.
    ${dir_path}=    normalize path    ${CURDIR}/..
    Should Contain    ${loader_Text_File_Content}    Total:
    Verify Bulk Loader output generated    ${dir_path}/results/out/0/p
    End Docker Execution  ${container_name}
    @{dirs}     Create List     alpha1  zero1
    Backup Custom Directories Created While Execution  @{dirs}  
    Backup Yaml File
    Start Dgraph 2-node In Docker with bulk data    ${dgraph_version}     ${container_name}       ${dir_path}/results/out/0/p
    ${compose_file_number}   Evaluate    ${DOCKER_COMPOSE_UP_COUNT} - 1 
    Verify file Content in results folder  docker_compose_up_${compose_file_number}  ${dir_path}/results/out/0/p

Docker Execute Parallel Loader with rdf and schema parameters
    [Arguments]    ${dgraph_version}   ${container_name}      ${rdf_filename}     ${schema_filename}    ${zero_host}    ${alpha_host}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" perform parallel live/bulk loader.
    ...    rdf_filename, schema_filename
    ${dir_path}=    normalize path    ${CURDIR}/..
    @{loader_type}=    Create List    live    bulk
    FOR    ${i}    IN    @{loader_type}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    ${i}
        ${alpha_host}   Set Variable If     '${i}' == 'bulk'      ${None}     ${alpha_host}
        Trigger Loader Process for Docker     ${loader_alias}     ${rdf_filename}    ${schema_filename}    ${i}     ${zero_host}    ${alpha_host}
        Log    ${loader_alias}.txt is log file name for this process.
    END
    FOR    ${i}    IN    @{loader_type}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    ${i}
        IF  '${i}'=='live'
            Docker Verify Live loader trigger properly or not  ${loader_alias}     ${rdf_filename}    ${schema_filename}    live   ${zero_host}    ${alpha_host}
        END
        Verify process to be stopped    ${loader_alias}
        ${grep_context}=    Set Variable If    "${i}"=="bulk"    Total:    N-Quads processed per second
        ${loader_Text_File_Content}    Grep File    ${dir_path}/results/${loader_alias}.txt    ${grep_context}
        Run Keyword If    '${i}' == 'live'    Should Contain    ${loader_Text_File_Content}    ${grep_context}
        ...    ELSE     Docker Verify Bulk Process     ${dgraph_version}     ${container_name}       ${loader_Text_File_Content}
    END

Docker Execute Multiple Parallel Live Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}    ${num_threads}      ${zero_host}    ${alpha_host}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" and "num_threads" perform multiple parallel live loading.
    ...    rdf_filename, schema_filename , num_threads
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${value}=    Get Tls Value  is_docker=${GLOBAL_IS_DOCKER_EXE}
    FOR    ${i}    IN RANGE    ${num_threads}
        Log    Running thread -- ${i}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    live    ${i}
        Trigger Loader Process for Docker      ${loader_alias}     ${rdf_filename}    ${schema_filename}    live    ${zero_host}    ${alpha_host}
        Check if parallel process is triggered      ${loader_alias}     ${rdf_filename}    ${schema_filename}       live    ${zero_host}    ${alpha_host}
    END
    FOR    ${i}    IN RANGE    ${num_threads}
        Docker Verify Live loader trigger properly or not  ${loader_alias}    ${rdf_filename}    ${schema_filename}    live    ${zero_host}    ${alpha_host}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    live    ${i}
        Verify process to be stopped    ${loader_alias}
        Grep and Verify file Content in results folder    ${loader_alias}    N-Quads processed per second
    END

Check if parallel process is triggered
    [Arguments]    ${loader_alias}     ${rdf_filename}    ${schema_filename}  ${loader_name}    ${zero_host}    ${alpha_host}
    [Documentation]     Keyword to retry live loading for couple of times.
    ${result_check}=    Run Keyword And Return Status   Grep and Verify file Content in results folder      ${loader_alias}    Please retry operation
    ${process_check}=    Is Process Running    ${loader_alias}
    log  ${loader_alias}
    Run Keyword If    ${process_check} and ${result_check}    Terminate Process     ${loader_alias}
    Run Keyword If  ${result_check}  Run Keywords     Sleep   30s
    ...     AND     Trigger Loader Process     ${loader_alias}     ${rdf_filename}    ${schema_filename}   ${loader_name}   ${zero_host}    ${alpha_host}
    ...     AND     Check if parallel process is triggered      ${loader_alias}     ${rdf_filename}    ${schema_filename}   ${loader_name}  ${zero_host}    ${alpha_host}

Docker Execute Increment Command
    [Arguments]     ${num_threads}
    [Documentation]  Keyword to verify increment..
    FOR    ${i}    IN RANGE    ${num_threads}
        ${alpha_count}  Evaluate        ${i} + 1
        ${inc_alias}=    Catenate    SEPARATOR=_    parallel    increment    ${i}
        ${inc_command}  Get dgraph increment command    is_latest_version=${DGRAPH_LATEST_VERSION_CHECK}  docker_string=${DOCKER_STRING}     alpha_host_name=alpha${alpha_count}
        ${result_i}=    Process.start Process   ${inc_command}    alias=${inc_alias}    cwd=results    shell=True    stdout=${inc_alias}.txt    stderr=${inc_alias}_err.txt
        Wait For Process    ${inc_alias}    timeout=20 s
    END
    FOR    ${i}    IN RANGE    ${num_threads}
        ${dir_path}=    normalize path    ${CURDIR}/..
        ${inc_alias}=    Catenate    SEPARATOR=_    parallel    increment    ${i}
        Terminate Process   ${inc_alias}
        Sleep   5s
        Grep and Verify file Content in results folder  ${inc_alias}  Total
    END

Docker Create NFS Backup
    [Arguments]    ${no_of_backups}     ${container_name}
    [Documentation]    Accepts params: "{is_clear_folder}"
    ...    Keyword to create a NFS backup i.e to save backup to local folder
    ${root_path}=    normalize path    ${CURDIR}/..
    ${backup_path}=    Join Path    ${root_path}/backup
    ${alpha_ports}  Get Port From Container     ${container_name}
    FOR    ${i}    IN RANGE    ${no_of_backups}
        connect request server      is_docker=${GLOBAL_IS_DOCKER_EXE}   port=${alpha_ports}
        ${res}=    Backup Using Admin    ${backup_path}
        log    ${res}
        Verify file exists in a directory with parent folder name    ${backup_path}
        Health Check for Backup Operation   ${container_name}
    END
    @{dirs_backup}=    List Directories In Directory    ${backup_path}
    log     ${dirs_backup}

Health Check for Backup Operation
    [Arguments]     ${container_name}
    [Documentation]  Keyword to verify if backup operation is completed successfully
    ${alpha_ports}  Get Port From Container     ${container_name}
    Connect Request Server      is_docker=${GLOBAL_IS_DOCKER_EXE}   port=${alpha_ports}
    Wait Until Keyword Succeeds    600x    30 sec  Check if backup is completed

Check if backup is completed
    ${response}=    Health Check    /health
    log     ${response}
    ${on_going}     Get Value From Json     ${response}    [0].$..ongoing[0]
    ${check}    Run Keyword And Return Status   Should Be Empty     ${on_going}
    Return From Keyword If   ${check}    Pass
    Run Keyword if  '${on_going}[0]'=='opBackup'    Fail

Clear Backup Folders
    [Documentation]  Keyword to clear backup folders
    [Arguments]  ${is_clear_folder}
    ${root_path}=    normalize path    ${CURDIR}/..
    ${backup_path}=    Join Path    ${root_path}/backup
    Run Keyword If    ${is_clear_folder}    clear all the folder in a directory    ${backup_path}

Get Port From Container
    [Arguments]     ${container_name}
    [Documentation]  Keyword to get port number of the container
    ${ports}    Run Process   docker  port  ${container_name}
    Wait For Process    timeout=10 s    on_timeout=continue
    ${ports_list}=   Split String    ${ports.stdout}    \n
    ${matches}      Set Variable If   'alpha' in '${container_name}'    8*   5*
    ${port_matching}=    Get Matches     ${ports_list}   ${matches} 
    ${port}   Get Substring    ${port_matching}[0]    0   4 
    log     ${port}
    [Return]    ${port}

Docker Export NFS data using admin endpoint
    [Arguments]    ${data_type}     ${is_clear_folder}      ${container_name}
    [Documentation]    Accepts params: "{is_clear_folder}", "{data_type}"
    ...    Keyword to export dgraph data to either json/rdf format in local
    ${root_path}=    normalize path    ${CURDIR}/..
    ${export_path}=    Join Path    ${root_path}/export
    Run Keyword If    ${is_clear_folder}    clear all the folder in a directory    ${export_path}
    ${alpha_ports}  Get Port From Container     ${container_name}
    Connect Request Server      is_docker=${GLOBAL_IS_DOCKER_EXE}   port=${alpha_ports}
    ${res}=    Export Nfs Data Admin    data_format=${data_type}    destination=${export_path}
    log    ${res.text}
    Verify file exists in a directory with parent folder name    ${export_path}


Docker Perform a restore on backup latest versions
    [Arguments]  ${increment_size}      ${container_name}   ${zero_service}
    [Documentation]    Performs an restore operation on the default location i.e "backup" dir.
    ${zero_ports}  Get Port From Container     ${zero_service}
    ${alpha_ports}  Get Port From Container     ${container_name}
    Connect Request Server      is_docker=${GLOBAL_IS_DOCKER_EXE}   port=${alpha_ports}
    @{inc_list}     Create List     full
    FOR    ${i}    IN RANGE    ${increment_size}
        Append To List  ${inc_list}     incremental
    END
    ${root_dir}=    normalize path    ${CURDIR}/..
    ${backup_path}=    Join Path    ${root_dir}/backup
    ${json_file}    Load JSON From File    ${backup_path}/manifest.json
    ${type}     Get Value From Json     ${json_file}    $..type
    ${enc}     Get Value From Json     ${json_file}    $..encrypted
    Lists Should Be Equal   ${inc_list}     ${type}
    ${tls_check}=    Get Tls Value  is_docker=${GLOBAL_IS_DOCKER_EXE}
    ${enc_check}=    Get Enc Value  is_docker=${GLOBAL_IS_DOCKER_EXE}
    Run Keyword If     ${enc_check} is ${True}    List Should Contain Value   ${enc}     ${TRUE}
    ${dgraph_command}   Set Variable IF  '${DOCKER_STRING}'!='${EMPTY}'     ${DOCKER_STRING} dgraph     dgraph
    ${cmd}  Catenate   ${dgraph_command}   restore -p ${backup_path} -l ${backup_path} -z localhost:${zero_ports}
    ${result_restore}=    Run Keyword If    ${tls_check}   Restore Using Admin    ${backup_path}
    ...    ELSE    Run Keywords    Start Process   ${cmd}      alias=restore    stdout=restorebackup.txt    cwd=results     shell=True
    ...    AND    Process Should Be Running    restore
    ...    AND    Wait For Process    restore
    ...    AND    Process Should Be Stopped    restore
    ...    AND    Sleep    5s
    ...    AND    Verify Restore File Content In Results Folder    restorebackup    ${backup_path}      ${zero_ports}
    Health Check for Restore Operation  ${container_name} 

Docker Perform a restore on backup by older dgraph versions
    [Documentation]    Performs an restore operation on the default location i.e "backup" dir.
    [Arguments]     ${container_name}   ${zero_service}
    ${zero_ports}  Get Port From Container     ${zero_service}
    ${alpha_ports}  Get Port From Container     ${container_name}
    Connect Request Server      is_docker=${GLOBAL_IS_DOCKER_EXE}   port=${alpha_ports}
    ${root_dir}=    normalize path    ${CURDIR}/..
    ${path}=    Join Path    ${root_dir}/backup
    @{dirs_backup}=    List Directories In Directory    ${path}
    ${dgraph_command}   Set Variable IF  '${DOCKER_STRING}'!='${EMPTY}'     ${DOCKER_STRING} dgraph     dgraph
    ${cmd}  Catenate   ${dgraph_command}   restore -p ${backup_path} -l ${backup_path} -z localhost:${zero_ports}
    FOR     ${i}  IN    ${dirs_backup}
        ${restore_dir}=    Set Variable    ${i}[0]
        ${restore_dir}=    Join Path    ${root_dir}/backup/${restore_dir}
        ${tls_check}=    Get Tls Value  is_docker=${GLOBAL_IS_DOCKER_EXE}
        ${result_restore}=    Run Keyword If    ${tls_check}   Restore Using Admin    ${restore_dir}
        ...    ELSE    Run Keywords    Start Process    ${cmd}      alias=restore    stdout=restorebackup.txt    cwd=results    shell=True
        ...    AND    Process Should Be Running    restore
        ...    AND    Wait For Process    restore
        ...    AND    Process Should Be Stopped    restore
        ...    AND    Sleep    5s
        ...    AND    Verify Restore File Content In Results Folder    restorebackup    ${restore_dir}      ${zero_ports}
        Health Check for Restore Operation  ${container_name}
    END

Health Check for Restore Operation
    [Arguments]     ${container_name}
    [Documentation]  Keyword to verify if backup operation is completed successfully
    ${alpha_ports}  Get Port From Container     ${container_name}
    Wait Until Keyword Succeeds    20x    30 sec    Connect Request Server      is_docker=${GLOBAL_IS_DOCKER_EXE}   port=${alpha_ports}
    Wait Until Keyword Succeeds    600x    30 sec      Check if restore is completed

Check if restore is completed
    ${response}=    Health Check    /health
    ${passed}    Run Keyword And Return Status   Should Be String    ${response}
    Run Keyword If  ${passed}
    ...     Evaluate    '${response}'=='the server is in draining mode and client requests will only be allowed after exiting the mode  by sending a GraphQL draining(enable: false) mutation to /admin'    Fail

Verify restore file Content in results folder
    [Arguments]    ${file_name}    ${path}     ${zero_port}
    [Documentation]    Keyword for validating content in restore.txt files generated in results folder
    ...    [Arguments] -> "file_name" -file name ex: alpha for alpha.txt | "cotent" -content you want to check in file
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${file_context}=    Get File    ${dir_path}/results/${file_name}.txt
    @{compare_context}=    Create List    Restoring backups from: ${path}    Writing postings to: ${path}    Updating Zero timestamp at: localhost:${zero_port}
    FOR    ${context}    IN    @{compare_context}
        Should Contain    ${file_context}    ${context}
    END

Verify Bulk Loader output generated
    [Arguments]    ${path}
    [Documentation]    Keyword to verify bulk loader files output
    @{count}=    List Files In Directory    ${path}
    ${list_size}    Get Length    ${count}
    Run Keyword If    ${list_size}<0    FAIL    “Files were not generated.”

Verify process to be stopped
    [Arguments]    ${process_alias}
    [Documentation]    Keyword to check if the process is still running and wait till process completes.
    log    Process which is runing ${process_alias}
    ${process_check}=    Is Process Running    ${process_alias}
    Run Keyword If    '${process_check}'=='False'    Return From Keyword
    FOR    ${i}    IN RANGE    99999
        log    ${i}
        Wait For Process    ${process_alias}
        ${process_check}=    Is Process Running    ${process_alias}
        Exit For Loop If    '${process_check}'=='False'
    END
    Log    ${process_alias} Process is stopped
    Comment    Wait Until Keyword Succeeds    600x    5minute    Process Should Be Stopped    handle=${process_alias}    error_message=${error_message} is still running

Verify file exists in a directory with parent folder name
    [Arguments]    ${path}
    [Documentation]    Keyword to verify if a file exists in a directory
    ...    Accepts one argument "{path}" <- which indicates the path of the direcory
    ${rest}    ${folder_name}=    Split String From Right    ${path}    /    1
    @{dirs}=    List Directories In Directory    ${path}
    FOR    ${dir}    IN    @{dirs}
        directory should exist    ${folder_name.strip()}/${dir}
    END

Verify alpha and zero contents in results folder
    [Arguments]    ${file_name}    @{context}
    [Documentation]    Keyword for checking content in .txt files generated in results folder
    ...    [Arguments] -> "file_name" -file name ex: alpha for alpha.txt | "cotent" -content you want to check in file
    ${dir_path}=    normalize path    ${CURDIR}/..
    FOR     ${i}  IN RANGE   ${DOCKER_COMPOSE_UP_COUNT}
        ${file_context}=    Get File    ${dir_path}/results/${file_name}_${i}.txt
        Should Contain Any    ${file_context}    @{context}
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

clean up dgraph folders
    [Documentation]    Keyword to clear up the dgraph alpha and zero folder created.
    ${curr_dir}=    Normalize Path    ${CURDIR}/..
    @{dir}    Create List    alpha1 zero1    out    alpha
    FOR    ${foldername}    IN    @{dir}
        Remove Directory    ${curr_dir}/results/${foldername}    recursive=True
    END
    Log    "All the folders created by alpha and zero were deleted."

Clean up bulk folders
    [Documentation]    Keyword to clear up the dgraph alpha and zero folder created.
    ${curr_dir}=    Normalize Path    ${CURDIR}/..
    @{dir}    Create List    out    alpha  alpha1
    FOR    ${foldername}    IN    @{dir}
        Remove Directory    ${curr_dir}/results/${foldername}    recursive=True
    END
    Log    "All the folders created by alpha and zero were deleted."

clean up list of folders in results dir
    [Arguments]    @{dir}
    [Documentation]    Keyword to clear up the dgraph alpha and zero folder created.
    ${curr_dir}=    Normalize Path    ${CURDIR}/..
    FOR    ${foldername}    IN    @{dir}
        Run    rm -rf ${curr_dir}/results/${foldername}
    END
    Log    "All the folders were deleted."

clean up a perticular folders
    [Arguments]    ${folder_name}
    [Documentation]    Keyword to clear up a perticular folder created.
    ${curr_dir}=    Normalize Path    ${CURDIR}/..
    Run    rm -rf ${curr_dir}/results/${folder_name}
    Log    " ${folder_name} folder is deleted."

Clear all the folder in a directory
    [Arguments]    ${path}
    [Documentation]    Keyword to clear all the folder in a directory
    ...    Accepts one argument "{path}" <- which indicates the path of the direcory
    @{dirs}=    List Directories In Directory    ${path}
    ${list_size}    Get Length    ${dirs}
    Run Keyword If    ${list_size}>0    Empty Directory    ${path}

Create Backup Folder
    [Documentation]     Keyword to create backup dir for execution
    ${datetime} =	Get Current Date      result_format=%d-%m-%Y-%H-%M-%S
    Run Keyword If    '${GLOBAL_BACKUP_DIR_FOLDER}'=='${EMPTY}'    Set Suite Variable  ${GLOBAL_BACKUP_DIR_FOLDER}     exe_logs_${datetime}

Backup alpha and zero logs
    [Documentation]     Kewyword to backup all the logs
    Move Files      results/*.txt	   results/${GLOBAL_BACKUP_DIR_FOLDER}

Backup Yaml File
    [Documentation]     Kewyword to backup yaml file
    ${passed}   Run Keyword and Return Status   File Should Exist      results/docker-compose.yml
    IF  ${passed}
        Move File      results/docker-compose.yml	   results/${GLOBAL_BACKUP_DIR_FOLDER}/docker-compose_${GLOBAL_YAML_COUNTER}.yml
        ${GLOBAL_YAML_COUNTER}  Evaluate    ${GLOBAL_YAML_COUNTER} + 1
        Set Suite Variable      ${GLOBAL_YAML_COUNTER}      ${GLOBAL_YAML_COUNTER}
    END

Backup directories created while execution
    [Documentation]     Keyword to backup execution time directories
    @{dirs}     Create List     alpha1  zero1  out  alpha   tmp
    FOR  ${i}  IN    @{dirs}
        ${passed}   Run Keyword and Return Status   Directory Should Exist      results/${i}
        Run Keyword If  ${passed}   Move Directory   results/${i}   results/${GLOBAL_BACKUP_DIR_FOLDER}/${i}_${DOCKER_COMPOSE_UP_COUNT}
    END

Backup Custom Directories Created While Execution
    [Arguments]       @{dirs_to_backup}  
    [Documentation]     Keyword to backup execution time directories
    FOR  ${i}  IN    @{dirs_to_backup}
        ${passed}   Run Keyword and Return Status   Directory Should Exist      results/${i}
        Run Keyword If  ${passed}   Move Directory   results/${i}   results/${GLOBAL_BACKUP_DIR_FOLDER}/${i}_${DOCKER_COMPOSE_UP_COUNT}
    END