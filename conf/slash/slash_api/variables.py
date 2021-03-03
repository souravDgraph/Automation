URL = "https://api.stage.thegaas.com/"
BACKEND_NAME = "Test"
BACKEND_ZONE = "stgdgraph"
HEADERS = { "Authorization" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1ETXlNemcyTnpFME1qTkNORUUzTWpZME1UVTJNa0pCTVRjMFFUUkVPVEJFT0VZNE5UWXhSUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kZ3JhcGgtc2Fhcy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDEyNDU5MjU2NzI2NjQzMDk0MTAiLCJhdWQiOlsiaHR0cDovL2xvY2FsaG9zdDo4MDcwIiwiaHR0cHM6Ly9kZXYtZGdyYXBoLXNhYXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYxNDc3MDYyMywiZXhwIjoxNjE0ODU3MDIzLCJhenAiOiJnYnBWcTdpMWdNdmdtdEkzbXVBem9aSEpiVTJieDVqdCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.RWGgpybLsIJQh9nqwiFw8hPErbDqjz4v1P4KS88CcWlVctxldNcagP0JSDBEBexojbtazbIKzrAhT6m4W0XPbX4VC3KalEdXhQur3dTI8mHy7V72K4o2nGQt6koKGH9xSI_5Vn_iJr1Vzfs_dae7E-QXgp0TK3R2gsRjPsLQEGYDhAEYKZL7z8sCYFCUi9GFtBGQCXCuHxZKwsLJjpniH9lXTCvsfJm7ZN-jxS09EMdL-w01Bk4z31f7wf9Kba9ZJLlNKqg5bakZ73y5FvSMNQouNpLIfLIUU5DNGujh91Zanyt6vty64-hamLCKNwtzl7h5qqegYmDQ8w-bZZ8CTQ",
            "Content-Type" : "application/json" }
DELETE_API_KEY_MESSAGE = "API Key Deleted Successfully."
SCHEMA = "type Task { id: ID! title: String! @search(by: [fulltext]) completed: Boolean! @search  user: User! }type User { username: String! @id @search(by: [hash]) name: String @search(by: [exact]) tasks: [Task] @hasInverse(field: user) }"
MUTATION_QUERY_1 = """{\"query\":\"mutation AddTasks {\\n addTask(input: [\\n {title: \\\"Create a database\\\", completed: false, user: {username: \\\"your-email@example.com\\\"}}]) {\\n numUids\\n task {\\n title\\n user {\\n username\\n }\\n  }\\n  }\\n}\"}"""
QUERY = """{\"query\":\"query {\\n \ __schema {\\n \ \ \ __typename\\n \ }\\n}\"}"""
INTROSPECTION_QUERY = """{"query":"query {__schema { __typename }}"}"""
NO_SCHEMA_ERROR = "Not resolving __schema. There's no GraphQL schema in Dgraph.  Use the /admin API to add a GraphQL schema"