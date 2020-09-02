#!/usr/bin/env python

import argparse
import configparser
import json
import os
from automation import logger, utility


log = logger.Log(__name__)


def get_feature_templates(session):
    url = '/dataservice/template/feature'

    try:
        response = session.rest_api_call('GET', url)
    except:
        raise RuntimeError('Error in getting feature template list')
    else:
        if response and 'data' in response and len(response['data']) > 0:
            return {entry['templateName']: entry for entry in response['data']}
        else:
            return {}


@log.log_this
def main(args):
    try:
        config = configparser.ConfigParser()
        config_file = os.path.join(utility.get_root_dir(), 'config.ini')
        config.read(config_file)

        host = config['VMANAGE']['HOST']
        user = config['VMANAGE']['USER']
        passwd = config['VMANAGE']['PASSWD']

        sess = utility.VmanageHttpSession(host, user, passwd)
    except:
        return RuntimeError('Error in contacting vManage')
    else:
        feature_templates = get_feature_templates(sess)
        if not feature_templates:
            raise RuntimeError('No feature templates found in vManage')

        try:
            if args.template in feature_templates:
                temp_file_with_path = os.path.join(utility.get_root_dir(), args.template)
                with open(temp_file_with_path, 'w') as temp_file:
                    json.dump(json.loads(feature_templates[args.template]['templateDefinition']), temp_file, indent=2)
                    template_type = feature_templates[args.template]['templateType']
            else:
                raise RuntimeError(f'No feature template found with the template name {args.template}')
        except:
            raise RuntimeError('Error in retrieving template attributes')
        else:
            final_temp_file = f'{temp_file_with_path}({template_type})'
            os.rename(temp_file_with_path, final_temp_file)
            print(f'Feature template {args.template} downloaded successfully at {final_temp_file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-template', '--template', help='vManage feature template name', type=str)
    args = parser.parse_args()
    main(args)
