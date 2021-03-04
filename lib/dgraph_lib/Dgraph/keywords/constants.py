LOGIN_BODY = """mutation {
    login(userId: "groot", password: "password") {
        response {
        accessJWT
        refreshJWT
        }
    }
}"""
COMMON_HEADER = {'Content-Type': 'application/json'}
BACKUP_QUERY = """mutation BackupReq ($path: String!) {
  backup(input: {destination: $path}) {
    response {
      message
      code
    }
  }
}"""
RESTORE_QUERY = """mutation RestoreReq($path: String!, $enc_file: String){
  restore(input: {location: $path, encryptionKeyFile: $enc_file}){
    message
    code 
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

EXPORT_NFS_QUERY = """mutation RestoreReq($data_format: String!, $destination: String){
  export(input: {format: $data_format, destination: $destination}) {
    response {
      message
      code
    }
  }
}"""


