# Automation
This is a Automation Repo for Dgraph including Slash.

###### Commands from the root directory
* To run the suite `robot -d results test_suites/dgraph/Linux/dgraph_suite.robot`
* To pass arguments from terminal `robot -d results -v rdf_file:2million.rdf.gz -v schema_file:testschema.schema test_suites/dgraph/Linux/dgraph_suite.robot`

- [x] results are stored under results
- [ ]   backup and restore are defaulted to backup/ directory
- [x] test data is present under test_data/datasets

###### Folders:
* test_suites/dgraph/Linux/ contains the main execution test suite
    * draph_suite.robot
* test_suites/sample_test_cases holds the code creation data.
    * backup_suite.robot - for all the back realted operations
    * liveloader_suite.robot - for all the live loader realted operations.
    * dd_test.robot - for any new implementations of robot-framework.

###### External Libraries
* Slash Selenium Library - Selenium Client calls for all the UI operations like click,sendkeys etc are handled here.
    * use `Library SlashSeleniumClient`
* Slash UI Library - Custom keywords realted to handling the browser also for organizing the locators and custom reusable actions related to slash are handled here.
    * use `Library Slash`
* RequestHandler - handles the request calls for performing backup (will be updated based on dgraph request calls).
    * To use the library 
        * use `Library      RequestHandler.CustomRequestKeywords`

###### Resources
* dgraph_commands.robot <- all the reusable keywords build using build-in and external keywords for the test cases go here.


###### Common Problems:
* While creating External Library.
    * make sure the file name and python class name are same. for reference check the file at `lib/external_keywords/custom_request_library/RequestHandler/keywords/custom_request_keywords`
* Incase of any error while executing backup
    * make sure backup folder is present in the root folder.

