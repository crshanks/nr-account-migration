import json
import os
import library.utils as utils
import library.migrationlogger as nrlogger
import library.clients.gql as nerdgraph

logger = nrlogger.get_logger(os.path.basename(__file__))


class CloudClient:

    def __init__(self):
        pass


    @staticmethod
    def query(func, user_api_key, account_id, region):
        payload = func(account_id)
        logger.debug(json.dumps(payload))
        return nerdgraph.GraphQl.post(user_api_key, payload, region)


    @staticmethod
    def linkedAccounts(account_id):
        query = '''query($accountId: Int!) {
                    actor {
                        account(id: $accountId) {
                            cloud {
                                linkedAccounts {
                                    authLabel
                                    createdAt
                                    disabled
                                    externalId
                                    id
                                    metricCollectionMode
                                    name
                                    nrAccountId
                                    provider {
                                        createdAt
                                        icon
                                        id
                                        name
                                        services {
                                            createdAt
                                            icon
                                            id
                                            isEnabled
                                            name
                                            slug
                                            updatedAt
                                        }
                                        slug
                                        updatedAt
                                    }
                                    updatedAt
                                }
                            }
                        }
                    }
                }'''
        variables = {'accountId': account_id}
        return {'query': query, 'variables': variables}


    @staticmethod
    def providers(account_id):
        query = '''query($accountId: Int!) {
                    actor {
                        account(id: $accountId) {
                            cloud {
                                providers {
                                    createdAt
                                    icon
                                    id
                                    name
                                    slug
                                    updatedAt
                                    services {
                                        createdAt
                                        icon
                                        id
                                        isEnabled
                                        name
                                        slug
                                        updatedAt
                                    }
                                }
                            }
                        }
                    }
                }'''
        variables = {'accountId': account_id}
        return {'query': query, 'variables': variables}
