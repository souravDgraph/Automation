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

    freeze_deployment = """{
    "query": "mutation { freeze(deepFreeze: {{properties['deep_freeze']}}, backup: {{properties['backup']}}) }"
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
    
        {% if properties['doNotFreeze'] and properties['doNotFreeze'] != "" %}
        ,"doNotFreeze": {{ '"' + properties['doNotFreeze'] + '"' }}
        {% endif %}
    
        {% if properties['dgraphHA'] and properties['dgraphHA'] != "" %}
        ,"dgraphHA": {{ '"' + properties['dgraphHA'] + '"' }}
        {% endif %}
    
        {% if properties['backupInterval'] and properties['backupInterval'] != "" %}
        ,"backupInterval": {{ '"' + properties['backupInterval'] + '"' }}
        {% endif %}
    
        {% if properties['backupBucketFormat'] and properties['backupBucketFormat'] != "" %}
        ,"backupBucketFormat": {{ '"' + properties['backupBucketFormat'] + '"' }}
        {% endif %}
    
        {% if properties['isProtected'] and properties['isProtected'] != "" %}
        ,"isProtected": {{ '"' + properties['isProtected'] + '"' }}
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
    
    }"""