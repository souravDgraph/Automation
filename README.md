# Automation
This is a Automation Repo for Dgraph including Slash.

## Table of Contents

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


# Framework Setup
* Goto utilities dir-> run `python env_setup.py -l Dgraph -c disabled` || `python env_setup.py -l Slash` in the terminal to install all the dependencies related to the particular library.
* Added Common Library for TestRails and Pydgraph `python env_setup.py -l Common`

## Execution Commands:
* To run the suite with virtualenv enabled `cd utilities &&  runner.sh -l Dgraph -c disabled -t /Users/souravmukherjee/Desktop/Sourav/office/repos/Automation/test_suites/dgraph/Linux/dgraph_suite.robot`. This is a prefered way to execute.
* To run individual suite without virtualenv setup `robot -d results test_suites/dgraph/Linux/dgraph_suite.robot`
* To pass arguments from terminal `robot -d results -v rdf_file:2million.rdf.gz -v schema_file:testschema.schema test_suites/dgraph/Linux/dgraph_suite.robot`

- [x] results are stored under results
- [x] backup and restore are defaulted to "backup/" directory
- [x] test data is present under test_data/datasets

# Framework Structure:
*   ##  conf:
    * Contains the configurations required in the test suite or test cases.
    * Configure all the options for zero and alpha at `conf_dgraph.json` under Dgraph based on requirement.
        * Enabling ACL
        * Enabling Encryption.
        * Enabling TLS and mTLS
    * Test Case global arguments are declared over here.
*   ## doc:
    * Contains all the  documents for generated lib keywords.

*   ## lib:
    * Contains the custom keywords defined for the Dgraph and Slash.
    * Slash Selenium Library - Selenium Client calls for all the UI operations like click,sendkeys etc are handled here.
        * use `Library SlashSeleniumClient`
    * Slash UI Library - Custom keywords related to handling the browser also for organizing the locators and custom reusable actions related to slash are handled here.
        * use `Library Slash`
    * Dgraph Library - Contains Keywords generated from CustomRequestKeywords, TestRailsKeywords and SetupDgraphKeywords .
        * use `Library  Dgraph`

*   ##  resources:
    * Contains the reusable keywords for the Dgraph and Slash.
        * dgraph_commands.robot <- all the reusable keywords build using build-in and external keywords for the test cases go here.

*   ##  results:
    * Contains all the results generated by the test suite execution.
    * Folder created by zero, alpha, restore and bulk are stored over here.
    * All the log files generated as part of execution are stored here.

*   ##  test_data:
    * Test data required for the execution for backup, live loading and bulk are stored here.

*   ##  test_suites:
    * Test Suites for Dgraph and Slash are stored here.
    * test_suites/dgraph/Linux/ contains the main execution test suite
        * dgraph_suite.robot
    * test_suites/sample_test_cases holds the code creation data.
        * backup_suite.robot - for all the backup related operations
        * liveloader_suite.robot - for all the live loader related operations.
        * dd_test.robot - for any new implementations of robot-framework.
        * bulkloader.robot - for all the test cases related to bulk
*   ##  utilities:
    * Contains the initial Setup for the framework.

*   ## backup:
    * dir to store the backup files created from live and bulk loading.

#### Docs generation:
* run the command `python3 -m robot.libdoc <lib_name> <save_location/file_type>`
    * Ex: `python3 -m robot.libdoc Dgraph doc/Dgraph.html`.

#### Common Problems:
* While creating External Library.
    * make sure the file name and python class name are same. for reference check the file at `lib/external_keywords/Dgraph_Lib/Dgraph/keywords/Dgraph/dgraph.py`
* Incase of any error while executing backup
    * make sure backup folder is present in the root folder.

#### Useful Commands
* For setting custom log and report title use `--logtitle and --reporttitle`.
* To specify time stamps use ` --timestampoutputs`.
* To specify log-level  use `--loglevel DEBUG:INFO` 

