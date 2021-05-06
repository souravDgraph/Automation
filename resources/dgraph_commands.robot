*** Settings ***
Library           OperatingSystem
Library           Process
Library           Dgraph
Library           JSONLibrary
Library           String
Library           Collections
Library           DateTime

*** Variables ***
${ZERO_COUNT}   0
${ALPHA_COUNT}  0
${ALPHA_BULK_COUNT}  0
${ALPHA_LEARNER_BULK_COUNT}  0
${ALPHA_LEARNER_COUNT}  0
${ALPHA_LEARNER_LUDIC_COUNT}    0
${ALPHA_LUDICROUS_COUNT}    0
${ALPHA_LUDICROUS_BULK_COUNT}  0
${LUDICROUS_MODE}   ${FALSE}
${GLOBAL_BACKUP_LOGS_FOLDER}
${GLOBAL_IS_LEARNER}    ${FALSE}
${DIR_PATH}

*** Keywords ***
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


Start Dgraph
    [Documentation]    Start Dgraph alpha and Zero process with cwd pointing to results folder.
    # Dgraph alpha and zero command
    ${DIR_PATH}=    normalize path    ${CURDIR}/..
    Set Suite Variable      ${DIR_PATH}    ${DIR_PATH}
    clean up dgraph folders
    Create Backup Logs Folder
    ${zero_command}    Generate Dgraph Zero Cli Command     
    ${result_z}=    Process.start Process    ${zero_command}    alias=zero_${ZERO_COUNT}    cwd=results/    shell=True    stdout=zero_${ZERO_COUNT}.txt      stderr=zero_${ZERO_COUNT}_err.txt
    Process Should Be Running    zero_${ZERO_COUNT}
    Wait For Process    timeout=20 s    on_timeout=continue
    ${alpha_command}    Generate Dgraph Alpha Cli Command       cwd=${DIR_PATH}/results/alpha_${ALPHA_COUNT}
    ${result_a}=    Process.start Process    ${alpha_command}    alias=alpha_${ALPHA_COUNT}    stdout=alpha_${ALPHA_COUNT}.txt    cwd=results/    shell=True       stderr=alpha_${ALPHA_COUNT}_err.txt
    Process Should Be Running    alpha_${ALPHA_COUNT}
    Wait For Process    timeout=20 s    on_timeout=continue
    ${ZERO_COUNT}   Evaluate        ${ZERO_COUNT} + 1
    ${ALPHA_COUNT}  Evaluate        ${ALPHA_COUNT} + 1
    Set Suite Variable      ${ZERO_COUNT}    ${ZERO_COUNT}
    Set Suite Variable      ${ALPHA_COUNT}    ${ALPHA_COUNT}
    Set Suite Variable      ${LUDICROUS_MODE}    ${FALSE}
    Set Suite Variable      ${GLOBAL_IS_LEARNER}    ${FALSE}
    @{alpha_context}  Create List     Dgraph Version  Dgraph codename   No GraphQL schema in Dgraph;
    ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify Perticular file contents in results folder    alpha     ${ALPHA_COUNT}     @{alpha_context}
    Run Keyword And Return If      ${passed}==${FALSE}       Fatal Error    msg=Error while bringing up Alpha

Start Dgraph with learner node
    [Documentation]    Start Dgraph alpha and Zero process with cwd pointing to results folder.
    # Dgraph alpha and zero command
    ${DIR_PATH}=    normalize path    ${CURDIR}/..
    Set Suite Variable      ${DIR_PATH}    ${DIR_PATH}
    clean up dgraph folders
    Create Backup Logs Folder
    ${zero_command}    Generate Dgraph Zero Cli Command
    ${result_z}=    Process.start Process    ${zero_command}    alias=zero    cwd=results/    shell=True    stdout=zero_${ZERO_COUNT}.txt      stderr=zero_${ZERO_COUNT}_err.txt
    Process Should Be Running    zero
    Wait For Process    timeout=15 s    on_timeout=continue
    ${alpha_command}    Generate Dgraph Alpha Cli Command    cwd=${DIR_PATH}/results/alpha_${ALPHA_COUNT}
    ${result_a}=    Process.start Process    ${alpha_command}    alias=alpha    stdout=alpha_${ALPHA_COUNT}.txt    cwd=results/    shell=True       stderr=alpha_${ALPHA_COUNT}_err.txt
    Process Should Be Running    alpha
    Wait For Process    timeout=15 s    on_timeout=continue
    ${alpha_command_learner}    Generate Dgraph Alpha Cli Command    learner=${TRUE}    cwd=${DIR_PATH}/results/alpha_learner_${ALPHA_LEARNER_COUNT}
    ${result_a}=    Process.start Process    ${alpha_command_learner}    alias=alpha_learner    stdout=alpha_learner_${ALPHA_LEARNER_COUNT}.txt    cwd=results/    shell=True       stderr=alpha_learner_${ALPHA_LEARNER_COUNT}_err.txt
    Process Should Be Running    alpha_learner
    Wait For Process    timeout=10 s    on_timeout=continue
    ${ZERO_COUNT}   Evaluate        ${ZERO_COUNT} + 1
    ${ALPHA_COUNT}  Evaluate        ${ALPHA_COUNT} + 1
    ${ALPHA_LEARNER_COUNT}  Evaluate        ${ALPHA_LEARNER_COUNT} + 1
    Set Suite Variable      ${ALPHA_LEARNER_COUNT}    ${ALPHA_LEARNER_COUNT}
    Set Suite Variable      ${ZERO_COUNT}    ${ZERO_COUNT}
    Set Suite Variable      ${ALPHA_COUNT}    ${ALPHA_COUNT}
    Set Suite Variable      ${LUDICROUS_MODE}    ${FALSE}
    Set Suite Variable      ${GLOBAL_IS_LEARNER}    ${TRUE}
    @{alpha_context}  Create List     Dgraph Version  Dgraph codename   No GraphQL schema in Dgraph;
    @{alpha_learner_context}  Create List     No GraphQL schema in Dgraph;    is_learner:true
    ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify Perticular file contents in results folder    alpha    ${ALPHA_COUNT}     @{alpha_context}
    ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify Perticular file contents in results folder    alpha_learner    ${ALPHA_LEARNER_COUNT}      @{alpha_learner_context}
    Run Keyword And Return If      ${passed}==${FALSE}       Fatal Error    msg=Error while bringing up Alpha

Start Dgraph Ludicrous Mode
    [Documentation]    Start Dgraph alpha and Zero process with cwd pointing to results folder.
    # Dgraph alpha and zero command
    ${DIR_PATH}=    normalize path    ${CURDIR}/..
    Set Suite Variable      ${DIR_PATH}    ${DIR_PATH}
    Set Suite Variable      ${LUDICROUS_MODE}    True
    ${alpha_alias}     Set Variable	    alpha_ludicrous_${ALPHA_LUDICROUS_COUNT}
    Create Backup Logs Folder
    ${zero_command}    Generate Dgraph Zero Cli Command     
    ${result_z}=    Process.start Process    ${zero_command}    alias=zero_${ZERO_COUNT}    cwd=results/    shell=True    stdout=zero_${ZERO_COUNT}.txt      stderr=zero_${ZERO_COUNT}_err.txt
    Process Should Be Running    zero_${ZERO_COUNT}
    Wait For Process    timeout=10 s    on_timeout=continue
    ${alpha_command}    Generate Dgraph Alpha Cli Command          ludicrous_mode=enabled   cwd=${DIR_PATH}/results/${alpha_alias}
    ${result_a}=    Process.start Process    ${alpha_command}    alias=${alpha_alias}    stdout=${alpha_alias}.txt    cwd=results/    shell=True       stderr=${alpha_alias}_err.txt
    Process Should Be Running    ${alpha_alias}
    Wait For Process    timeout=10 s    on_timeout=continue
    ${ZERO_COUNT}   Evaluate        ${ZERO_COUNT} + 1
    ${ALPHA_LUDICROUS_COUNT}    Evaluate        ${ALPHA_LUDICROUS_COUNT} + 1
    Set Suite Variable      ${ZERO_COUNT}    ${ZERO_COUNT}
    Set Suite Variable      ${ALPHA_LUDICROUS_COUNT}    ${ALPHA_LUDICROUS_COUNT}
    @{alpha_context}  Create List     Dgraph Version  Dgraph codename   No GraphQL schema in Dgraph;
    ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify Perticular file contents in results folder    alpha_ludicrous     ${ALPHA_LUDICROUS_COUNT}     @{alpha_context}
    Run Keyword And Return If      ${passed}==${FALSE}       Fatal Error    msg=Error while bringing up Alpha

Start Dgraph Zero
    [Documentation]    Start Dgraph Zero process
    ${zero_command}    Generate Dgraph Zero Cli Command
    ${result_z}=    Process.start Process    ${zero_command}    alias=zero    cwd=results/   shell=True    stdout=zero_${ZERO_COUNT}.txt    stderr=zero_${ZERO_COUNT}_err.txt
    Process Should Be Running    zero
    Wait For Process    timeout=20 s    on_timeout=continue
    ${ZERO_COUNT}   Evaluate        ${ZERO_COUNT} + 1
    Set Suite Variable      ${ZERO_COUNT}    ${ZERO_COUNT}

Start Dgraph Alpha
    [Arguments]     ${path}=${None}     ${is_ludicrous_mode}=${None}    ${is_learner}=${None}       ${alpha_offset}=${None}
    [Documentation]    Start Dgraph alpha process.
    ${alpha_command}     Set Variable	    alpha
    ${alpha_alias}      Set Variable If     '${path}'!='${None}'    alpha_bulk_${ALPHA_BULK_COUNT}    alpha_${ALPHA_COUNT}
    ${alpha_bulk_path}      Set Variable If   '${is_learner}'=='${None}'   ${path}     ${None}
    IF   ${is_ludicrous_mode}
        ${alpha_alias}      Set Variable If     '${path}'!='${None}'    alpha_ludicrous_bulk_${ALPHA_LUDICROUS_BULK_COUNT}    alpha_ludicrous_${ALPHA_LUDICROUS_COUNT}
        ${log_count}    Set Variable If     '${path}'!='${None}'    ${ALPHA_LUDICROUS_BULK_COUNT}   ${ALPHA_LUDICROUS_COUNT}
        ${alpha_command}    Generate Dgraph Alpha Cli Command     bulk_path=${alpha_bulk_path}    ludicrous_mode=enabled    offset=${alpha_offset}   cwd=${DIR_PATH}/results/${alpha_alias}
    ELSE IF  ${is_learner}
        ${alpha_alias}      Set Variable If     '${path}' != '${None}'    alpha_bulk_learner_${ALPHA_LEARNER_BULK_COUNT}    alpha_learner_${ALPHA_LEARNER_COUNT}
        ${log_count}    Set Variable If     '${path}' != '${None}'    ${ALPHA_LEARNER_BULK_COUNT}    ${ALPHA_LEARNER_COUNT}
        IF  ${is_ludicrous_mode}
            ${alpha_alias}     Set Variable	    alpha_learner_ludic_${ALPHA_LEARNER_LUDIC_COUNT}
            ${log_count}    Set Variable   ${ALPHA_LEARNER_LUDIC_COUNT}
            ${alpha_command}     Generate Dgraph Alpha Cli Command    bulk_path=${path}  ludicrous_mode=enabled  learner=${TRUE}    offset=${alpha_offset}    cwd=${DIR_PATH}/results/${alpha_alias}
        ELSE
            ${alpha_command}    Generate Dgraph Alpha Cli Command    bulk_path=${path}      learner=${TRUE}     offset=${alpha_offset}      cwd=${DIR_PATH}/results/${alpha_alias}
        END
    ELSE
        ${alpha_command}    Generate Dgraph Alpha Cli Command      bulk_path=${alpha_bulk_path}     offset=${alpha_offset}      cwd=${DIR_PATH}/results/${alpha_alias}
        ${log_count}    Set Variable  ${ALPHA_COUNT}
    END
    ${result_a}=    Process.start Process    ${alpha_command}    alias=${alpha_alias}    stdout=${alpha_alias}.txt    cwd=results/    shell=True       stderr=${alpha_alias}_err.txt
    Process Should Be Running    ${alpha_alias} 
    Wait For Process    timeout=20 s    on_timeout=continue
    IF  '${path}' != '${None}' and '${is_learner}' == '${None}' and '${is_ludicrous_mode}' == '${None}'
        ${ALPHA_BULK_COUNT}  Evaluate        ${ALPHA_BULK_COUNT} + 1
        Set Suite Variable      ${ALPHA_BULK_COUNT}    ${ALPHA_BULK_COUNT}
    ELSE IF   ${is_ludicrous_mode}
        IF  '${path}' != '${None}'
            ${ALPHA_LUDICROUS_BULK_COUNT}  Evaluate        ${ALPHA_LUDICROUS_BULK_COUNT} + 1
            Set Suite Variable      ${ALPHA_LUDICROUS_BULK_COUNT}    ${ALPHA_LUDICROUS_BULK_COUNT}
        ELSE
            ${ALPHA_LUDICROUS_COUNT}  Evaluate        ${ALPHA_LUDICROUS_COUNT} + 1
            Set Suite Variable      ${ALPHA_LUDICROUS_COUNT}    ${ALPHA_LUDICROUS_COUNT}
        END
    ELSE IF  ${is_learner}
        IF  '${path}'!='${None}'
            ${ALPHA_LEARNER_BULK_COUNT}  Evaluate        ${ALPHA_LEARNER_BULK_COUNT} + 1
            Set Suite Variable      ${ALPHA_LEARNER_BULK_COUNT}    ${ALPHA_LEARNER_BULK_COUNT}
        ELSE IF     ${is_ludicrous_mode}
            ${ALPHA_LEARNER_LUDIC_COUNT}  Evaluate        ${ALPHA_LEARNER_LUDIC_COUNT} + 1
            Set Suite Variable      ${ALPHA_LEARNER_LUDIC_COUNT}    ${ALPHA_LEARNER_LUDIC_COUNT}
        ELSE
            ${ALPHA_LEARNER_COUNT}  Evaluate        ${ALPHA_LEARNER_COUNT} + 1
            Set Suite Variable      ${ALPHA_LEARNER_COUNT}    ${ALPHA_LEARNER_COUNT}
        END
    ELSE
        ${ALPHA_COUNT}  Evaluate        ${ALPHA_COUNT} + 1
        Set Suite Variable      ${ALPHA_COUNT}    ${ALPHA_COUNT}
    END
    @{alpha_context}  Create List     Dgraph Version  Dgraph codename   No GraphQL schema in Dgraph;
    ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify Perticular file contents in results folder    ${alpha_alias}   0   @{alpha_context}
    Run Keyword And Return If      ${passed}==${FALSE}       Fatal Error    msg=Error while bringing up Alpha

End All Process
    [Documentation]    End all the dgraph alpha and zero process.
    Terminate All Processes
    
Verify Alpha and Zero logs generated
    [Documentation]     Verifies all zero's and alpha's logs generated during execution.
    Post Execution Verify Zero contents
    Post Execution Verify Alpha contents

Terminate and Create Backup of Dgraph Execution
    [Documentation]     Terminates and backsup up all the executions.
    [Arguments]  ${is_clear_folder}
    Run Keyword If Any Tests Failed     Run Keywords    Terminate All Processes
    ...     AND     Sleep   20s
    ...     AND     Backup alpha and zero logs
    ...     AND     Backup directories created while execution
    ...     AND     Run Keyword If    ${is_clear_folder}    clean up dgraph folders
    ...     AND     Return From Keyword
    End All Process
    Run Keyword And Continue On Failure    Verify Alpha and Zero logs generated
    Run Keyword If    ${is_clear_folder}    clean up dgraph folders
    Backup alpha and zero logs
    Backup directories created while execution

End Zero Process
    [Documentation]    End dgraph zero process
    Switch Process    zero
    Terminate Process    handle=zero

Post Execution Verify Zero contents
    [Documentation]  Keyword to verify alpha and zero logs
    @{zero_context}    Create List    All done. Goodbye!    Got connection request
    Wait Until Keyword Succeeds     60x    10 sec     Verify alpha and zero contents in results folder    zero     ${ZERO_COUNT}    @{zero_context}

Post Execution Verify Alpha contents
    [Documentation]  Keyword to verify alpha and zero logs
    @{alpha_alias}      Create List     alpha   alpha_bulk   alpha_bulk_learner  alpha_learner      alpha_ludicrous     alpha_learner_ludic
    @{alpha_counts}     Create List     ${ALPHA_COUNT}  ${ALPHA_BULK_COUNT}     ${ALPHA_LEARNER_BULK_COUNT}     ${ALPHA_LEARNER_COUNT}      ${ALPHA_LUDICROUS_COUNT}    ${ALPHA_LEARNER_LUDIC_COUNT}
    ${index}=    Set Variable    0
    FOR  ${alias}  IN     @{alpha_alias}
    ${log_count}    Set Variable  ${alpha_counts}[${index}]
        IF  ${log_count}>0
            @{alpha_context}    Create List    Buffer flushed successfully.     Raft node done.    Operation completed with id: opRestore
            @{alpha_error_context}  Create List     Error: unknown flag     panic: runtime error:   runtime.goexit      runtime.throw
            @{alpha_init_err_context}  Create List     Dgraph Version  Dgraph codename
            ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify alpha and zero contents in results folder    ${alias}    ${log_count}     @{alpha_init_err_context}
            Run Keyword And Return If      ${passed}==${FALSE}       Fail       alpha Initialization failed.
            ${passed}=  Run Keyword And Return Status   Wait Until Keyword Succeeds     5x    5 sec   Verify alpha and zero contents in results folder    ${alias}    ${log_count}     @{alpha_error_context}
            Run Keyword And Return If      ${passed}       Fail     Captured few errors in alpha
            Wait Until Keyword Succeeds     60x    10 sec     Verify alpha and zero contents in results folder    ${alias}      ${log_count}      @{alpha_context}
        END
        ${index}=    Evaluate    ${index} + 1
    END

End All Alpha Process
    [Documentation]    Ends All the  dgraph alpha process
    @{alpha_alias}      Create List     alpha   alpha_bulk   alpha_bulk_learner  alpha_learner      alpha_ludicrous     alpha_learner_ludic
    @{alpha_counts}     Create List     ${ALPHA_COUNT}  ${ALPHA_BULK_COUNT}     ${ALPHA_LEARNER_BULK_COUNT}     ${ALPHA_LEARNER_COUNT}      ${ALPHA_LUDICROUS_COUNT}    ${ALPHA_LEARNER_LUDIC_COUNT}
    ${index}=    Set Variable    0
    FOR  ${alias}    IN    ${alpha_alias}
        ${count}    Set Variable  ${alpha_counts}[${index}]
        FOR  ${log_count}    IN RANGE   ${count}
            ${passed}   Run Keyword And Return Status   Switch Process    ${alias}_${index}
            Run Keyword If  ${passed}  Terminate Process    handle=${alias}_${index}
        END
    END

End Alpha Process
    [Documentation]    End dgraph alpha process
    ${alpha_count}  Evaluate    ${ALPHA_COUNT} - 1
    Switch Process    alpha_${alpha_count}
    Terminate Process    handle=alpha_${alpha_count}

End Alpha Ludicrous Process
    [Documentation]    End dgraph alpha process
    ${alpha_count}  Evaluate    ${ALPHA_LUDICROUS_COUNT} - 1
    Switch Process    alpha_ludicrous_${alpha_count}
    Terminate Process    handle=alpha_ludicrous_${alpha_count}

End Alpha Learner Process
    [Documentation]    End dgraph alpha with learner node process
    ${alpha_count}  Evaluate    ${ALPHA_LEARNER_COUNT} - 1
    Switch Process    alpha_learner_${alpha_count}
    Terminate Process    handle=alpha_learner_${alpha_count}

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

Trigger Loader Process
    [Arguments]     ${loader_alias}     ${rdf_filename}    ${schema_filename}     ${loader_name}    ${is_learner}=None      ${bulk_out_dir}=${None}
    [Documentation]     Keyword to only trigger live loader process
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${path}=    Set Variable     ${dir_path}
    ${conf_loder_command}=    Get Dgraph Loader Command    ${path}/test_data/datasets/${rdf_filename}    ${path}/test_data/datasets/${schema_filename}       ${loader_name}     is_learner=${is_learner}    out_dir=${bulk_out_dir}
    ${result_loader}=   Process.start Process    ${conf_loder_command}    alias=${loader_alias}    stdout=${loader_alias}.txt    stderr=${loader_alias}_err.txt    shell=True    cwd=results

Execute Live Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}    ${is_learner}=None
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" perform live loader.
    ...    rdf_filename, schema_filename
    ${dir_path}=    normalize path    ${CURDIR}/..
    Trigger Loader Process      live     ${rdf_filename}    ${schema_filename}    live    is_learner=${is_learner}
    Verify process to be stopped    live
    ${loader_Text_File_Content}=    Grep File    ${dir_path}/results/live.txt    N-Quads processed per second
    Log    ${loader_Text_File_Content}
    Should Contain    ${loader_Text_File_Content}    N-Quads processed per second

Execute Bulk Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}    ${is_learner}=${None}   ${alpha_offset_bulk}=${0}
    [Documentation]    Keyword to accept four params "rdf_filename","schema_filename", "is_learner", "alpha_offset" perform bulk loader.
    ...    rdf_filename, schema_filename"bulk"
    ${dir_path}=    normalize path    ${CURDIR}/..
    Trigger Loader Process      bulk     ${rdf_filename}    ${schema_filename}    bulk      bulk_out_dir=${dir_path}/results/bulk/out
    Verify process to be stopped    bulk
    ${loader_Text_File_Content}=    Grep File    ${dir_path}/results/bulk.txt    Total:
    Log    ${loader_Text_File_Content}
    Verify Bulk Process     ${dir_path}/results/bulk/out    ${loader_Text_File_Content}     is_learner=${is_learner}       alpha_offset_bulk=${alpha_offset_bulk}

Verify Bulk Process
    [Arguments]    ${bulk_out_path}     ${loader_Text_File_Content}     ${is_retrigger}=${FALSE}    ${is_learner}=${FALSE}   ${alpha_offset_bulk}=${0}
    [Documentation]     Keyword to verify bulk loader output files generated along with
     ...    altering zero and alpha instances.
    ${dir_path}=    normalize path    ${CURDIR}/..
    Should Contain    ${loader_Text_File_Content}    Total:
    Verify Bulk Loader output generated    ${bulk_out_path}/0/p
    IF  ${is_retrigger}
        IF  ${LUDICROUS_MODE}
            End Alpha Ludicrous Process
            ${count}    Set Variable  ${ALPHA_LUDICROUS_COUNT} - 1
            @{dirs}     Create List       alpha_ludicrous_${count}
        ELSE IF     ${is_learner}
            End Alpha Learner Process
            ${count}    Set Variable  ${ALPHA_LEARNER_COUNT} - 1
            @{dirs}     Create List       alpha_learner_${count}
        ELSE
            End Alpha Process
            ${count}    Set Variable  ${ALPHA_COUNT} - 1
            @{dirs}     Create List       alpha_${count}
        END
        Post Execution Verify Alpha contents
        Backup Custom Directories Created While Execution
        Start Dgraph Alpha    ${bulk_out_path}/0/p       ${LUDICROUS_MODE}   is_learner=${is_learner}
    END
    Start Dgraph Alpha    ${bulk_out_path}/0/p       ${LUDICROUS_MODE}   is_learner=${is_learner}     alpha_offset=${alpha_offset_bulk}

Verify Live loader trigger properly or not
    [Documentation]  Keyword to verify live loader to trigger properly
    [Arguments]  ${loader_alias}    ${rdf_filename}    ${schema_filename}     ${loader_name}    ${is_leaner}=${None}
    ${status}   Run Keyword And Return Status   Wait Until Keyword Succeeds    3x    10 sec    Grep and Verify file Content in results folder    ${loader_alias}    N-Quads:
    ${loader_err}   Run Keyword And Return Status   Wait Until Keyword Succeeds    3x    10 sec    Grep and Verify file Content in results folder    ${loader_alias}_err   Please retry operation
    ${tcp_error}=    Run Keyword And Return Status   Wait Until Keyword Succeeds    2x    60 sec    Grep and Verify file Content in results folder    ${loader_alias}    Error while dialing dial tcp
    IF  ${status}==${FALSE} or ${tcp_error} or ${loader_err}
        ${retry_check}=    Run Keyword And Return Status   Wait Until Keyword Succeeds    2x    60 sec    Grep and Verify file Content in results folder    ${loader_alias}    Please retry
        Terminate Process   ${loader_alias}
        Trigger Loader Process     ${loader_alias}     ${rdf_filename}    ${schema_filename}     ${loader_name}     ${is_leaner}
        @{live_loader_errors}  Create List     github.com/dgraph-io/dgraph/
        ${check}    Run Keyword And Return Status   Grep and Verify file Content in results folder   ${loader_alias}_err     @{live_loader_errors}
        Run Keyword If   ${check}   FAIL    Found Issues in Live Loader during live load
        @{alpha_error_context}  Create List     Error: unknown flag     panic: runtime error:   runtime.goexit      runtime.throw      fatal error:
        IF  ${is_leaner}
            ${check}    Run Keyword And Return Status   Verify Perticular file contents in results folder   alpha_learner    ${ALPHA_LEARNER_COUNT}     @{alpha_error_context}
            Run Keyword If   ${check}   FAIL    Found Issues in alpha during live load
        ELSE
            ${check}    Run Keyword And Return Status   Verify Perticular file contents in results folder   alpha    ${ALPHA_COUNT}      @{alpha_error_context}
            Run Keyword If   ${check}   FAIL    Found Issues in alpha during live load
        END
        ${check}    Run Keyword And Return Status   Verify Live loader trigger properly or not  ${loader_alias}     ${rdf_filename}    ${schema_filename}     ${loader_name}    ${is_leaner}
        Return From Keyword If   ${check}
        ...     ELSE    FAIL    Some issue with live loader
    END

Execute Parallel Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}    ${is_learner}=${None}       ${alpha_offset_bulk}=${30}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" perform parallel live/bulk loader.
    ...    rdf_filename, schema_filename
    ${dir_path}=    normalize path    ${CURDIR}/..
    @{loader_type}=    Create List    live    bulk
    FOR    ${i}    IN    @{loader_type}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    ${i}
        Trigger Loader Process     ${loader_alias}     ${rdf_filename}    ${schema_filename}    ${i}    is_learner=${is_learner}        bulk_out_dir=${dir_path}/results/parallel_bulk/out
        #Wait For Process    timeout=30 s
        Log    ${loader_alias}.txt is log file name for this process.
    END
    FOR    ${i}    IN    @{loader_type}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    ${i}
        IF  '${i}'=='live'
            Verify Live loader trigger properly or not  ${loader_alias}     ${rdf_filename}    ${schema_filename}    live   is_learner=${is_learner}
        END
        Verify process to be stopped    ${loader_alias}
        ${grep_context}=    Set Variable If    "${i}"=="bulk"    Total:    N-Quads processed per second
        ${loader_Text_File_Content}    Grep File    ${dir_path}/results/${loader_alias}.txt    ${grep_context}
        Run Keyword If    '${i}' == 'live'    Should Contain    ${loader_Text_File_Content}    ${grep_context}
        ...    ELSE     Verify Bulk Process     ${dir_path}/results/parallel_bulk/out    ${loader_Text_File_Content}     is_learner=${is_learner}       alpha_offset_bulk=${alpha_offset_bulk}
    END

Execute Multiple Parallel Live Loader with rdf and schema parameters
    [Arguments]    ${rdf_filename}    ${schema_filename}    ${num_threads}   ${is_learner}=${None}
    [Documentation]    Keyword to accept three params "rdf_filename","schema_filename" and "num_threads" perform multiple parallel live loading.
    ...    rdf_filename, schema_filename , num_threads
    ${dir_path}=    normalize path    ${CURDIR}/..
    FOR    ${i}    IN RANGE    ${num_threads}
        Log    Running thread -- ${i}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    live    ${i}
        Trigger Loader Process      ${loader_alias}     ${rdf_filename}    ${schema_filename}    live    ${is_learner}
        Check if parallel process is triggered      ${loader_alias}     ${rdf_filename}    ${schema_filename}       live     ${is_learner}
    END
    FOR    ${i}    IN RANGE    ${num_threads}
        ${loader_alias}=    Catenate    SEPARATOR=_    parallel    live    ${i}
        Verify Live loader trigger properly or not  ${loader_alias}    ${rdf_filename}    ${schema_filename}    live     ${is_learner}
        Verify process to be stopped    ${loader_alias}
        Grep and Verify file Content in results folder    ${loader_alias}    N-Quads processed per second
    END

Check if parallel process is triggered
    [Arguments]    ${loader_alias}     ${rdf_filename}    ${schema_filename}  ${loader_name}     ${is_learner}
    [Documentation]     Keyword to retry live loading for couple of times.
    ${result_check}=    Run Keyword And Return Status   Grep and Verify file Content in results folder      ${loader_alias}    Please retry operation
    ${result_check_err}=    Run Keyword And Return Status   Grep and Verify file Content in results folder      ${loader_alias}_err    Please retry operation
    ${process_check}=    Is Process Running    ${loader_alias}
    Sleep   30s
    log  ${loader_alias}
    Run Keyword If    ${process_check} and ${result_check} and ${result_check_err}   Terminate Process     ${loader_alias}
    Run Keyword If  ${result_check} and ${result_check_err}  Run Keywords     Sleep   30s
    ...     AND     Trigger Loader Process     ${loader_alias}     ${rdf_filename}    ${schema_filename}   ${loader_name}    ${is_learner}
    ...     AND     Check if parallel process is triggered      ${loader_alias}     ${rdf_filename}    ${schema_filename}   ${loader_name}       ${is_learner}


Execute Increment Command
    [Arguments]     ${num_threads}      ${alpha_offset}
    [Documentation]  Keyword to verify increment..
    FOR    ${i}    IN RANGE    ${num_threads}
        ${alpha_offset}    Set Variable If     ${i}>=1     ${alpha_offset}      0
        ${inc_alias}=    Catenate    SEPARATOR=_    parallel    increment    ${i}
        ${inc_command}  Get dgraph increment command       alpha_offset=${alpha_offset}
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

Create NFS Backup
    [Arguments]    ${no_of_backups}
    [Documentation]    Accepts params: "{is_clear_folder}"
    ...    Keyword to create a NFS backup i.e to save backup to local folder
    ${root_path}=    normalize path    ${CURDIR}/..
    ${backup_path}=    Join Path    ${root_path}/backup
    FOR    ${i}    IN RANGE    ${no_of_backups}
        connect request server      is_learner=${GLOBAL_IS_LEARNER}
        ${res}=    Backup Using Admin    ${backup_path}
        log    ${res}
        Verify files exists in directory    ${backup_path}
        Health Check for Backup Operation
    END
    @{dirs_backup}=    List Directories In Directory    ${backup_path}
    log     ${dirs_backup}

Health Check for Backup Operation
    [Documentation]  Keyword to verify if backup operation is completed successfully
    Connect Request Server      is_learner=${GLOBAL_IS_LEARNER}
    Wait Until Keyword Succeeds    600x    30 sec  Check if backup is completed

Check if backup is completed
    ${response}=    Health Check    /health
    log     ${response}
    ${on_going}     Get Value From Json     ${response}    [0].$..ongoing[0]
    ${check}    Run Keyword And Return Status   Should Be Empty     ${on_going}
    Return From Keyword If   ${check}    Pass
    Run Keyword if  '${on_going}[0]'=='opBackup'    Fail

Export NFS data using admin endpoint
    [Arguments]    ${data_type}     ${is_clear_folder}
    [Documentation]    Accepts params: "{is_clear_folder}", "{data_type}"
    ...    Keyword to export dgraph data to either json/rdf format in local
    ${root_path}=    normalize path    ${CURDIR}/..
    ${export_path}=    Join Path    ${root_path}/export
    Run Keyword If    ${is_clear_folder}    clear all the folder in a directory    ${export_path}
    connect request server       is_learner=${GLOBAL_IS_LEARNER}
    ${res}=    Export Nfs Data Admin    data_format=${data_type}    destination=${export_path}
    log    ${res.text}
    Verify files exists in directory    ${export_path}


Perform a restore on backup latest versions
    [Arguments]  ${increment_size}
    [Documentation]    Performs an restore operation on the default location i.e "backup" dir.
    Connect request server      is_learner=${GLOBAL_IS_LEARNER}
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
    ${tls_check}=    Get Tls Value
    ${enc_check}=    Get Enc Value
    Run Keyword If     ${enc_check} is ${True}    List Should Contain Value   ${enc}     ${TRUE}
    ${cmd}  Catenate   dgraph   restore -p ${backup_path} -l ${backup_path} -z localhost:5080
    ${result_restore}=    Run Keyword If    ${tls_check}    Restore Using Admin    ${backup_path}
    ...    ELSE    Run Keywords    Start Process   ${cmd}      alias=restore    stdout=restorebackup.txt    cwd=results     shell=True
    ...    AND    Process Should Be Running    restore
    ...    AND    Wait For Process    restore
    ...    AND    Process Should Be Stopped    restore
    ...    AND    Sleep    5s
    ...    AND    Verify Restore File Content In Results Folder    restorebackup    ${backup_path}
    Health Check for Restore Operation

Perform a restore on backup by older dgraph versions
    [Documentation]    Performs an restore operation on the default location i.e "backup" dir.
    Connect request server      is_learner=${GLOBAL_IS_LEARNER}
    ${root_dir}=    normalize path    ${CURDIR}/..
    ${path}=    Join Path    ${root_dir}/backup
    @{dirs_backup}=    List Directories In Directory    ${path}
    ${cmd}  Catenate   dgraph   restore -p ${backup_path} -l ${backup_path} -z localhost:5080
    FOR     ${i}  IN    ${dirs_backup}
        ${restore_dir}=    Set Variable    ${i}[0]
        ${restore_dir}=    Join Path    ${root_dir}/backup/${restore_dir}
        ${tls_check}=    Get Tls Value
        ${result_restore}=    Run Keyword If    ${tls_check}   Restore Using Admin    ${restore_dir}
        ...    ELSE    Run Keywords    Start Process    ${cmd}      alias=restore    stdout=restorebackup.txt    cwd=results    shell=True
        ...    AND    Process Should Be Running    restore
        ...    AND    Wait For Process    restore
        ...    AND    Process Should Be Stopped    restore
        ...    AND    Sleep    5s
        ...    AND    Verify Restore File Content In Results Folder    restorebackup    ${restore_dir}
        Health Check for Restore Operation
    END


Health Check for Restore Operation
    [Documentation]  Keyword to verify if backup operation is completed successfully
    Wait Until Keyword Succeeds    20x    30 sec       Connect Request Server   is_learner=${GLOBAL_IS_LEARNER}
    Wait Until Keyword Succeeds    600x    30 sec      Check if restore is completed

Check if restore is completed
    [Documentation]    Keyword to check if the restore operation is performed sucessfully
    ${response}=    Health Check    /health
    ${passed}    Run Keyword And Return Status   Should Be String    ${response}
    Run Keyword If  ${passed}
    ...     Evaluate    '${response}'=='the server is in draining mode and client requests will only be allowed after exiting the mode  by sending a GraphQL draining(enable: false) mutation to /admin'    Fail


Verify process to be stopped
    [Arguments]    ${process_alias}
    [Documentation]    Keyword to check if the process is still running and wait till process completes.
    log    Process which is runing ${process_alias}
    ${process_check}=    Is Process Running    ${process_alias}
    Run Keyword If    ${process_check}==${FALSE}    Return From Keyword
    FOR    ${i}    IN RANGE    99999
        log    ${i}
        Wait For Process    ${process_alias}
        ${process_check}=    Is Process Running    ${process_alias}
        Exit For Loop If    ${process_check}==${FALSE}
    END
    Log    ${process_alias} Process is stopped
    Comment    Wait Until Keyword Succeeds    600x    5minute    Process Should Be Stopped    handle=${process_alias}    error_message=${error_message} is still running

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

Verify files exists in directory
    [Arguments]    ${path}
    [Documentation]    Keyword to verify if a file exists in a directory
    ...    Accepts one argument "{path}" <- which indicates the path of the direcory
    ${rest}    ${folder_name}=    Split String From Right    ${path}    /    1
    @{dirs}=    List Directories In Directory    ${path}
    FOR    ${dir}    IN    @{dirs}
        directory should exist    ${folder_name.strip()}/${dir}
    END


Verify Perticular file contents in results folder
    [Arguments]    ${file_name}    ${count}=${0}     @{context}
    [Documentation]    Keyword for checking content in .txt file generated in results folder
    ...    [Arguments] -> "file_name" -file name ex: alpha for alpha.txt | "cotent" -content you want to check in file
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${count_check}=    Evaluate   ${count} - 1
    ${file_name}=    Set Variable IF  ${count} != 0  ${file_name}_${count_check}     ${file_name}
    ${file_context}=    Get File    ${dir_path}/results/${file_name}.txt
    Should Contain Any    ${file_context}    @{context}

Verify alpha and zero contents in results folder
    [Arguments]    ${file_name}   ${count}      @{context}
    [Documentation]    Keyword for checking content in .txt files generated in results folder
    ...    [Arguments] -> "file_name" -file name ex: alpha for alpha.txt | "cotent" -content you want to check in file
    ${dir_path}=    normalize path    ${CURDIR}/..
    FOR     ${i}  IN RANGE   ${count}
        ${file_context}=    Get File    ${dir_path}/results/${file_name}_${i}.txt
        Should Contain Any    ${file_context}    @{context}
    END

Grep and Verify file Content in results folder
    [Arguments]    ${file_name}    ${grep_text}
    [Documentation]    Keyword for grepping and checking content in .txt files generated in results folder
    ...    [Arguments] -> "file_name" -file name ex: alpha for alpha.txt | "cotent" -content you want to check in file
    ${dir_path}=    normalize path    ${CURDIR}/..
    ${grep_file}=    Grep File    ${dir_path}/results/${file_name}.txt    ${grep_text}
    Should Contain    ${grep_file}    ${grep_text}

Monitor zero and alpha process
    [Arguments]     ${is_clear_folder}    ${is_alpha_retrigger}=${FALSE}  ${is_alpha_learner_retrigger}=${FALSE}  ${is_zero_retrigger}=${FALSE}
    [Documentation]    Keyword to monitor zero and alpha process to run
    Run Keyword If Test Failed     Run Keywords    Terminate All Processes
    ...     AND     Sleep   20s
    ...     AND     Backup directories created while execution
    ...     AND     Run Keyword If    ${is_clear_folder}    clean up dgraph folders
    ...     AND     Run Keyword And Return If  ${LUDICROUS_MODE}   Start Dgraph Ludicrous Mode
    ...     AND     Run Keyword And Return If   ${is_alpha_learner_retrigger}    Start Dgraph with learner node
    ...     AND     Run Keyword And Return      Start Dgraph
    IF      ${is_zero_retrigger}
        End Zero Process
        @{dir}  Create List     w   zw
        Post Execution Verify Zero contents  
        Backup Custom Directories Created While Execution  @{dir}   
    ELSE
        Post Execution Verify Zero contents
    END

    IF  ${is_alpha_learner_retrigger}
        End Alpha Learner Process
        Post Execution Verify Alpha contents
        @{dir}  Create List     alpha_learner_p     alpha_learner_w
        Backup Custom Directories Created While Execution  @{dir}
    ELSE
        Post Execution Verify Alpha contents
    END
    IF     ${is_alpha_retrigger}   
        End Alpha Process
        Post Execution Verify Alpha contents
        @{dir}  Create List     p   t
        Backup Custom Directories Created While Execution  @{dir}
    ELSE
        Post Execution Verify Alpha contents
    END
    
    IF  ${LUDICROUS_MODE}
        Start Dgraph Ludicrous Mode
    ELSE IF   ${is_learner}
        Start Dgraph with learner node
    ELSE
        Start Dgraph
    END

Monitor health and state check
    [Documentation]   Keyword to check the health and state of the connection.
    Monitor health check
    Monitor State Check

Monitor health check
    [Documentation]   Keyword to check the health of the connection.
    connect request server  is_learner=${GLOBAL_IS_LEARNER}
    ${response}=    Health status Check    /health
    log     ${response}
    Run Keyword If      "${response}" != "healthy"      Fail    Health check is un-healthy

Monitor State Check
    [Documentation]  Keyword to check the state of the process.
    connect request server  is_learner=${GLOBAL_IS_LEARNER}
    ${state_resposne}=  State Check     /state
    ${leader}=    Get Value From Json   ${state_resposne}   $..members..leader
    ${am_dead}=    Get Value From Json   ${state_resposne}   $..members..amDead
    Should Be Equal As Strings  ${leader[0]}   ${TRUE}
    Should Be Equal As Strings  ${am_dead[0]}   ${FALSE}

Clear Backup Folders
    [Documentation]  Keyword to clear backup folders
    [Arguments]  ${is_clear_folder}
    ${root_path}=    normalize path    ${CURDIR}/..
    ${backup_path}=    Join Path    ${root_path}/backup
    Run Keyword If    ${is_clear_folder}    clear all the folder in a directory    ${backup_path}

clean up dgraph folders
    [Documentation]    Keyword to clear up the dgraph alpha and zero folder created.
    ${curr_dir}=    Normalize Path    ${CURDIR}/..
    @{dir}    Create List    w   zw  p   t  out  alpha   tmp     alpha_learner_p     alpha_learner_w
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

Clear all the folder in a directory
    [Arguments]    ${path}
    [Documentation]    Keyword to clear all the folder in a directory
    ...    Accepts one argument "{path}" <- which indicates the path of the direcory
    @{dirs}=    List Directories In Directory    ${path}
    ${list_size}    Get Length    ${dirs}
    Run Keyword If    ${list_size}>0    Empty Directory    ${path}

Create Backup Logs Folder
    [Documentation]  Keyword to create backup logs folder name
    ${datetime} =	Get Current Date      result_format=%d-%m-%Y-%H-%M-%S
    Run Keyword If    '${GLOBAL_BACKUP_LOGS_FOLDER}'=='${EMPTY}'     Set Suite Variable      ${GLOBAL_BACKUP_LOGS_FOLDER}   exe_logs_${datetime}

Backup alpha and zero logs
    [Documentation]     Kewyword to backup all the logs
    Move Files      results/*.txt	   results/${GLOBAL_BACKUP_LOGS_FOLDER}

Backup directories created while execution
    [Documentation]     Keyword to backup execution time directories
    @{alpha_alias}      Create List     alpha   alpha_bulk   alpha_bulk_learner  alpha_learner      alpha_ludicrous     alpha_learner_ludic   alpha_ludicrous_bulk
    @{alpha_counts}     Create List     ${ALPHA_COUNT}  ${ALPHA_BULK_COUNT}     ${ALPHA_LEARNER_BULK_COUNT}     ${ALPHA_LEARNER_COUNT}      ${ALPHA_LUDICROUS_COUNT}    ${ALPHA_LEARNER_LUDIC_COUNT}    ${ALPHA_LUDICROUS_BULK_COUNT}
    ${index}=    Set Variable    0
    FOR  ${i}  IN    @{alpha_alias}
        ${log_count}    Set Variable  ${alpha_counts}[${index}]
        FOR  ${l_count}  IN RANGE  ${log_count}
            ${passed}   Run Keyword and Return Status   Directory Should Exist      results/${i}_${l_count}
            Run Keyword If  ${passed}   Move Directory   results/${i}_${l_count}   results/${GLOBAL_BACKUP_LOGS_FOLDER}/${i}_${l_count}
        END
        ${index}=    Evaluate    ${index} + 1
    END
    @{dirs}     Create List     w   zw  p   t  out   tmp     bulk    parallel_bulk
    FOR  ${i}  IN    @{dirs}
        ${passed}   Run Keyword and Return Status   Directory Should Exist      results/${i}
        Run Keyword If  ${passed}   Move Directory   results/${i}   results/${GLOBAL_BACKUP_LOGS_FOLDER}/${i}
    END

Backup Custom Directories Created While Execution
    [Arguments]       @{dirs_to_backup}
    [Documentation]     Keyword to backup execution time directories
    ${count}    Evaluate    ${ALPHA_COUNT} - 1
    FOR  ${i}  IN    @{dirs_to_backup}
        ${passed}   Run Keyword and Return Status   Directory Should Exist      results/${i}
        Run Keyword If  ${passed}   Move Directory   results/${i}   results/${GLOBAL_BACKUP_LOGS_FOLDER}/${i}_${count}
    END