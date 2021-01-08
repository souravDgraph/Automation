*** Settings ***
Documentation     This is a simple test with Robot Framework
Suite Teardown
Test Setup
Test Teardown
Library           SlashAPI
Library           Collections

*** Variables ***
${Browser_Alias}    Browser1
${Auth}           eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1ETXlNemcyTnpFME1qTkNORUUzTWpZME1UVTJNa0pCTVRjMFFUUkVPVEJFT0VZNE5UWXhSUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kZ3JhcGgtc2Fhcy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDA5ODU2MDI0NDA2Njk3NTI1ODIiLCJhdWQiOlsiaHR0cDovL2xvY2FsaG9zdDo4MDcwIiwiaHR0cHM6Ly9kZXYtZGdyYXBoLXNhYXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwOTc3NDg0NSwiZXhwIjoxNjA5ODYxMjQ1LCJhenAiOiJnYnBWcTdpMWdNdmdtdEkzbXVBem9aSEpiVTJieDVqdCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.dOVxBZOLkP6ADknAPuPpfimOEE82cP2TUdFYr5aTwbPc99B75cYGZrV3F7iM20LXcB3tvAp3lRZAoI3j22iVLVHNarRJrdp7e6uFqswVvGundfZVbmXezyxEZIWu0a1Q5Nfzv1Ct6GxUC6at2N6RaOtwHj-lCJdGlImHKpz97fiYlqpOVNdzKFm3xRQdu7hgcIJn97tvwH4AUpJ9Pn1KVmKcQGD5npNhNO4QhHW4tFBXZHwQt7zrX-xBMKewg6zx2ZR2maDnFC9Ty_TnVLPk63YchGur6ANgJr_CPgmVkYfToG7OMXZRPXwgIsVvqwm14-_BPXKZiXh7dVjU0jt9mg

*** Test Cases ***
launch and login
    [Tags]    Sanity    Regression
    Click Launch New Backend    ${Browser_Alias}
    Fill Backend Details    ${Browser_Alias}    ${BACKEND_NAME}    organization=${ORGANIZATION}
    Click Launch Button    ${Browser_Alias}
    Monitor Backend Creation    ${Browser_Alias}    ${BACKEND_MONITORING_TIMEOUT}
    Click Lambdas In Menu    ${Browser_Alias}
    ${lambda_script}=    Get File    ../../conf/slash/lambda_script
    log    ${lambda_script}
    Fill Lambda Script    ${Browser_Alias}    ${lambda_script}
    Click Settings In Menu    ${Browser_Alias}
    Validate General Tab Data    ${Browser_Alias}    ${BACKEND_NAME}    ${ORGANIZATION}
    Update Backend Organization    ${Browser_Alias}    ${NEW_ORGANIZATION}
    Delete Deployment    ${Browser_Alias}    ${BACKEND_NAME}

test
    ${header}=    Create Dictionary    Authorization=Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1ETXlNemcyTnpFME1qTkNORUUzTWpZME1UVTJNa0pCTVRjMFFUUkVPVEJFT0VZNE5UWXhSUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kZ3JhcGgtc2Fhcy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDA5ODU2MDI0NDA2Njk3NTI1ODIiLCJhdWQiOlsiaHR0cDovL2xvY2FsaG9zdDo4MDcwIiwiaHR0cHM6Ly9kZXYtZGdyYXBoLXNhYXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYxMDEwMjYzNiwiZXhwIjoxNjEwMTg5MDM2LCJhenAiOiJnYnBWcTdpMWdNdmdtdEkzbXVBem9aSEpiVTJieDVqdCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.R_4IMtK3jDIPMRCQUZEcFQKuXY23vqttsvsD0jxrDtBaI0__C9iva2VmaFncS3Iwib3jLkfIjMgSwuo0nPvG6xNSNtDfM52mQV9Z2wUOzNo7p9ocRlMvoUnFIC91kidnc1NAdpgBaXVhvR3E2_1NXt9WUaelfWRPamRzeNcIY9KdvsBy-oGBMxR661JHJlLaWNVTp_qthX_GBFZPxwXjxoj0PEnyigYdOHeUnwEHMEFQqxX5gObOAZRtR0WhKmT1tPhqhKOpurQIn1357EsimWbQ3w8XJOQKsJO5a4EnoyoEVeqHuLf7OWtO1FggigT5W6ABAxLoOZbW3LHGQA1TTQ    Content-Type=application/json
    ${data}=    Create Deployment    test    https://api.thegaas.com    ${header}    test2    us-east-1
    Validate Created Deployment    ${data}    test2    us-east-1
    ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    Comment    Delete Deployment    test    https://api.thegaas.com    ${header}    ${deployment_id}

delete deployment
    ${header}=    Create Dictionary    Authorization=Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1ETXlNemcyTnpFME1qTkNORUUzTWpZME1UVTJNa0pCTVRjMFFUUkVPVEJFT0VZNE5UWXhSUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kZ3JhcGgtc2Fhcy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDA5ODU2MDI0NDA2Njk3NTI1ODIiLCJhdWQiOlsiaHR0cDovL2xvY2FsaG9zdDo4MDcwIiwiaHR0cHM6Ly9kZXYtZGdyYXBoLXNhYXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYxMDEwMjYzNiwiZXhwIjoxNjEwMTg5MDM2LCJhenAiOiJnYnBWcTdpMWdNdmdtdEkzbXVBem9aSEpiVTJieDVqdCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.R_4IMtK3jDIPMRCQUZEcFQKuXY23vqttsvsD0jxrDtBaI0__C9iva2VmaFncS3Iwib3jLkfIjMgSwuo0nPvG6xNSNtDfM52mQV9Z2wUOzNo7p9ocRlMvoUnFIC91kidnc1NAdpgBaXVhvR3E2_1NXt9WUaelfWRPamRzeNcIY9KdvsBy-oGBMxR661JHJlLaWNVTp_qthX_GBFZPxwXjxoj0PEnyigYdOHeUnwEHMEFQqxX5gObOAZRtR0WhKmT1tPhqhKOpurQIn1357EsimWbQ3w8XJOQKsJO5a4EnoyoEVeqHuLf7OWtO1FggigT5W6ABAxLoOZbW3LHGQA1TTQ    Content-Type=application/json
    Delete Deployment    test    https://api.thegaas.com    ${header}    0x2c54e

*** Keywords ***
Setup
    Open Browser    ${Browser_Alias}    ${URL}    Chrome
    Login    ${Browser_Alias}    ${USER_NAME}    ${PASSWORD}
