import unittest
import json
from authservices import *
from .request_common.functions import set_header

class test_loginsso(unittest.TestCase):

    header = {}
    body = {
        "appId": "",
        "culture": "",
        "ip": "",
        "login": ""
    }
    client = app.test_client()
    url = '/AuthServices/loginsso'

    def set_body_default(self):
        self.body['appId'] = 'f282375a9c5f4f849e2716d39bf1d627'
        self.body['login'] = 'ETVBO'
        self.body['ip'] = '172.30.28.28'
        self.body['culture'] = 'en-us'

    def execute_request(self):
        return self.client.post(self.url, data = json.dumps(self.body), headers = self.header)

    def test_method_loginsso_with_cwid_bayer(self):
        self.header = set_header()
        self.set_body_default()
        self.body['login'] = 'GDEVS'
        resp = self.execute_request()
        if resp.status_code != 200:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 1 - Your login attempt was successful!
        self.assertTrue(result.get('code') == 1, result.get('code'))

    def test_method_loginsso_with_email_bayer(self):
        self.header = set_header()
        self.set_body_default()
        self.body['login'] = 'ronald.maldonado.ext@bayer.com'
        resp = self.execute_request()
        if resp.status_code != 200:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 1 - Your login attempt was successful!
        self.assertTrue(result.get('code') == 1, result.get('code'))

    def test_method_loginsso_with_cwid_external(self):
        self.header = set_header()
        self.set_body_default()
        self.body['login'] = 'GAEL'
        resp = self.execute_request()
        if resp.status_code != 200:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 1 - Your login attempt was successful!
        self.assertTrue(result.get('code') == 1, result.get('code'))

    def test_method_loginsso_with_email_external(self):
        self.header = set_header()
        self.set_body_default()
        self.body['login'] = 'gael@maldonado.com.br'
        resp = self.execute_request()
        if resp.status_code != 200:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 1 - Your login attempt was successful!
        self.assertTrue(result.get('code') == 1, result.get('code'))

    def test_method_loginsso_with_email_gigya(self):
        self.header = set_header()
        self.set_body_default()
        self.body['login'] = 'gael@maldonado.com.br'
        resp = self.execute_request()
        if resp.status_code != 200:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 1 - Your login attempt was successful!
        self.assertTrue(result.get('code') == 1, result.get('code'))

    def test_method_loginsso_return_invalid_system(self):
        self.header = set_header()
        self.set_body_default()
        self.body['appId'] = 'INVALID_APP_ID'
        resp = self.execute_request()
        if resp.status_code != 200 and resp.status_code != 400:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 3 - System not found or inactive!
        self.assertTrue(result.get('code') == 3, result.get('code'))

    def test_method_loginsso_return_invalid_credentials(self):
        self.header = set_header()
        self.set_body_default()
        self.body['login'] = 'INVALID_LOGIN'
        resp = self.execute_request()
        if resp.status_code != 200 and resp.status_code != 401:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 2 - Invalid credentials (user/password) !
        self.assertTrue(result.get('code') == 2, result.get('code'))
