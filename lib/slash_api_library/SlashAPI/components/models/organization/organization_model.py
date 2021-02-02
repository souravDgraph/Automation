CREATE_ORGANIZATION = """
                        mutation CreateOrganization($name: String!) {  
                            createOrganization(input: {name: $name}) {    
                                name
                                uid
                                __typename  
                            }
                        }
                         """


def create_organization(name):
    variables = {"name": name}
    query = {
        "query": CREATE_ORGANIZATION,
        "variables": variables
    }
    return query


GET_ORGANIZATIONS = """
                    query GetOrganizations {
                      organizations {
                        uid
                        name
                        __typename  
                      }
                    }
                        
                    """

GET_MEMBERS_IN_ORGANIZATIONS = """
                    query GetOrganizations {
                      organizations {
                        uid
                        name
                        members {
                            uid
                            auth0User {
                                name
                                email
                                id
                            }
                        } 
                      }
                    }
                    """


def get_organization():
    """
    Method to create a get query for organizations
    :return:
    """
    variables = {}
    query = {
        "query": GET_ORGANIZATIONS,
        "variables": variables
    }
    return query


def get_members_in_organization():
    """
    Method to create a get query for organizations
    :return:
    """
    variables = {}
    query = {
        "query": GET_MEMBERS_IN_ORGANIZATIONS,
        "variables": variables
    }
    return query


ADD_ORG_MEMBER = """
  mutation AddOrganizationMember($member: AddOrgMember!) 
  {  addOrganizationMember(input: $member) {   
        uid
        name
        members {
            uid
            auth0User {
                name
                email
                id
                __typename
            }
            __typename
        }
        createdBy {
            auth0User {
                name
                email
                id
                __typename
            }
        __typename
        }
    __typename
    }
    }
"""


def add_member_to_organization(email, org_uid):
    member = {
        "email": email,
        "organizationUID": org_uid,
    }

    variables = {
        "member": member
    }

    query = {
        "query": ADD_ORG_MEMBER,
        "variables": variables
    }
    return query


DEL_ORGANIZATION = """
mutation DeleteOrganizationMember($member: DeleteOrgMember!){
  deleteOrganizationMember(input: $member) {
    uid 
    name
    members {
        uid 
        auth0User {
            name
            email
            id
            __typename
        }
        __typename
    }
    createdBy {
        auth0User {
            name
            email
            id
            __typename
            }
        __typename
    }
    __typename
}
}
"""


def del_member_from_organization(mem_uid, org_uid):
    member = {
        "memberUID": mem_uid,
        "organizationUID": org_uid,
    }

    variables = {
        "member": member
    }

    query = {
        "query": DEL_ORGANIZATION,
        "variables": variables
    }
    return query


