*** Settings ***
Documentation       It contains Security Test Cases for Slash API
Suite Setup         Create Backend
Suite Teardown      Delete Deployment		${Session_alias}		${URL}		${HEADERS}		${deployment_id}
Test Setup			
Test Teardown
Default Tags	    Security
Library		    	SlashAPI
Library		    	Collections
Variables	    	../../../conf/slash/slash_api/variables.py

*** Variables ***
${Session_alias}	Session1
${org_name}		Dgraph_Lab
${user_email}		santhosh@dgraph.io
${API_name}		Test
${response}		The organization is not found.
${API_endpoint}		https://api.stage.thegaas.com

*** Test Cases ***
Delete API Key With Correct User
	[Documentation]		
    ...     List of Test Covered
	...
	...		- Create API Key with User Auth
	...		- Get API Key
	...		- Delete API Key with User Auth
	${api_key_details}=	Create Api Key	    ${Session_alias}	  ${URL}      ${HEADERS}     ${deployment_id}	  ${API_name}
	${details}=    Collections.Get From Dictionary    ${api_key_details}    data
    ${api_key_details}=    Collections.Get From Dictionary    ${details}    createAPIKey
    ${api_key_uid}=    Collections.Get From Dictionary    ${api_key_details}    uid	
	Delete Api Key	    ${Session_alias}	  ${URL}      ${HEADERS}	${deployment_id}    ${api_key_uid}     API Key Deleted Successfully.

Delete API Key With Different User
	[Documentation]		
    ...     List of Test Covered
	...
	...		- Create API Key with User Auth
	...     - Get API Key
	...		- Delete API Key with Different User Auth
	${api_key_details}= 	Create Api key		${Session_alias}	${URL}	    ${HEADERS}	     ${deployment_id}		${API_name}
	${details}=    Collections.Get From Dictionary    ${api_key_details}    data
    ${api_key_details}=    Collections.Get From Dictionary    ${details}    createAPIKey
    ${api_key_uid}=    Collections.Get From Dictionary    ${api_key_details}    uid	
	Delete Api Key	   ${Session_alias}	${URL}	    ${USER2_HEADER}	  ${deployment_id}	${api_key_uid}	    Unauthorized
	Delete Api Key	   ${Session_alias}	${URL}      ${HEADERS}	   ${deployment_id}	   ${api_key_uid}     API Key Deleted Successfully.

Only Owner Add Member To Organization
	[Documentation]		
    ...     List of Test Covered
	...
	...		- Create Organization
	...		- Add a member to the organization
	...		- Get Organization ID
	...		- Remove a member
	...		- Add a member to the organization with another user auth
	Create Session For Organization      ${HEADERS}     ${API_endpoint}
	${org_details}=		Create Organization	${org_name}	200
	log 	${org_details}
	${details}=    Collections.Get From Dictionary    ${org_details}    data
    ${organization}=    Collections.Get From Dictionary    ${details}    createOrganization
    ${org_uid}=    Collections.Get From Dictionary    ${organization}    uid
	${data}=	Add New Member To Existing Organization		${org_uid}	   ${user_email}
	log		${data}
	Remove Member From Existing Organization    ${org_name}     ${user_email}
	Create Session For Organization 	 ${USER2_HEADER}     ${API_endpoint}
	Add New Member To Existing Organization		${org_uid}	${user_email}	  ${response}

Only Owner View Members From Organization
	[Documentation]		
    ...     List of Test Covered
	...
	...		- Create Organization
	...		- Add a member to the Organization
	...		- Get Organization uid
	...		- View members from Organization
	...		- Create a session for another user
	...		- View members with another user auth
	Create Session For Organization     ${HEADERS}    ${API_endpoint}
	${org_details}=		Create Organization	   ${org_name}	  200
	log 	${org_details}
	${details}=    Collections.Get From Dictionary    ${org_details}    data
    ${organization}=    Collections.Get From Dictionary    ${details}    createOrganization
    ${org_uid}=    Collections.Get From Dictionary    ${organization}    uid
	Add New Member To Existing Organization	    ${org_uid} 	   ${user_email}
	${data}=	Get Members From Organization	  ${org_uid}
	log	  ${data}
	Remove Member From Existing Organization    ${org_name}    ${user_email}
	Create Session For Organization     ${USER2_HEADER}    ${API_endpoint}
	Get Members From Organization	  ${org_uid}	 ${response}

Only Owner Fetch the Organization
	[Documentation]		
    ...     List of Test Covered
	...
	...		- Create Organization with User 2
	...		- Get Organization uid
	...		- Fetch User 2 Organization with User 1
	Create Session For Organization    ${USER2_HEADER}    ${API_endpoint}
	${org_details}=	     Create Organization     Dgraph    200
	log 	${org_details}
	${details}=    Collections.Get From Dictionary    ${org_details}    data
    ${organization}=    Collections.Get From Dictionary    ${details}    createOrganization
    ${organization_uid}=    Collections.Get From Dictionary    ${organization}    uid
	Create Session For Organization      ${HEADERS}     ${API_endpoint}
	Get Members From Organization	  ${organization_uid}	 ${response}

Only Owner Fetch the Deployment
	[Documentation]		
    ...     List of Test Covered
	...
	...		- Get Deployment with Deployment ID
	Get Deployment    ${Session_alias}	${URL}	  ${USER2_HEADER}    ${deployment_id}	 Unauthorized

Only Owner Update the Organization for Deployment
	[Documentation]		
	...		List of Test Covered
	...
	...		- Create Deployment 
	...		- Get Deployment Name and Deployment uid
	...		- Update Deployment with User 1
	...		- Update Deployment with User 2
	${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${BACKEND_NAME}    ${BACKEND_ZONE}
    Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}
	${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
    ${deployment_name}=    Collections.Get From Dictionary    ${data}    name
	Update Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${deployment_id}    ${deployment_name}		 organizationId=${org_uid}		
	Update Deployment    ${Session_alias}    ${URL}    ${USER2_HEADER}    ${deployment_id}    ${deployment_name}     organizationId=${org_uid}		expected_response_text=Unauthorized
	Delete Deployment	   ${Session_alias}		${URL}		${HEADERS}		${deployment_id}

*** Keywords ***
Create Backend
        ${data}=    Create Deployment    ${Session_alias}    ${URL}    ${HEADERS}    ${BACKEND_NAME}    ${BACKEND_ZONE}
        Validate Created Deployment    ${data}    ${BACKEND_NAME}    ${BACKEND_ZONE}
        ${endpoint}=    Collections.Get From Dictionary    ${data}    url
        ${deployment_endpoint}=    Catenate    SEPARATOR=    https://    ${endpoint}
        Get Deployment Health    ${Session_alias}    ${deployment_endpoint}    ${HEADERS}
        ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
        Set Suite Variable    ${deployment_id}
        Set Suite Variable    ${deployment_endpoint}
        ${deployment_id}=    Collections.Get From Dictionary    ${data}    uid
        ${deployemnt_jwt_token}=    Collections.Get From Dictionary    ${data}    jwtToken
        Set Suite Variable    ${deployemnt_jwt_token}
        ${deployment_auth}=    Create Dictionary    x-auth-token=${deployemnt_jwt_token}    Content-Type=application/json
        Set Suite Variable    ${deployment_auth}

