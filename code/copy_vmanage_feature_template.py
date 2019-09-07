#!/usr/bin/env python

import argparse
import configparser
import json
import os
from code import utility


def get_feature_templates(session):
    url = '/dataservice/template/feature'

    try:
        response = session.rest_api_call('GET', url)
    except:
        raise RuntimeError('Error in getting feature templates')
    else:
        if response and 'data' in response and len(response['data']) > 0:
            feature_template_list = response['data']
            return {template_entry['templateName']: template_entry for template_entry in feature_template_list}
        else:
            return {}


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


def main(name):
    template_name = name.template

    if not template_name:
        raise RuntimeError('Template name not provided')

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
        src_templates = get_feature_templates(src_sess)
        if not src_templates:
            raise RuntimeError(f'No feature templates found in source vManage {src_host}')

        if template_name not in src_templates:
            raise RuntimeError(f'No feature template found with template name {template_name} in source vManage'
                               f' {src_host}')

        dest_templates = get_feature_templates(dest_sess)
        if template_name in dest_templates:
            raise RuntimeError(f'Feature template with template name {template_name} already exists in destination'
                               f' vManage {dest_host}')

        try:
            config_template = src_templates[template_name]
            resp = create_feature_template(dest_sess, config_template)
        except:
            raise
        else:
            if not resp:
                raise RuntimeError(f'Feature template creation with template name {template_name} failed in destination'
                                   f' vManage {dest_host}')
            else:
                print(f'Feature template {template_name} copied successfully from source vManage {src_host} to'
                      f' destination vManage {dest_host}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-template', '--template', help='vManage feature template name', type=str)
    temp_args = parser.parse_args()
    main(temp_args)
