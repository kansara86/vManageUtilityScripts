#!/usr/bin/env python

import json
import os
import requests
import socket
import time
import yaml
from automation import logger


log = logger.Log(__name__)
root_dir = None


class VmanageHttpSession:
    @log.log_this
    def __init__(self, host, username, password):
        # Default session parameters
        self.host_url = f'https://{host}'
        self.default_header = {'accept': 'application/json'}
        self.session = self.get_session(username, password)
        self.disable_cert_validation()

    @log.log_this
    def enable_cert_validation(self, cert_file):
        self.session.verify = True
        self.session.cert = cert_file

    @log.log_this
    def disable_cert_validation(self):
        self.session.verify = False
        self.session.cert = None

    @log.log_this
    def add_headers(self, headers):
        new_headers = {**self.default_header, **headers}
        self.session.headers.update(new_headers)

    @log.log_this
    def get_session(self, username, password):
        sess = requests.Session()

        url = self.host_url + '/j_security_check'
        headers = {'content-type': 'application/x-www-form-urlencoded', 'accept': 'application/json'}
        data = {'j_username': username, 'j_password': password}

        try:
            sess.post(url=url, headers=headers, data=data, verify=False)
        except:
            raise RuntimeError()
        else:
            return sess

    @log.log_this
    def rest_api_call(self, method, url, headers={}, data=None, params=None, timeout=10):
        method = method.upper()

        if 'https' not in url:
            url = self.host_url + url

        self.add_headers(headers)
        if data:
            data = json.dumps(data)

        for count in range(7):
            resp = None
            try:
                if method in ['GET', 'POST', 'PUT', 'DELETE']:
                    if method == 'GET':
                        resp = self.session.get(url, params=params, timeout=timeout)
                    elif method == 'POST':
                        resp = self.session.post(url, data=data, params=params, timeout=timeout)
                    elif method == 'PUT':
                        resp = self.session.put(url, data=data, params=params, timeout=timeout)
                    elif method == 'DELETE':
                        resp = self.session.delete(url, data=data, params=params, timeout=timeout)

                    if resp.status_code in [200, 201]:
                        if not resp.content:
                            return resp
                        if method == 'GET' and '/dataservice/device/action/status/' in url:
                            if 'data' in resp.json() and len(resp.json()['data']) == 1 and 'status' in resp.json()['data'][0] and resp.json()['data'][0]['status'] != 'Done - Scheduled':
                                raise RuntimeError()
                            else:
                                return resp.json()
                        if 'id' in resp.json():
                            task_id = resp.json()['id']
                            task_url = f'/dataservice/device/action/status/{task_id}'
                            return self.rest_api_call('GET', task_url)
                        return resp.json()
                    elif resp.status_code in [500]:
                        if ('status' in resp.json() and isinstance(resp.json()['status'], bool) and
                                resp.json()['status'] is False and 'response' in resp.json() and
                                len(resp.json()['response']) == 0):
                            return resp.json()
                    elif resp.status_code in [202, 204, 206]:
                        if 'executionStatusUrl' in resp.json():
                            return self.rest_api_call('GET', resp.json()['executionStatusUrl'])
                        if 'response' in resp.json() and 'url' in resp.json()['response']:
                            return self.rest_api_call('GET', resp.json()['response']['url'])

                    if count == 6:
                        raise RuntimeError()
                else:
                    raise RuntimeError()
            except:
                time.sleep(count+1)
                continue

        raise RuntimeError(f'Exception in the REST API call - Method: {method} URL: {url}')


@log.log_this
def get_root_dir():
    global root_dir

    try:
        if not root_dir:
            root_dir = os.path.dirname(os.path.dirname(__file__))
    except:
        raise RuntimeError('Failed to get the root directory')

    return root_dir


@log.log_this
def convert_yaml_to_dict(yaml_file):
    try:
        with open(yaml_file) as f:
            data_dict = yaml.load(f)
    except:
        raise RuntimeError('Error converting {} file to dictionary'.format(yaml_file))

    return data_dict

