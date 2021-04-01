class AuthModels:
    login = """{
    "variables":{
    "email": {{ '"' + properties['email'] + '"' }},
    "password":{{ '"' + properties['password'] + '"' }}
    },
    "query":"query login($email: String!, $password: String!) { login(email: $email, password: $password) {token __typename}}"
    }"""
#"query":"query login($email: String!, $password: String!) { login(email: $email, password: $password) {user {uid auth0ID email accountType config {maxDeployments isSuperAdmin __typename} emailVerified __typename} token __typename}}"