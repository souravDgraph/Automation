# Dgraph Robot Framework Automation - v21.03-slash
> *Make sure that the local version matches with v21.03-slash before execution while using binary*

**This is a Automation Repo for Dgraph including Slash.**

Nightly | CI  |  Weekely  | Docker
--------|-----|-----------|-------
[![nightly](https://teamcity.dgraph.io/guestAuth/app/rest/builds/buildType:(id:Dgraph_QA_Nightly_Automation)/statusIcon.svg)](https://teamcity.dgraph.io/viewLog.html?buildTypeId=Dgraph_QA_Nightly_Automation&buildId=lastFinished&guest=1)          |      [![CI Build Status](https://teamcity.dgraph.io/guestAuth/app/rest/builds/buildType:(id:QADgraphAutomation)/statusIcon.svg)](https://teamcity.dgraph.io/viewLog.html?buildTypeId=QADgraphAutomation&buildId=lastFinished&guest=1)        |       [![weeklyLargeData](https://teamcity.dgraph.io/guestAuth/app/rest/builds/buildType:(id:Dgraph_QA_Weekely_Automation)/statusIcon.svg)](https://teamcity.dgraph.io/viewLog.html?buildTypeId=Dgraph_QA_Weekely_Automation&buildId=lastFinished&guest=1)   |       [![docker_execution](https://teamcity.dgraph.io/guestAuth/app/rest/builds/buildType:(id:Dgraph_QA_Docker_Execution)/statusIcon.svg)](https://teamcity.dgraph.io/viewLog.html?buildTypeId=Dgraph_QA_Docker_Execution&buildId=lastFinished&guest=1)

## Table of Contents

* [Framework Features](#framework-features) 
* [Framework Setup](#framework-setup)
* [Execution Commands](#execution-commands)
* [Framework Structure](#framework-structure)
  * [conf](#config)
  * [doc](#doc)
  * [lib](#lib)
  * [resources](#resources)
  * [results](#results)
  * [test_data](#test_data)
  * [test_suites](#test_suites)
  * [utilities](#utilities)
  * [backup](#backup)
* [Docs generation](#docs-generation)
* [Common Problems](#common-Problems)
* [Useful Commands](#useful-commands)

## Framework Setup

* Goto utilities dir-> run `python env_setup.py -l All -c disabled -o 0` in the terminal to install all the dependencies related to the framework.
  * -l (library):
    * `all`: To setup all the external libraries for robot framework.
  * -c (Configuration):
    * `enabled`: To enable all the configuraitons
    * `disbaled`: To disable all the configurations
  * -o (off set value for zero and alpha):
    * `200`: When set, alpha and zero ports are triggered with 200 as offset value
* To install particular library goto utilities dir->  run `python env_setup.py -l <project_name>`
  * All -c enabled | disabled  -o 0 | 200
  * Dgraph -c enabled | disabled  -o 0 | 200
  * Slash
  * Common
  * CustomTestRailListener
* To run dgraph using docker file goto test_suites/dgraph/docker dir->
  * Setup supports
    * 2node - ( 1 zero and 1 alpha ) 
    * 4node - ( 1 zero and 3 alpha ) **under progress

## Framework Features:

* **Binary Support with 1 cluster**:
  * Alpha with Learner Node Suite:
    * `test_suites/dgraph/Linux/dgraph_suite_04.robot`
    * To execute use:
      * `robot -A conf/dgraph_learner_args.txt`
  * Alpha in Ludicrous Mode Suite:
    * `test_suites/dgraph/Linux/dgraph_suite_03.robot`
    * To execute use:
      * `robot -A conf/dgraph_ludicrous_args.txt`
  * Dgraph Sanity Test Suite:
    * `test_suites/dgraph/Linux/dgraph_suite_01.robot`
    * To execute use:
      * `robot -A conf/dgraph_live_args.txt`
* **Docker Support:**
  * Currently supports only 2 node (1 cluster)
    * Can be run only in `sudo` mode.
    * Test suite is present at:
      * `test_suites/dgraph/docker/dgraph_docker_2-node_suite.robot`
    * To Execute 2-node Docker Suite:
      * `sudo robot -A conf/dgraph_docker_args.txt`

* [x] Results are stored under **results/**
* [x] Backup and Restore are defaulted to **backup/**
* [x] Test Data is present under **test_data/datasets/**


## Execution Commands

* To run the suite with virtualenv enabled
  * `cd utilities &&  runner.sh -l Dgraph -c disabled -t <absoulte_path>/Automation/test_suites/dgraph/Linux/dgraph_suite.robot`. This is a prefered way to execute.
* To run individual suite without virtualenv setup
  * `robot -d results test_suites/dgraph/Linux/dgraph_suite_01.robot`
* To set variables from terminal pass `-v <variablename>:<value>`
  * `robot -d results -v rdf_file:21million.rdf.gz -v schema_file:21million.schema test_suites/dgraph/Linux/dgraph_suite_01.robot`
* To run from arguments file
  * `robot -A conf/dgraph_live_args.txt`

## Framework Structure

* ##  conf

  * Contains the configurations required in the test suite or test cases.
  * Configure all the options for zero and alpha at `conf_dgraph.json` under Dgraph based on requirement.
    * Enabling ACL
    * Enabling Encryption.
    * Enabling TLS and mTLS
  * Test Case global arguments are declared over here.

* ## doc

  * Contains the documentation for the keywords used, generated by the custom libraries created.

* ## lib

  * Contains the custom keywords defined as part of Dgraph and Slash.
  * Slash Selenium Library - Selenium Client calls for all the UI operations like click,sendkeys etc are handled here.
    * use `Library SlashSeleniumClient`
    * setup: `python env_setup.py -l Slash`
  * Slash UI Library - Custom keywords related to handling the browser also for organizing the locators and custom reusable actions related to slash are handled here.
    * use `Library Slash`
    * setup: `python env_setup.py -l Slash`
  * SlashAPI Library - Custom keyword related to the API automation of slash endpoints.
    * use `Library SlashAPI`
    * setup: `python env_setup.py -l Slash`
  * Dgraph Library - Contains Keywords generated from CustomRequestKeywords, TestRailsKeywords and SetupDgraphKeywords .
    * use `Library  Dgraph`
    * setup: `python env_setup.py -l Dgraph -c enabled | disabled`
  * CustomTestRailListener Library - Listener Library which contains keywords to update execution results.
    * use `Library  CustomTestRailListener`
    * setup: `python env_setup.py -l CustomTestRailListener`
  * Common Library - Contains Common Keywords which can be used across Slash and Dgraph.
    * use `Library  Common`
    * setup: `python env_setup.py -l Common`

* ##  resources

  * Contains the reusable keywords for the Dgraph and Slash.
    * dgraph_commands.robot <- all the reusable keywords build using build-in and external keywords for the test cases go here.

* ##  results

  * Contains all the results generated by the test suite execution.
  * Folder created by zero, alpha, restore and bulk are stored over here.
  * All the log files generated as part of execution are stored here.

* ##  test_data

  * Test data required for the execution for backup, live loading and bulk are stored here.

* ##  test_suites

  * Test Suites for Dgraph and Slash are stored here.
  * test_suites/dgraph/Linux/ contains the main execution test suite
    * dgraph_suite.robot
  * test_suites/sample_test_cases holds the code creation data.
    * backup_suite.robot - for all the backup related operations
    * liveloader_suite.robot - for all the live loader related operations.
    * dd_test.robot - for any new implementations of robot-framework.
    * bulkloader.robot - for all the test cases related to bulk

* ##  utilities

  * Contains the initial Setup for the framework.

* ## backup

  * dir to store the backup files created from live and bulk loading.

## Docs generation

* run the command `python3 -m robot.libdoc <lib_name> <save_location/file_type>`
  * Ex: `python3 -m robot.libdoc Dgraph doc/Dgraph.html`.

## Common Problems

* While creating External Library.
  * make sure the file name and python class name are same. for reference check the file at `lib/external_keywords/Dgraph_Lib/Dgraph/keywords/Dgraph/dgraph.py`
* Incase of any error while executing backup
  * make sure backup folder is present in the root folder.

## Useful Commands

* For setting custom log and report title use `--logtitle and --reporttitle`.
* To specify time stamps use `--timestampoutputs`.
* To specify log-level  use `--loglevel DEBUG:INFO`
