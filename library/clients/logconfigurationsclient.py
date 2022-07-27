import json
import os
import library.utils as utils
import library.migrationlogger as nrlogger
import library.clients.gql as nerdgraph

logger = nrlogger.get_logger(os.path.basename(__file__))


class LogConfigurationsClient:

    def __init__(self):
        pass


    @staticmethod
    def query(func, user_api_key, account_id, region):
        payload = func(account_id)
        logger.debug(json.dumps(payload))
        return nerdgraph.GraphQl.post(user_api_key, payload, region)


    @staticmethod
    def parsingRules(account_id):
        query = '''query($accountId: Int!) {
                    actor {
                        account(id: $accountId) {
                            logConfigurations {
                                parsingRules {
                                    accountId
                                    createdBy {
                                        id
                                        name
                                        email
                                        gravatar
                                    }
                                    description
                                    enabled
                                    grok
                                    id
                                    lucene
                                    nrql
                                    updatedAt
                                    updatedBy {
                                        name
                                        id
                                        gravatar
                                        email
                                    }
                                    deleted
                                }
                            }
                        }
                    }
                }'''
        variables = {'accountId': account_id}
        return {'query': query, 'variables': variables}


    @staticmethod
    def dataPartitionRules(account_id):
        query = '''query($accountId: Int!) {
                    actor {
                        account(id: $accountId) {
                            logConfigurations {
                                dataPartitionRules {
                                    createdAt
                                    createdBy {
                                        email
                                        gravatar
                                        id
                                        name
                                    }
                                    deleted
                                    description
                                    enabled
                                    id
                                    matchingCriteria {
                                        attributeName
                                        matchingOperator
                                        matchingExpression
                                    }
                                    retentionPolicy
                                    targetDataPartition
                                    updatedAt
                                    updatedBy {
                                        email
                                        gravatar
                                        id
                                        name
                                    }
                                }
                            }
                        }
                    }
                }'''
        variables = {'accountId': account_id}
        return {'query': query, 'variables': variables}


    @staticmethod
    def obfuscationRules(account_id):
        query = '''query($accountId: Int!) {
                    actor {
                        account(id: $accountId) {
                            logConfigurations {
                                obfuscationRules {
                                    actions {
                                        attributes
                                            expression {
                                                createdAt
                                                createdBy {
                                                    email
                                                    gravatar
                                                    id
                                                    name
                                                }
                                                description
                                                id
                                                name
                                                regex
                                                updatedAt
                                                updatedBy {
                                                    email
                                                    gravatar
                                                    id
                                                    name
                                                }
                                            }
                                        id
                                        method
                                    }
                                    createdAt
                                    createdBy {
                                        email
                                        gravatar
                                        id
                                        name
                                    }
                                    description
                                    enabled
                                    filter
                                    id
                                    name
                                    updatedAt
                                    updatedBy {
                                        email
                                        gravatar
                                        id
                                        name
                                    }
                                }
                            }
                        }
                    }
                }'''
        variables = {'accountId': account_id}
        return {'query': query, 'variables': variables}


    @staticmethod
    def obfuscationExpressions(account_id):
        query = '''query($accountId: Int!) {
                    actor {
                        account(id: $accountId) {
                            logConfigurations {
                                obfuscationExpressions {
                                    createdAt
                                    description
                                    id
                                    name
                                    regex
                                    updatedAt
                                    updatedBy {
                                        email
                                        gravatar
                                        name
                                        id
                                    }
                                    createdBy {
                                        email
                                        gravatar
                                        id
                                        name
                                    }
                                }
                            }
                        }
                    }
                }'''
        variables = {'accountId': account_id}
        return {'query': query, 'variables': variables}


    @staticmethod
    def pipelineConfiguration(account_id):
        query = '''query($accountId: Int!) {
                    actor {
                        account(id: $accountId) {
                            logConfigurations {
                                pipelineConfiguration {
                                    accountId
                                    enrichmentDisabled
                                    jsonParsingDisabled
                                    obfuscationDisabled
                                    parsingDisabled
                                    patternsEnabled
                                    recursiveJsonParsingDisabled
                                    transformationDisabled
                                    updatedAt
                                    updatedBy {
                                        email
                                        gravatar
                                        id
                                        name
                                    }
                                }
                            }
                        }
                    }
                }'''
        variables = {'accountId': account_id}
        return {'query': query, 'variables': variables}
