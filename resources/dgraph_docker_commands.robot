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
${ZERO_COUNT}   0
${ALPHA_COUNT}  0
${GLOBAL_IS_DOCKER_EXE}     ${FALSE}

*** Keywords ***

Start Dgraph n-node In Docker
    [Documentation]  Keyword to start dgraph in docker setup.
    [Arguments]     ${no_of_alphas}     ${no_of_zeros}    ${dgraph_version}     ${container_name}
    ${dir_path}=    normalize path    ${CURDIR}/..
    log    ${dir_path}
    ${service_json}   get zero and alpha docker cli command     container_name=${container_name}     dgraph_version=${dgraph_version}     zero_count=${no_of_zeros}   alpha_count=${no_of_alphas}
    @{zeros_list}   Get From Dictionary     ${service_json}     zeros
    @{alphas_list}   Get From Dictionary     ${service_json}     alphas
    FOR     ${zero_command}  IN      @{zeros_list}
        ${result_docker}=    Start Process    ${zero_command}       alias=zero_${ZERO_COUNT}   stdout=zero_${ZERO_COUNT}.txt    stderr=zero_err_${ZERO_COUNT}.txt    cwd=results    shell=True
        Wait For Process    timeout=20 s    on_timeout=continue
        ${ZERO_COUNT}   Evaluate        ${ZERO_COUNT} + 1
        Set Suite Variable      ${ZERO_COUNT}    ${ZERO_COUNT}
    END

    FOR    ${alpha_command}   IN    @{alphas_list}
        ${result_docker}=    Start Process     ${alpha_command}      alias=alpha_${ALPHA_COUNT}   stdout=alpha_${ALPHA_COUNT}.txt    stderr=alpha_err_${ALPHA_COUNT}.txt    cwd=results    shell=True
        Wait For Process    timeout=20 s    on_timeout=continue
        ${ALPHA_COUNT}  Evaluate        ${ALPHA_COUNT} + 1
        Set Suite Variable      ${ALPHA_COUNT}    ${ALPHA_COUNT}
    END
    Set Dgraph Version from docker      ${container_name}
    Set Suite Variable  ${GLOBAL_IS_DOCKER_EXE}     ${TRUE}

Start Dgraph 2-node In Docker with bulk data
    [Documentation]  Keyword to start dgraph with alpha pointing to bulk loader data in docker setup.
    [Arguments]    ${dgraph_version}     ${container_name}      ${bulk_data_path}
    ${dir_path}=    normalize path    ${CURDIR}/..
    log    ${dir_path}
    ${service_json}   get zero and alpha docker cli command     bulk_path=${bulk_data_path}      container_name=${container_name}     dgraph_version=${dgraph_version}     zero_count=1   alpha_count=1
    @{zeros_list}   Get From Dictionary     ${service_json}     zeros
    @{alphas_list}   Get From Dictionary     ${service_json}     alphas
    FOR     ${zero_command}  IN      @{zeros_list}
        ${result_docker}=    Start Process    ${zero_command}       alias=zero_${ZERO_COUNT}   stdout=zero_${ZERO_COUNT}.txt    stderr=zero_err_${ZERO_COUNT}.txt    cwd=results    shell=True
        Wait For Process    timeout=20 s    on_timeout=continue
        ${ZERO_COUNT}   Evaluate        ${ZERO_COUNT} + 1
        Set Suite Variable      ${ZERO_COUNT}    ${ZERO_COUNT}
    END

    FOR    ${alpha_command}   IN    @{alphas_list}
        ${result_docker}=    Start Process     ${alpha_command}      alias=alpha_${ALPHA_COUNT}   stdout=alpha_${ALPHA_COUNT}.txt    stderr=alpha_err_${ALPHA_COUNT}.txt    cwd=results    shell=True
        Wait For Process    timeout=20 s    on_timeout=continue
        ${ALPHA_COUNT}  Evaluate        ${ALPHA_COUNT} + 1
        Set Suite Variable      ${ALPHA_COUNT}    ${ALPHA_COUNT}
    END
    Set Dgraph Version from docker      ${container_name}
    Set Suite Variable  ${GLOBAL_IS_DOCKER_EXE}     ${TRUE}

End Docker Execution
    [Documentation]  Keyword to end docker execution
    [Arguments]     ${container_name}
    Terminate All Processes
    Process.start Process    docker    stop    ${container_name}       alias=dc_stop    cwd=results    shell=True    stdout=dc_stop.txt     stderr=dc_stop_err.txt
    Wait For Process    timeout=20 s    on_timeout=continue
    Process.start Process    docker    rm    ${container_name}       alias=dc_down    cwd=results    shell=True    stdout=docker_compose_down.txt     stderr=docker_compose_down_err.txt
    Wait For Process    timeout=40 s    on_timeout=continue
    Process Should Be Stopped   dc_down
    @{zero_context}    Create List    All done. Goodbye!    Got connection request
    @{alpha_context}    Create List    Buffer flushed successfully.     Raft node done.    Operation completed with id: opRestore
    @{alpha_error_context}  Create List     Error: unknown flag     panic: runtime error:   runtime.goexit
    @{alpha_init_err_context}  Create List     Dgraph Version  Dgraph codename
    ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify alpha and zero contents in results folder    alpha    @{alpha_init_err_context}
    Run Keyword And Return If      ${passed}==${FALSE}       Fail       alpha Initlization failed.
    ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify alpha and zero contents in results folder    alpha   @{alpha_error_context}
    Run Keyword And Return If      ${passed}       Fail     Captured few errors in aplpha

Terminate Docker Execution and Create Backup of Dgraph Execution
    [Arguments]     ${container_name}      ${is_clear_folder}
    Run Keyword And Continue On Failure    END DOCKER EXECUTION     ${container_name}
    ${backup_folder_name}      Backup alpha and zero logs
    Backup directories created while execution      ${backup_folder_name}
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up dgraph folders

End Zero Process
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    Switch Process    zero
    Terminate Process    handle=zero

Post Execution Verify Zero contents
    [Arguments]    ${is_clear_folder}
    [Documentation]  Keyword to verify alpha and zero logs
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    @{zero_context}    Create List    All done. Goodbye!
    @{dir}    Create List    w  zw
    Wait Until Keyword Succeeds     60x    10 sec     Verify alpha and zero contents in results folder    zero    @{zero_context}
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up list of folders in results dir    @{dir}

Post Execution Verify Alpha contents
    [Arguments]    ${is_clear_folder}
    [Documentation]  Keyword to verify alpha and zero logs
    ...    Accepts argument "is_clear_folder" as a check to clear the folder
    @{dir}    Create List    p   t
    @{alpha_err_context}  Create List     Dgraph Version  Dgraph codename
    ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify alpha and zero contents in results folder    alpha    @{alpha_err_context}
    Run Keyword And Return If      ${passed}==${FALSE}       Fail   alpha Initlization failed.
    @{alpha_error_context}  Create List     Error: unknown flag     panic: runtime error:   runtime.goexit
    ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify alpha and zero contents in results folder    alpha    @{alpha_error_context}
    Run Keyword And Return If      ${passed}       Fail     Captured few errors in alpha
    @{alpha_context}    Create List    Buffer flushed successfully.
    Wait Until Keyword Succeeds     60x    10 sec     Verify alpha and zero contents in results folder    alpha    @{alpha_context}
    Run Keyword If    '${is_clear_folder}' == 'true'    clean up list of folders in results dir    @{dir}

End Alpha Process
    [Documentation]    End all the dgraph alpha and zero process and clear the folder based on variable.
    Switch Process    alpha
    Terminate Process    handle=alpha


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
    [Arguments]     ${loader_alias}     ${rdf_filename}    ${schema_filename}     ${loader_name}
    [Documentation]     Keyword to only trigger live loader process
    ${dir_path}=    normalize path    ${CURDIR}/..
    log     ${DOCKER_STRING}
    ${path}=    Set Variable     ${dir_path}
    ${conf_loder_command}=    Get Dgraph Loader Command    ${path}/test_data/datasets/${rdf_filename}    ${path}/test_data/datasets/${schema_filename}       ${loader_name}     is_latest_version=${DGRAPH_LATEST_VERSION_CHECK}  docker_string=${DOCKER_STRING}      
    ${result_loader}=   Start Process    ${conf_loder_command}    alias=${loader_alias}    stdout=${loader_alias}.txt    stderr=${loader_alias}_err.txt    shell=True    cwd=results

Docker Execute Live Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" perform live loader.
    ...    rdf_filename, schema_filename
    ${dir_path}=    normalize path    ${CURDIR}/..
    Trigger Loader Process for Docker     live     ${rdf_filename}    ${schema_filename}    live
    Verify process to be stopped    live
    ${loader_Text_File_Content}=    Grep File    ${dir_path}/results/live.txt    N-Quads processed per second
    Log    ${loader_Text_File_Content}
    Should Contain    ${loader_Text_File_Content}    N-Quads processed per second

Docker Execute Bulk Loader for Docker with rdf and schema parameters
    [Arguments]    ${dgraph_version}     ${container_name}      ${rdf_filename}    ${schema_filename}
    [Documentation]    Keyword to accept two params "rdf_filename","schema_filename" perform bulk loader.
    ...    rdf_filename, schema_filename"bulk"
    ${dir_path}=    normalize path    ${CURDIR}/..
    Trigger Loader Process for Docker      bulk     ${rdf_filename}    ${schema_filename}    bulk
    Verify process to be stopped    bulk
    ${loader_Text_File_Content}=    Grep File    ${dir_path}/results/bulk.txt    Total:
    Log    ${loader_Text_File_Content}
    Docker Verify Bulk Process     ${dgraph_version}     ${container_name}       ${loader_Text_File_Content}

Verify Live loader trigger properly or not
    [Documentation]  Keyword to verify live loader to trigger properly
    [Arguments]  ${loader_alias}    ${rdf_filename}    ${schema_filename}     ${loader_name}
    ${status}   Run Keyword And Return Status   Wait Until Keyword Succeeds    3x    10 sec    Grep and Verify file Content in results folder    ${loader_alias}    N-Quads:
    ${tcp_error}=    Run Keyword And Return Status   Wait Until Keyword Succeeds    2x    60 sec    Grep and Verify file Content in results folder    ${loader_alias}    Error while dialing dial tcp
    IF  ${status}==${FALSE} or ${tcp_error}
        ${retry_check}=    Run Keyword And Return Status   Wait Until Keyword Succeeds    2x    60 sec    Grep and Verify file Content in results folder    ${loader_alias}    Please retry
        Terminate Process   ${loader_alias}
        Trigger Loader Process     ${loader_alias}     ${rdf_filename}    ${schema_filename}     ${loader_name}
        ${check}    Run Keyword And Return Status   Verify Live loader trigger properly or not  ${loader_alias}     ${rdf_filename}    ${schema_filename}     ${loader_name}
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
    End Docker Execution    ${container_name}
    Start Dgraph 2-node In Docker with bulk data    ${dgraph_version}     ${container_name}       ${dir_path}/results/out/0/p
    Clean up bulk folders


Docker Execute Parallel Loader with rdf and schema parameters
    [Arguments]    ${dgraph_version}   ${container_name}      ${rdf_filename}     ${schema_filename}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" perform parallel live/bulk loader.
    ...    rdf_filename, schema_filename
    ${dir_path}=    normalize path    ${CURDIR}/..
    @{loader_type}=    Create List    live    bulk
    FOR    ${i}    IN    @{loader_type}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    ${i}
        Trigger Loader Process for Docker     ${loader_alias}     ${rdf_filename}    ${schema_filename}    ${i}
        Log    ${loader_alias}.txt is log file name for this process.
    END
    FOR    ${i}    IN    @{loader_type}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    ${i}
        IF  '${i}'=='live'
            Verify Live loader trigger properly or not  ${loader_alias}     ${rdf_filename}    ${schema_filename}    live
        END
        Verify process to be stopped    ${loader_alias}
        ${grep_context}=    Set Variable If    "${i}"=="bulk"    Total:    N-Quads processed per second
        ${loader_Text_File_Content}    Grep File    ${dir_path}/results/${loader_alias}.txt    ${grep_context}
        Run Keyword If    '${i}' == 'live'    Should Contain    ${loader_Text_File_Content}    ${grep_context}
        ...    ELSE     Docker Verify Bulk Process     ${dgraph_version}     ${container_name}       ${loader_Text_File_Content}
    END

Docker Execute Multiple Parallel Live Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}    ${num_threads}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" and "num_threads" perform multiple parallel live loading.
    ...    rdf_filename, schema_filename , num_threads
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${value}=    Get Tls Value  is_docker=${GLOBAL_IS_DOCKER_EXE}
    FOR    ${i}    IN RANGE    ${num_threads}
        Log    Running thread -- ${i}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    live    ${i}
        Trigger Loader Process for Docker      ${loader_alias}     ${rdf_filename}    ${schema_filename}    live
        Check if parallel process is triggered      ${loader_alias}     ${rdf_filename}    ${schema_filename}       live
    END
    FOR    ${i}    IN RANGE    ${num_threads}
        Verify Live loader trigger properly or not  ${loader_alias}    ${rdf_filename}    ${schema_filename}    live
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    live    ${i}
        Verify process to be stopped    ${loader_alias}
        Grep and Verify file Content in results folder    ${loader_alias}    N-Quads processed per second
    END

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

Docker Execute Increment Command
    [Arguments]     ${num_threads}      ${alpha_offset}
    [Documentation]  Keyword to verify increment..
    FOR    ${i}    IN RANGE    ${num_threads}
        ${alpha_offset}    Set Variable If     ${i}>=1     ${alpha_offset}      0
        ${inc_alias}=    Catenate    SEPARATOR=_    parallel    increment    ${i}
        ${inc_command}  Get dgraph increment command    is_latest_version=${DGRAPH_LATEST_VERSION_CHECK}  docker_string=${DOCKER_STRING}      alpha_offset=${alpha_offset}
        ${result_i}=    Process.start Process   ${inc_command}    alias=${inc_alias}    cwd=results/inc_logs    shell=True    stdout=${inc_alias}.txt    stderr=${inc_alias}_err.txt
        Wait For Process    ${inc_alias}    timeout=20 s
    END
    FOR    ${i}    IN RANGE    ${num_threads}
        ${dir_path}=    normalize path    ${CURDIR}/..
        ${inc_alias}=    Catenate    SEPARATOR=_    parallel    increment    ${i}
        Terminate Process   ${inc_alias}
        Sleep   5s
        ${grep_file}=    Grep File    ${dir_path}/results/inc_logs/${inc_alias}.txt    Total
        Should Contain    ${grep_file}    Total
    END

Docker Create NFS Backup
    [Arguments]    ${no_of_backups}
    [Documentation]    Accepts params: "{is_clear_folder}"
    ...    Keyword to create a NFS backup i.e to save backup to local folder
    ${root_path}=    normalize path    ${CURDIR}/..
    ${backup_path}=    Join Path    ${root_path}/backup
    FOR    ${i}    IN RANGE    ${no_of_backups}
        connect request server      is_docker=${GLOBAL_IS_DOCKER_EXE}
        ${res}=    Backup Using Admin    ${backup_path}
        log    ${res}
        Verify file exists in a directory with parent folder name    ${backup_path}
        Health Check for Backup Operation
    END
    @{dirs_backup}=    List Directories In Directory    ${backup_path}
    log     ${dirs_backup}

Health Check for Backup Operation
    [Documentation]  Keyword to verify if backup operation is completed successfully
    Connect Request Server      is_docker=${GLOBAL_IS_DOCKER_EXE}
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
    Run Keyword If    '${is_clear_folder}' == 'true'    clear all the folder in a directory    ${backup_path}

Docker Export NFS data using admin endpoint
    [Arguments]    ${data_type}     ${is_clear_folder}
    [Documentation]    Accepts params: "{is_clear_folder}", "{data_type}"
    ...    Keyword to export dgraph data to either json/rdf format in local
    ${root_path}=    normalize path    ${CURDIR}/..
    ${export_path}=    Join Path    ${root_path}/export
    Run Keyword If    '${is_clear_folder}' == 'true'    clear all the folder in a directory    ${export_path}
    connect request server      is_docker=${GLOBAL_IS_DOCKER_EXE}
    ${res}=    Export Nfs Data Admin    data_format=${data_type}    destination=${export_path}
    log    ${res.text}
    Verify file exists in a directory with parent folder name    ${export_path}


Docker Perform a restore on backup latest versions
    [Arguments]  ${increment_size}
    [Documentation]    Performs an restore operation on the default location i.e "backup" dir.
    Connect request server  is_docker=${GLOBAL_IS_DOCKER_EXE}
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
    ${cmd}  Catenate   ${dgraph_command}   restore -p ${backup_path} -l ${backup_path} -z localhost:5080
    ${result_restore}=    Run Keyword If    "${tls_check}" == "True"    Restore Using Admin    ${backup_path}
    ...    ELSE    Run Keywords    Start Process   ${cmd}      alias=restore    stdout=restorebackup.txt    cwd=results     shell=True
    ...    AND    Process Should Be Running    restore
    ...    AND    Wait For Process    restore
    ...    AND    Process Should Be Stopped    restore
    ...    AND    Sleep    5s
    ...    AND    Verify Restore File Content In Results Folder    restorebackup    ${backup_path}
    Health Check for Restore Operation

Docker Perform a restore on backup by older dgraph versions
    [Documentation]    Performs an restore operation on the default location i.e "backup" dir.
    Connect request server  is_docker=${GLOBAL_IS_DOCKER_EXE}
    ${root_dir}=    normalize path    ${CURDIR}/..
    ${path}=    Join Path    ${root_dir}/backup
    @{dirs_backup}=    List Directories In Directory    ${path}
    ${dgraph_command}   Set Variable IF  '${DOCKER_STRING}'!='${EMPTY}'     ${DOCKER_STRING} dgraph     dgraph
    ${cmd}  Catenate   ${dgraph_command}   restore -p ${backup_path} -l ${backup_path} -z localhost:5080
    FOR     ${i}  IN    ${dirs_backup}
        ${restore_dir}=    Set Variable    ${i}[0]
        ${restore_dir}=    Join Path    ${root_dir}/backup/${restore_dir}
        ${tls_check}=    Get Tls Value  is_docker=${GLOBAL_IS_DOCKER_EXE}
        ${result_restore}=    Run Keyword If    "${tls_check}" == "True"    Restore Using Admin    ${restore_dir}
        ...    ELSE    Run Keywords    Start Process    ${cmd}      alias=restore    stdout=restorebackup.txt    cwd=results    shell=True
        ...    AND    Process Should Be Running    restore
        ...    AND    Wait For Process    restore
        ...    AND    Process Should Be Stopped    restore
        ...    AND    Sleep    5s
        ...    AND    Verify Restore File Content In Results Folder    restorebackup    ${restore_dir}
        Health Check for Restore Operation
    END


Perform a restore on backup present at other location
    [Arguments]   ${backup_path}     ${is_increment}
    [Documentation]    Performs an restore operation on the other location i.e "{path}" dir.
    ${json_file}    Load JSON From File    ${backup_path}/manifest.json
    Run Keyword If     '${is_increment}'=='true'    List Should Contain Value   ${type}     incremental
    ${result_restore}=    Run Keyword If    "https" in "${url}"    Restore Using Admin    ${backup_path}
    ...    ELSE    Run Keywords    Start Process    dgraph    restore    -p    ${backup_path}    -l    ${backup_path}    -z    localhost:5080    alias=restore    stdout=restorebackup.txt    cwd=results
    ...    AND    Process Should Be Running    zero
    ...    AND    Process Should Be Running    alpha
    ...    AND    Process Should Be Running    restore
    ...    AND    Wait For Process    restore
    ...    AND    Process Should Be Stopped    restore
    ...    AND    Sleep    5s
    ...    AND    Verify Restore File Content In Results Folder    restorebackup    ${backup_path}

Health Check for Restore Operation
    [Documentation]  Keyword to verify if backup operation is completed successfully
    Wait Until Keyword Succeeds    20x    30 sec       Connect Request Server   is_docker=${GLOBAL_IS_DOCKER_EXE}
    Wait Until Keyword Succeeds    600x    30 sec      Check if restore is completed

Check if restore is completed
    ${response}=    Health Check    /health
    ${passed}    Run Keyword And Return Status   Should Be String    ${response}
    Run Keyword If  ${passed}
    ...     Evaluate    '${response}'=='the server is in draining mode and client requests will only be allowed after exiting the mode  by sending a GraphQL draining(enable: false) mutation to /admin'    Fail

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
    ${count}=   Set Variable If     '${file_name}' == 'zero'   ${ZERO_COUNT}   ${ALPHA_COUNT}
    FOR     ${i}  IN RANGE   ${count}
        ${file_context}=    Get File    ${dir_path}/results/${file_name}_${i}.txt
        Should Contain Any    ${file_context}    @{context}
    END

Verify alpha and zero contents in sepcific folder
    [Arguments]    ${file_name}    ${folder_name}   @{context}
    [Documentation]    Keyword for checking content in .txt files generated in results folder
    ...    [Arguments] -> "file_name" -file name ex: alpha for alpha.txt | "cotent" -content you want to check in file
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${count}=   Set Variable If     '${file_name}' == 'zero'   ${ZERO_COUNT}   ${ALPHA_COUNT}
    FOR     ${i}  IN RANGE   ${count}
        ${file_context}=    Get File    ${dir_path}/results/${folder_name}/${file_name}_${i}.txt
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
    @{dir}    Create List    p    t    w    zw    out    alpha
    FOR    ${foldername}    IN    @{dir}
        Remove Directory    ${curr_dir}/results/${foldername}    recursive=True
    END
    Log    "All the folders created by alpha and zero were deleted."

Clean up bulk folders
    [Documentation]    Keyword to clear up the dgraph alpha and zero folder created.
    ${curr_dir}=    Normalize Path    ${CURDIR}/..
    @{dir}    Create List    out    alpha
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

Backup alpha and zero logs
    [Documentation]     Kewyword to backup all the logs
    ${datetime} =	Get Current Date      result_format=%d-%m-%Y-%H-%M-%S
    Move Files      results/*.txt	   results/exe_logs_${datetime}
    [Return]  exe_logs_${datetime}

Backup directories created while execution
    [Arguments]       ${direc_name}
    [Documentation]     Keyword to backup execution time directories
    @{dirs}     Create List     w   zw  p   t  out  alpha   tmp
    FOR  ${i}  IN    @{dirs}
        ${passed}   Run Keyword and Return Status   Directory Should Exist      results/${i}
        Run Keyword If  ${passed}   Move Directory   results/${i}   results/${direc_name}
    END