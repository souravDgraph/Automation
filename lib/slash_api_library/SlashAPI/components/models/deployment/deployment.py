class DeploymentModels:
    update_schema = """
    {"query":"mutation updateGQLSchema($sch: String!) {updateGQLSchema(input: { set: { schema: $sch } }) {gqlSchema {schema generatedSchema}}}",
    "variables":{"sch":{{ '"' + properties['schema'] + '"' }}}}
    """
    update_rules = """{"operationName":"UpdateRules",
        "variables":{"deploymentID":{{ '"' + properties['deploymentID'] + '"' }},"anonAccess":{{ '"' + properties['anonAccess'] + '"' }}},
        "query":"mutation UpdateRules($deploymentID: String!, $anonAccess: String!) {updateDeploymentAnonAccess(deploymentID: $deploymentID, anonAccess: $anonAccess)}"
    }"""

    get_rules = """{"query":"query GetExistingRules($deploymentID: ID!) { getDeploymentByID(deploymentID: $deploymentID) { uid    name   anonAccess } }", "variables":{"deploymentID":{{ '"' + properties['deploymentID'] + '"'}}}}"""

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
        "query":"query GetDeploymentById($id: ID!){ getDeploymentByID(deploymentID: $id) { uid  url  name  zone  subdomain jaegerEnabled size deploymentMode dgraphHA backupInterval backupBucketFormat aclEnabled isProtected deploymentType jaegerSize jaegerTrace} }",
        "variables":{"id":{{ '"' + properties['deployment_id'] + '"' }}}
        }"""

    read_rules_attributes = """{"rules":{"types": ["get{{ properties['type'] }}","query{{ properties['type'] }}","aggregate{{ properties['type'] }}"],"lambdas":[]}}"""

    write_rules_attributes = """{"rules":{"types": ["update{{ properties['type'] }}","add{{ properties['type'] }}","delete{{ properties['type'] }}"],"lambdas":[]}}"""

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
        ,"organizationId": {{'"' + properties['organizationId'] + '"' }}
        {% endif %}

        {% if properties['deploymentType'] and properties['deploymentType'] != "" %}
        ,"deploymentType": {{ '"' + properties['deploymentType'] + '"' }}
        {% endif %}

        {% if properties['alphaStorage'] and properties['alphaStorage'] != "" %}
        ,"alphaStorage": {{ '"' + properties['alphaStorage'] + '"' }}
        {% endif %}

    }"""

    create_deployment = """
    {
    "query":"mutation CreateDeployment($input: NewDeployment!) {createDeployment(input: $input) {enterprise size uid url name zone deploymentType alphaStorage subdomain charts{compact full} jwtToken organization {uid name createdBy {accountType}} owner deletedAt frontendUrl frontendRepo deploymentMode lambdaScript dgraphHA jaegerEnabled jaegerSize jaegerTrace aclEnabled}}",
    "variables":{
        "input":{
            {% if properties['name'] and properties['name'] != "" %}
            "name": {{ '"' + properties['name'] + '"' }}
            {% endif %}
            {% if properties['deploymentType'] and properties['deploymentType'] != "" %}
            ,"deploymentType": {{ '"' + properties['deploymentType'] + '"' }}
            {% endif %}
            {% if properties['alphaStorage'] and properties['alphaStorage'] != "" %}
            ,"alphaStorage": {{ '"' + properties['alphaStorage'] + '"' }}
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

            {% if properties['aclEnabled'] and properties['aclEnabled'] != "" %}
            ,"aclEnabled": {{ '"' + properties['aclEnabled'] + '"' }}
            {% endif %}

            {% if properties['jaegerEnabled'] and properties['jaegerEnabled'] != "" %}
            ,"jaegerEnabled": {{ '"' + properties['jaegerEnabled'] + '"' }}
            {% endif %}

            {% if properties['jaegerSize'] and properties['jaegerSize'] != "" %}
            ,"jaegerSize": {{ '"' + properties['jaegerSize'] + '"' }}
            {% endif %}

            {% if properties['jaegerTrace'] and properties['jaegerTrace'] != "" %}
            ,"jaegerTrace": {{ '"' + properties['jaegerTrace'] + '"' }}
            {% endif %}

            }
            }
    }
    """

    update_deployment = """
    {"query": "mutation UpdateDeployment($input: UpdateDeploymentInput!) {updateDeployment(input: $input)}",
     "variables": {"input": {
        "uid": {{ '"' + properties['uid'] + '"' }}
        {% if properties['name'] and properties['name'] != "" %}
        ,"name": {{ '"' + properties['name'] + '"' }}
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

        {% if properties['organizationUID'] and properties['organizationUID'] == "empty" %}
        ,"organizationUID": null
        {% elif properties['organizationUID'] and properties['organizationUID'] != "" %}
        ,"organizationUID": {{'"' + properties['organizationUID'] + '"' }}
        {% endif %}

        {% if properties['jaegerEnabled'] and properties['jaegerEnabled'] != "" %}
        ,"jaegerEnabled": {{ '"' + properties['jaegerEnabled'] + '"' }}
        {% endif %}

        {% if properties['jaegerSize'] and properties['jaegerSize'] != "" %}
        ,"jaegerSize": {{ '"' + properties['jaegerSize'] + '"' }}
        {% endif %}

        {% if properties['jaegerTrace'] and properties['jaegerTrace'] != "" %}
        ,"jaegerTrace": {{ '"' + properties['jaegerTrace'] + '"' }}
        {% endif %}

        {% if properties['storage'] and properties['storage'] != "" %}
        ,"storage": {{ '"' + properties['storage'] + '"' }}
        {% endif %}

        {% if properties['backupInterval'] and properties['backupInterval'] != "" %}
        ,"backupInterval": {{ '"' + properties['backupInterval'] + '"' }}
        {% endif %}

        {% if properties['backupBucketFormat'] and properties['backupBucketFormat'] != "" %}
        ,"backupBucketFormat": {{ '"' + properties['backupBucketFormat'] + '"' }}
        {% endif %}

        {% if properties['aclEnabled'] and properties['aclEnabled'] != "" %}
        ,"aclEnabled": {{ '"' + properties['aclEnabled'] + '"' }}
        {% endif %}

        {% if properties['deploymentType'] and properties['deploymentType'] != "" %}
        ,"deploymentType": {{ '"' + properties['deploymentType'] + '"' }}  
        {% endif %}
        }

     }}
    """

    protect_deployment = """
       {"query": "mutation UpdateDeploymentProtection($input: UpdateDeploymentProtectionInput!){updateDeploymentProtection(input:$input){uid isProtected}}",
       "variables": {"input": {
        "uid": {{ '"' + properties['uid'] + '"' }},
        "protect": ""
        }}}
    """
    delete_deployment = """
           {"query":"mutation DeleteDeployment($deploymentID: String!) {deleteDeployment(deploymentID: $deploymentID)}",
           "variables":{"deploymentID":{{ '"' + properties['deploymentID'] + '"' }}}}
        """
