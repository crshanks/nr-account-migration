import json
import os
import library.utils as utils
import library.migrationlogger as nrlogger
import library.clients.gql as nerdgraph

logger = nrlogger.get_logger(os.path.basename(__file__))


class EventsToMetricsClient:

    def __init__(self):
        pass


    @staticmethod
    def query(func, user_api_key, account_id, region):
        payload = func(account_id)
        logger.debug(json.dumps(payload))
        return nerdgraph.GraphQl.post(user_api_key, payload, region)


    @staticmethod
    def eventsToMetrics(account_id):
        query = '''query($accountId: Int!) {
                    actor {
                        account(id: $accountId) {
                            eventsToMetrics {
                                allRules {
                                    rules {
                                        accountId
                                        createdAt
                                        description
                                        enabled
                                        id
                                        name
                                        nrql
                                        updatedAt
                                    }
                                }
                            }
                        }
                    }
                }'''
        variables = {'accountId': account_id}
        return {'query': query, 'variables': variables}
