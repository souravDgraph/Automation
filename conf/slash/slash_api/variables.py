URL = "https://api.stage.thegaas.com/"
BACKEND_NAME = "Test"
BACKEND_ZONE = "stgdgraph"
HEADERS = { "Authorization" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1ETXlNemcyTnpFME1qTkNORUUzTWpZME1UVTJNa0pCTVRjMFFUUkVPVEJFT0VZNE5UWXhSUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kZ3JhcGgtc2Fhcy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDA5ODU2MDI0NDA2Njk3NTI1ODIiLCJhdWQiOlsiaHR0cDovL2xvY2FsaG9zdDo4MDcwIiwiaHR0cHM6Ly9kZXYtZGdyYXBoLXNhYXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYxNDA5NjYzMCwiZXhwIjoxNjE0MTgzMDMwLCJhenAiOiJnYnBWcTdpMWdNdmdtdEkzbXVBem9aSEpiVTJieDVqdCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.ODyyqEnw266ojYkHlT6L68opcVTbKO1QBpFhAaPPctKvs51wqh71L78hvXL0rbUmOqEXmFHm43gIms2n2WfQYPpjbs_2cFX7eeGlA9xRSyNUn9sD-l0whc-awidinN5jFrAgsK-ciTLcyHVMASESkLLobz6_WfGxVFT3c6gHjolwU-GEscBIF3bEPJFfS0ZIn4kN1IttfucMu7NFWBHkSpI-0EWGiPW7Ekh_I0AjCNfrOqog4Ug3db9HlbzNqXyvibVUClvvPgu_6kfxIrJ6O091NRzf2SzOg_N66hzzY_EK5Xi_mxMJlttGB27yLg4FAJhPscc0KHTkeMSd6R3ZmQ",
            "Content-Type" : "application/json" }
DELETE_API_KEY_MESSAGE = "API Key Deleted Successfully."
SCHEMA = "type Task { id: ID! title: String! @search(by: [fulltext]) completed: Boolean! @search  user: User! }type User { username: String! @id @search(by: [hash]) name: String @search(by: [exact]) tasks: [Task] @hasInverse(field: user) }"
MUTATION_QUERY_1 = """{\"query\":\"mutation AddTasks {\\n addTask(input: [\\n {title: \\\"Create a database\\\", completed: false, user: {username: \\\"your-email@example.com\\\"}}]) {\\n numUids\\n task {\\n title\\n user {\\n username\\n }\\n  }\\n  }\\n}\"}"""
QUERY = """{\"query\":\"query {\\n \ __schema {\\n \ \ \ __typename\\n \ }\\n}\"}"""
INTROSPECTION_QUERY = """{"query":"query {__schema { __typename }}"}"""
NO_SCHEMA_ERROR = "Not resolving __schema. There's no GraphQL schema in Dgraph.  Use the /admin API to add a GraphQL schema"