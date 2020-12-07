*** Settings ***
Documentation    Data Driven Dgraph Live Loading Test Suite

Library           OperatingSystem
Library           String
Library           Process
Library     DataDriver      ../../../test_data/liveloading_datasets/liveload.csv
Resource    ../../../resources/dgraph_commands.robot
Resource    ../../../resources/dgraph_initiation.robot

Suite Setup     Start Dgraph
Suite Teardown  End All Process
Test Template   Template for live loader execution

*** Test Cases ***
Import a big dataset with the live loader - Ubuntu or CentOS
    ${rdf_filename}     ${schema_filename}


