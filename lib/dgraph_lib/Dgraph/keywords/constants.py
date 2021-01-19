LOGIN_BODY = """mutation {
    login(userId: "groot", password: "password") {
        response {
        accessJWT
        refreshJWT
        }
    }
}"""
COMMON_HEADER = {'Content-Type': 'application/json'}
BACKUP_QUERY = """mutation {
  backup(input: {destination: $path}) {
    response {
      message
      code
    }
  }
}"""
RESTORE_QUERY = """mutation{
  restore(input: {location: $path}){
    message
    code 
    restoreId
  }
}"""
EXPORT_QUERY = """mutation {
  export(input: {format: $data_format}) {
    response {
      message
      code
    }
  }
}"""


