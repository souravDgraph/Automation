*** Settings ***
Documentation     This Suite contains the sanity test cases for Slash UI
Test Setup        Setup
Test Teardown     Close Browser    ${Browser_Alias}
Library           Slash
Variables         ../../conf/slash/variables.py
Library           AWSLibrary
Library           OperatingSystem

*** Variables ***
${Browser_Alias}    Browser1
${invalid_user_alert}    No user found with this email
${invalid_email}    a@b.com

*** Test Cases ***
User should be able to create API Key
    



*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}
