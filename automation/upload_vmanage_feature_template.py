#!/usr/bin/env python

import argparse
import configparser
import json
import os
from automation import logger, utility


log = logger.Log(__name__)


def create_feature_template(session, template_file, template_type):
    with open(template_file, 'r') as config_file:
        content = json.load(config_file)

    if not content:
        raise RuntimeError(f'Template file {template_file} is empty')

    url = '/dataservice/template/feature'

    headers = {
        'content-type': 'application/json'
    }

    payload = {
        'templateName': os.path.basename(template_file),
        'templateDescription': 'Feature template',
        'templateType': template_type,
        'templateMinVersion': '15.0.0',
        'transitionInProgress': True,
        'viewMode': 'add',
        'deviceType': [
            'vedge-ISR-4451-X'
        ],
        'deviceModels': [
            {
                'name': 'vedge-ISR-4451-X',
                'displayName': 'ISR4451-X',
                'deviceType': 'vedge',
                'isCliSupported': False,
                'isCiscoDeviceModel': True
            }
        ],
        'templateUrl': '/app/configuration/template/feature/templates/vpn-vedge-15.0.0.html',
        'view': {
            'name': 'add'
        },
        'removeTableRow': {},
        'templateDefinition': content,
        'factoryDefault': False
    }

    try:
        response = session.rest_api_call('POST', url, headers, payload)
    except:
        raise RuntimeError('Error in creating feature template')
    else:
        if response and 'templateId' in response:
            return payload['templateName']
        else:
            return None


@log.log_this
def main(args):
    try:
        if not os.path.exists(args.template) or not os.path.isfile(args.template):
            raise RuntimeError()
    except:
        raise RuntimeError(f'Template file {args.template} doesn\'t exist')
    else:
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
            name = create_feature_template(sess, args.template, args.type)
            if not name:
                raise RuntimeError(f'Failed to upload template {name} in vManage')
            else:
                print(f'Feature template {name} uploaded successfully on {host}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-template', '--template', help='vManage feature template file with full path', type=str)
    parser.add_argument('-type', '--type', help='vManage feature template type', type=str)
    args = parser.parse_args()
    main(args)
