*** Settings ***
Documentation     Dgraph Live Loading Test Suite
Suite Setup        Start Dgraph    local
Suite Teardown     End All Process    true
Resource          ../../../resources/dgraph_commands.robot
Library           Dgraph
Library           String

*** Variables ***
${URL}            http://localhost:8080
${rdf_file}       1million.rdf.gz
${schema_file}    1million.schema
${appenders}      /admin

*** Test Cases ***
TC_01 Perform live load backup restore data.
     [Documentation]    Perform live load data.
     ...    *Author*: Krishna, Sourav and Sankalan
     [Tags]    regression   C698
     Execute Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}     live

TC_02 Perform bulk load backup restore data.
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression
     Execute Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}     bulk

TC_03 Perform NFS backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Krishna, Sourav and Sankalan
     [Tags]    regression   C702    C700
     Create NFS Backup    ${URL}    ${appenders}    full
     perform a restore on backup    ${URL}

TC_04 Perform parallel live and bulk load backup restore data.
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression
     Execute Parallel Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}

TC_05 Perform Increment backup and restore data
     [Documentation]    Perform NFS backup and restore data.
     ...    *Author*: Sourav
     [Tags]    regression
     Create NFS Backup    ${URL}    ${appenders}    full
     Create NFS Backup    ${URL}    ${appenders}    increment
     perform a restore on backup    ${URL}

TC_06 Perform parallel live loads.
     [Documentation]    Perform live load data.
     ...    *Author*: Sourav
     [Tags]    regression
     Execute Multiple Parallel Live Loader with rdf and schema parameters    ${rdf_file}    ${schema_file}    2
