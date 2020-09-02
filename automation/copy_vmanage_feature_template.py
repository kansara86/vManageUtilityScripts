#!/usr/bin/env python

import argparse
import configparser
import json
import os
from automation import logger, utility


log = logger.Log(__name__)


def get_feature_template_list(session):
    url = '/dataservice/template/feature'

    try:
        response = session.rest_api_call('GET', url)
    except:
        raise RuntimeError('Error in getting feature template list')
    else:
        if response and 'data' in response:
            return response['data']
        else:
            return None


def create_feature_template(session, config_template_dict):
    url = '/dataservice/template/feature'

    headers = {
        'content-type': 'application/json'
    }

    payload = {
        'templateName': config_template_dict['templateName'],
        'templateDescription': config_template_dict['templateDescription'],
        'templateType': config_template_dict['templateType'],
        'templateMinVersion': config_template_dict['templateMinVersion'],
        'deviceType': config_template_dict['deviceType'],
        'templateDefinition': json.loads(config_template_dict['templateDefinition']),
        'factoryDefault': config_template_dict['factoryDefault']
    }

    try:
        response = session.rest_api_call('POST', url, headers, payload)
    except:
        raise RuntimeError('Error in creating feature template')
    else:
        if response and 'templateId' in response:
            return response['templateId']
        else:
            return None


@log.log_this
def main(args):
    try:
        config = configparser.ConfigParser()
        config_file = os.path.join(utility.get_root_dir(), 'config.ini')
        config.read(config_file)

        src_host = config['SRC_VMANAGE']['HOST']
        src_user = config['SRC_VMANAGE']['USER']
        src_passwd = config['SRC_VMANAGE']['PASSWD']

        dest_host = config['DEST_VMANAGE']['HOST']
        dest_user = config['DEST_VMANAGE']['USER']
        dest_passwd = config['DEST_VMANAGE']['PASSWD']

        src_sess = utility.VmanageHttpSession(src_host, src_user, src_passwd)
        dest_sess = utility.VmanageHttpSession(dest_host, dest_user, dest_passwd)
    except:
        return RuntimeError('Error in contacting vManage(s)')
    else:
        template_list = get_feature_template_list(src_sess)
        if not template_list:
            raise RuntimeError('No feature templates found in source vManage')

        config_template = {}
        try:
            found = False
            for template_entry in template_list:
                if template_entry['templateName'] == args.template:
                    config_template = template_entry
                    found = True
                    break
        except:
            raise RuntimeError('templateName key not found in feature template list')
        else:
            if not found:
                raise RuntimeError(f'No feature template found with the template name {args.template}')

            resp = create_feature_template(dest_sess, config_template)
            if not resp:
                raise RuntimeError('Template not created successfully in destination vManage')
            else:
                print(f'Feature template {args.template} copied successfully')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-template', '--template', help='vManage feature template name', type=str)
    args = parser.parse_args()
    main(args)
