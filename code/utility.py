#!/usr/bin/env python

import json
import os
import requests


class VmanageHttpSession:
    def __init__(self, host, username, password):
        # Default session parameters
        self.host_url = f'https://{host}'
        self.default_header = {'accept': 'application/json'}
        self.session = self.get_session(username, password)
        self.disable_cert_validation()

    def enable_cert_validation(self, cert_file):
        self.session.verify = True
        self.session.cert = cert_file

    def disable_cert_validation(self):
        self.session.verify = False
        self.session.cert = None

    def add_headers(self, headers):
        new_headers = {**self.default_header, **headers}
        self.session.headers.update(new_headers)

    def get_session(self, username, password):
        sess = requests.Session()

        url = self.host_url + '/j_security_check'
        headers = {'content-type': 'application/x-www-form-urlencoded', 'accept': 'application/json'}
        data = {'j_username': username, 'j_password': password}

        try:
            sess.post(url=url, headers=headers, data=data, verify=False)
        except:
            raise
        else:
            return sess

    def rest_api_call(self, method, url, headers={}, data=None, params=None, timeout=10):
        method = method.upper()

        if 'https' not in url:
            url = self.host_url + url

        self.add_headers(headers)
        if data:
            data = json.dumps(data)

        resp = None
        resp_json = None
        try:
            if method in ['GET', 'POST']:
                if method == 'GET':
                    resp = self.session.get(url, params=params, timeout=timeout)
                elif method == 'POST':
                    resp = self.session.post(url, data=data, params=params, timeout=timeout)

                if resp.status_code in [200, 201] and resp.content:
                    resp_json = resp.json()
                else:
                    raise RuntimeError('Invalid REST response')
        except:
            error_resp = dict()
            error_resp['method'] = method
            error_resp['url'] = url
            error_resp['response_code'] = resp.status_code
            error_resp['response_content'] = resp.content

            print('Exception in REST API call')
            print(error_resp)
            raise
        else:
            return resp_json


def get_root_dir():
    try:
        root_dir = os.path.dirname(os.path.dirname(__file__))
    except:
        raise RuntimeError('Failed to get the root directory')
    else:
        return root_dir


def convert_yaml_to_dict(yaml_file):
    try:
        with open(yaml_file) as f:
            data_dict = yaml.load(f)
    except:
        raise RuntimeError('Error converting {} file to dictionary'.format(yaml_file))

    return data_dict
