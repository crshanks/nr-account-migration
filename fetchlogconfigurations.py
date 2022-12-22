import argparse
import os
import json
import library.migrationlogger as nrlogger
import library.clients.logconfigurationsclient as logconfigurationsclient
import library.localstore as store
import library.utils as utils

logger = nrlogger.get_logger(os.path.basename(__file__))
lcc = logconfigurationsclient.LogConfigurationsClient()


def configure_parser():
    parser = argparse.ArgumentParser(description='Fetch Log Configurations')
    parser.add_argument('--accounts', nargs=1, type=str, required=True, help='Path to file with account IDs')
    parser.add_argument('--userApiKey', nargs=1, type=str, required=True, help='User API Key')
    parser.add_argument('--region', type=str, nargs=1, required=False, help='sourceRegion us(default) or eu')
    parser.add_argument('--parsingRules', dest='parsingRules', required=False, action='store_true', help='Query parsingRules')
    parser.add_argument('--dataPartitionRules', dest='dataPartitionRules', required=False, action='store_true', help='Query dataPartitionRules')
    parser.add_argument('--obfuscationRules', dest='obfuscationRules', required=False, action='store_true', help='Query obfuscationRules')
    parser.add_argument('--obfuscationExpressions', dest='obfuscationExpressions', required=False, action='store_true', help='Query obfuscationExpressions')
    parser.add_argument('--pipelineConfiguration', dest='pipelineConfiguration', required=False, action='store_true', help='Query pipelineConfiguration')
    return parser


def get_config(func, user_api_key, from_file, region):
    acct_ids = store.load_names(from_file)
    configs = []
    # Strip the class name
    field = func.__name__
    for acct_id in acct_ids:
        try:
            result = lcc.query(func, user_api_key, int(acct_id), region)
            logger.info(json.dumps(result))
            config = result['response']['data']['actor']['account']['logConfigurations'][field]
        except:
            logger.error(f'Error querying {field} for account {acct_id}')
        else:
            # config['accountId'] = acct_id
            configs.append(config)
    logger.info(configs)
    store.save_config_csv(field, configs)


def main():
    parser = configure_parser()
    args = parser.parse_args()
    user_api_key = utils.ensure_user_api_key(args)
    if not user_api_key:
        utils.error_and_exit('userApiKey', 'ENV_USER_API_KEY')
    region = utils.ensure_region(args)
    if args.parsingRules:
        get_config(lcc.parsingRules, user_api_key, args.accounts[0], region)
    elif args.dataPartitionRules:
        get_config(lcc.dataPartitionRules, user_api_key, args.accounts[0], region)
    elif args.obfuscationRules:
        get_config(lcc.obfuscationRules, user_api_key, args.accounts[0], region)
    elif args.obfuscationExpressions:
        get_config(lcc.obfuscationExpressions, user_api_key, args.accounts[0], region)
    elif args.pipelineConfiguration:
        get_config(lcc.pipelineConfiguration, user_api_key, args.accounts[0], region)
    else:
        logger.info("pass [--parsingRules | --dataPartitionRules | --obfuscationRules | --obfuscationExpressions | --pipelineConfiguration] to fetch configuration")


if __name__ == '__main__':
    main()