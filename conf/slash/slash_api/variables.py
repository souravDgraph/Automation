URL = "https://api.stage.thegaas.com/"
BACKEND_NAME = "Test"
BACKEND_ZONE = "stgdgraph"
HEADERS = { "Authorization" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1ETXlNemcyTnpFME1qTkNORUUzTWpZME1UVTJNa0pCTVRjMFFUUkVPVEJFT0VZNE5UWXhSUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kZ3JhcGgtc2Fhcy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDA5ODU2MDI0NDA2Njk3NTI1ODIiLCJhdWQiOlsiaHR0cDovL2xvY2FsaG9zdDo4MDcwIiwiaHR0cHM6Ly9kZXYtZGdyYXBoLXNhYXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYxNTg2NTU2MCwiZXhwIjoxNjE1OTUxOTYwLCJhenAiOiJnYnBWcTdpMWdNdmdtdEkzbXVBem9aSEpiVTJieDVqdCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.g8zWd0TibCO9Zymsg7d7FrlQnGLuhsq3mZJ2LnH0Wa-kNqVMiXkYY2Ymuskl4CjmBcPMgU_Pn4spMM25mFlXEhBVo50MyIn7DG5O4431SVqRD0wrUnWZBJngsGv7Aa6lbpsh4v6JIBPcMJ_HJTJrvtP7YwLaFmgKsl1bddIY4I9AGcxghzD_VUQdVvkFOXh6qxRLUnNFW_3j3D4TxWi-7EZcihUwjWDMlrp2bedhoENdN9v9IAlAB5uP_n1b1lSyemJDLL5bhUz30zeg4IiU0ldiHXbCDgRDz1JgIlqjXD5Y9Y5HjvK2zKjHiSUb-iX5TcaAkVxHBglEGbCZXKS-yQ",
            "Content-Type" : "application/json" }
USER2_HEADER = { "Authorization" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1ETXlNemcyTnpFME1qTkNORUUzTWpZME1UVTJNa0pCTVRjMFFUUkVPVEJFT0VZNE5UWXhSUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1kZ3JhcGgtc2Fhcy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyNTMzZmI3YzBkZmYwMDcwZDI5ZmY3IiwiYXVkIjpbImh0dHA6Ly9sb2NhbGhvc3Q6ODA3MCIsImh0dHBzOi8vZGV2LWRncmFwaC1zYWFzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTU1NDg1MDksImV4cCI6MTYxNTYzNDkwOSwiYXpwIjoiZ2JwVnE3aTFnTXZnbXRJM211QXpvWkhKYlUyYng1anQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIn0.ieOLxCa9N88rP9vtsLfKUlZyvY-NbK6WcnhlEEYqoo692LgmudiCo3pGQ7ysQ3jRitH0wh7-k8w3k8v1dJ9ZsZHH90-xfJYG1UwePqmUFKPpqtx_S8HwzD95iMrEeogWa9jcVhyXssy64d6d_wJJeV0qdXiTmJLUJu147TDAwEcp-t7pfLDY3E6vez81w6SJFkSz4TumTdkeBZIQyUv2S4eJPy2Laiv9KDSAMn45WbVMXHGgdDkeUQtB08jXWihKgWg2A327jDoU2niAmddR0cY0h2z1PCn12qHNklaHs-f4gUPqGTskPxiYOl7M32hDChIADs2EdaB8UA5fL8EmKQ",
            "Content-Type" : "application/json" }
DELETE_API_KEY_MESSAGE = "API Key Deleted Successfully."
SCHEMA = "type Task { id: ID! title: String! @search(by: [fulltext]) completed: Boolean! @search  user: User! }type User { username: String! @id @search(by: [hash]) name: String @search(by: [exact]) tasks: [Task] @hasInverse(field: user) }"
MUTATION_QUERY_1 = """{\"query\":\"mutation AddTasks {\\n addTask(input: [\\n {title: \\\"Create a database\\\", completed: false, user: {username: \\\"your-email@example.com\\\"}}]) {\\n numUids\\n task {\\n title\\n user {\\n username\\n }\\n  }\\n  }\\n}\"}"""
QUERY = """{\"query\":\"query {\\n \ __schema {\\n \ \ \ __typename\\n \ }\\n}\"}"""
INTROSPECTION_QUERY = """{"query":"query {__schema { __typename }}"}"""
NO_SCHEMA_ERROR = "Not resolving __schema. There's no GraphQL schema in Dgraph.  Use the /admin API to add a GraphQL schema"
PROTECT_MODE_ERROR = "Deployment is protected from any changes."
READ_RULES = """{\\"rules\\":{\\"types\\":[\\"getUser\\",\\"queryUser\\",\\"aggregateUser\\"],\\"lambdas\\":[]}}"""
WRITE_RULES = """{\\"rules\\":{\\"types\\":[\\"updateUser\\",\\"addUser\\",\\"deleteUser\\"],\\"lambdas\\":[]}}"""
MUTATION1 = """{\"query\":\"mutation MyMutation {\\n addUser(input: [\\n {firstName: \\\"user\\\", lastName: \\\"a\\\"}]) {\\n numUids\\n }\\n }\"}"""
