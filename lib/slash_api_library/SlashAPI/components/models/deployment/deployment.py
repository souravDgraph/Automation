class DeploymentModels:
    update_schema = """
    {"query":"mutation updateGQLSchema($sch: String!) {updateGQLSchema(input: { set: { schema: $sch } }) {gqlSchema {schema generatedSchema}}}",
    "variables":{"sch":{{ '"' + properties['schema'] + '"' }}}}
    """
    get_schema = """{"query":"{getGQLSchema {schema generatedSchema }}"}"""

    drop_data = """{"query":"mutation { dropData(allData: true) { response { code message } } }"}"""

    drop_schema_and_data = """{"query":"mutation { dropData(allDataAndSchema: true) { response { code message } } }"}"""

    list_backup = """{"query": "{ listBackups{ response { type backupNum folder timestamp }, errors { message } } }" }"""

    create_backup = """{
        "query": "mutation { backup { response { code message }, location } }",
        "variables": {}
    }"""

    delete_api_key = """
    {
    "variables":
        {
           {% if properties['deploymentID'] and properties['deploymentID'] != "" %}
            "deploymentID": {{ '"' + properties['deploymentID'] + '"' }}
            {% endif %}
            
            {% if properties['apiKeyID'] and properties['apiKeyID'] != "" %}
            ,"apiKeyID": {{ '"' + properties['apiKeyID'] + '"' }}
            {% endif %}
        },
     "query":"mutation DeleteAPIKey($deploymentID: String!, $apiKeyID: ID!){deleteAPIKey(deploymentID: $deploymentID, apiKeyID: $apiKeyID)}"
    }
    """

    create_api_key = """
    {
    "variables":
        {
           {% if properties['deploymentID'] and properties['deploymentID'] != "" %}
            "deploymentID": {{ '"' + properties['deploymentID'] + '"' }}
            {% endif %}
            
            {% if properties['name'] and properties['name'] != "" %}
            ,"name": {{ '"' + properties['name'] + '"' }}
            {% endif %}
            
            {% if properties['role'] and properties['role'] != "" %}
            ,"role": {{ '"' + properties['role'] + '"' }}
            {% endif %}
        },
    "query":"mutation CreateAPIKey($deploymentID: String!, $name: String!, $role: String) {createAPIKey(deploymentID: $deploymentID, name: $name, role: $role) {uid name role key deployment{uid apiKeys {uid name role key __typename} __typename} __typename}}"}
    """

    get_api_key = """
    {
    "variables":
        {
           {% if properties['deploymentID'] and properties['deploymentID'] != "" %}
            "deploymentID": {{ '"' + properties['deploymentID'] + '"' }}
            {% endif %}
        },
     "query":"query GetAPIKeys($deploymentID: ID!){getDeploymentByID(deploymentID: $deploymentID){uid name apiKeys {uid name role key __typename} __typename}}"
    }
    """

    freeze_deployment = """{
    "query": "mutation { freeze(deepFreeze: {{properties['deep_freeze']}}, backup: {{properties['backup']}}) }"
    }"""

    get_deployment = """{
        "query":"query GetDeploymentById($id: ID!){ getDeploymentByID(deploymentID: $id) { uid  url  name  zone  subdomain } }",
        "variables":{"id":{{ '"' + properties['deployment_id'] + '"' }}}
        }"""

    deployment_attributes = """
    {
        {% if properties['name'] and properties['name'] != "" %}
        "name": {{ '"' + properties['name'] + '"' }}
        {% endif %}
    
        {% if properties['zone'] and properties['zone'] != "" %}
        ,"zone": {{ '"' + properties['zone'] + '"' }}
        {% endif %}
    
        {% if properties['subdomain'] and properties['subdomain'] != "" %}
        ,"subdomain": {{ '"' + properties['subdomain'] + '"' }}
        {% endif %}
    
        {% if properties['organization'] and properties['organization'] != "" %}
        ,"organization": {{ '"' + properties['organization'] + '"' }}
        {% endif %}
    
        {% if properties['deploymentMode'] and properties['deploymentMode'] != "" %}
        ,"deploymentMode": {{ '"' + properties['deploymentMode'] + '"' }}
        {% endif %}
    
        {% if properties['dgraphHA'] and properties['dgraphHA'] != "" %}
        ,"dgraphHA": {{ '"' + properties['dgraphHA'] + '"' }}
        {% endif %}
    
        {% if properties['size'] and properties['size'] != "" %}
        ,"size": {{ '"' + properties['size'] + '"' }}
        {% endif %}
    
        {% if properties['organizationId'] and properties['organizationId'] == "empty" %}
        "organizationId": null
        {% elif properties['organizationId'] and properties['organizationId'] != "" %}
        "organizationId": {{'"' + properties['organizationId'] + '"' }}
        {% endif %}
        
        {% if properties['enterprise'] and properties['enterprise'] != "" %}
        ,"enterprise": {{ '"' + properties['enterprise'] + '"' }}
        {% endif %}
        
         {% if properties['storage'] and properties['storage'] != "" %}
        ,"storage": {{ '"' + properties['storage'] + '"' }}
        {% endif %}
    
    }"""

    create_deployment = """
    {
    "query":"mutation CreateDeployment($input: NewDeployment!) {createDeployment(input: $input) {enterprise size uid url name zone subdomain charts{compact full} jwtToken organization {uid name createdBy {accountType}} owner deletedAt frontendUrl frontendRepo deploymentMode lambdaScript dgraphHA}}",
    "variables":{
        "input":{
             {% if properties['name'] and properties['name'] != "" %}
            "name": {{ '"' + properties['name'] + '"' }}
            {% endif %}
            
            {% if properties['zone'] and properties['zone'] != "" %}
            ,"zone": {{ '"' + properties['zone'] + '"' }}
            {% endif %}
            
            {% if properties['subdomain'] and properties['subdomain'] != "" %}
            ,"subdomain": {{ '"' + properties['subdomain'] + '"' }}
            {% endif %}
            
            {% if properties['enterprise'] and properties['enterprise'] != "" %}
            ,"enterprise": {{ '"' + properties['enterprise'] + '"' }}
            {% endif %}
            
            {% if properties['size'] and properties['size'] != "" %}
            ,"size": {{ '"' + properties['size'] + '"' }}
            {% endif %}
            
            {% if properties['dgraphHA'] and properties['dgraphHA'] != "" %}
            ,"dgraphHA": {{ '"' + properties['dgraphHA'] + '"' }}
            {% endif %}
            }
            }
    }
    """
