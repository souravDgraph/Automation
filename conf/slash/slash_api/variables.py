URL = "https://api.stage.thegaas.com/"
BACKEND_NAME = "Test"
BACKEND_ZONE = "us-east-1"
USER_NAME = "vivetha+test25@dgraph.io"
PASSWORD = "Password@123"
HEADERS = { "Content-Type" : "application/json" }
USER2_HEADER = { "Authorization" : "earer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjgwNzAiLCJleHAiOjE2MTcyMDk3MTAsImlzcyI6Imh0dHBzOi8vZGV2LWRncmFwaC1zYWFzLmF1dGgwLmNvbS8iLCJzdWIiOiIweDI3NmZhIn0.zFbUhkQ6NS2QW3UEoKpm3HFk2VXgUrPvd1DQNUG18is",
"Content-Type" : "application/json" }
DELETE_API_KEY_MESSAGE = "API Key Deleted Successfully."
SCHEMA = "type Task { id: ID! title: String! @search(by: [fulltext]) completed: Boolean! @search  user: User! }type User { username: String! @id @search(by: [hash]) name: String @search(by: [exact]) tasks: [Task] @hasInverse(field: user) }"
MUTATION_QUERY_1 = """{\"query\":\"mutation AddTasks {\\n addTask(input: [\\n {title: \\\"Create a database\\\", completed: false, user: {username: \\\"your-email@example.com\\\"}}]) {\\n numUids\\n task {\\n title\\n user {\\n username\\n }\\n  }\\n  }\\n}\"}"""
QUERY = """{\"query\":\"query {\\n \ __schema {\\n \ \ \ __typename\\n \ }\\n}\"}"""
INTROSPECTION_QUERY = """{"query":"query {__schema { __typename }}"}"""
NO_SCHEMA_ERROR = "Not resolving __schema. There's no GraphQL schema in Dgraph.  Use the /admin API to add a GraphQL schema"
PROTECT_MODE_ERROR = "Deployment is protected from any changes."