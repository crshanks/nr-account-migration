import argparse
import os
import json
import library.migrationlogger as nrlogger
import library.clients.metricnormalizationclient as metricnormalizationclient
import library.localstore as store
import library.utils as utils

logger = nrlogger.get_logger(os.path.basename(__file__))
mnc = metricnormalizationclient.MetricNormalizationClient()


def configure_parser():
    parser = argparse.ArgumentParser(description='Fetch Log Configurations')
    parser.add_argument('--accounts', nargs=1, type=str, required=True, help='Path to file with account IDs')
    parser.add_argument('--userApiKey', nargs=1, type=str, required=True, help='User API Key')
    parser.add_argument('--region', type=str, nargs=1, required=False, help='sourceRegion us(default) or eu')
    parser.add_argument('--metricNormalizationRules', dest='metricNormalizationRules', required=False, action='store_true', help='Query metricNormalizationRules')
    return parser


def get_config(func, user_api_key, from_file, region):
    acct_ids = store.load_names(from_file)
    configs = []
    # Strip the class name
    field = func.__name__
    for acct_id in acct_ids:
        result = mnc.query(func, user_api_key, int(acct_id), region)
        logger.info(json.dumps(result))
        config = result['response']['data']['actor']['account']['metricNormalization'][field]
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
    if args.metricNormalizationRules:
        get_config(mnc.metricNormalizationRules, user_api_key, args.accounts[0], region)
    else:
        logger.info("pass --metricNormalizationRules to fetch metricNormalizationRules")


if __name__ == '__main__':
    main()