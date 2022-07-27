import json
import os
import library.utils as utils
import library.migrationlogger as nrlogger
import library.clients.gql as nerdgraph

logger = nrlogger.get_logger(os.path.basename(__file__))


class AiClient:

    def __init__(self):
        pass


    @staticmethod
    def query(func, user_api_key, account_id, region):
        payload = func(account_id)
        logger.debug(json.dumps(payload))
        return nerdgraph.GraphQl.post(user_api_key, payload, region)


    @staticmethod
    def aiDecisions(account_id):
        query = '''query($accountId: Int!) {
                    actor {
                        account(id: $accountId) {
                            aiDecisions {
                                decisions {
                                    count
                                    decisions {
                                        annotations {
                                            key
                                            value
                                        }
                                        correlationWindowLength
                                        createdAt
                                        creator {
                                            email
                                            gravatar
                                            name
                                            id
                                        }
                                        decisionExpression
                                        decisionType
                                        description
                                        id
                                        metadata {
                                            mergeOpinionCount {
                                                count
                                                opinion
                                            }
                                        }
                                        minCorrelationThreshold
                                        name
                                        overrideConfiguration {
                                            description
                                            priority
                                            title
                                        }
                                        source
                                        state
                                        updatedAt
                                    }
                                    nextCursor
                                }
                            }
                        }
                    }
                }'''
        variables = {'accountId': account_id}
        return {'query': query, 'variables': variables}


    @staticmethod
    def aiIssues(account_id):
        query = '''query($accountId: Int!) {
                    actor {
                        account(id: $accountId) {
                            aiIssues {
                                configByEnvironment {
                                    config {
                                        flappingInterval
                                        gracePeriod {
                                            period
                                            priority
                                        }
                                        inactivePeriod
                                        incidentTimeout
                                        issueTtl
                                        maxIssueSize
                                    }
                                }
                            }
                        }
                    }
                }'''
        variables = {'accountId': account_id}
        return {'query': query, 'variables': variables}
