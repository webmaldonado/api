import unittest
import json
from authservices import *
from .request_common.functions import set_header

class test_add_external_user(unittest.TestCase):

    header = {}
    body = {
        "appId": "",
        "cultureName": "",
        "cwid": "",
        "email": "",
        "ip": "",
        "userName": "",
        "roles": [],
        "fields": []
    }
    client = app.test_client()
    url = '/AuthServices/add-external-user'

    def execute_request(self):
        return self.client.post(self.url, data = json.dumps(self.body), headers = self.header)

    def set_body_default(self):
        self.body['appId'] = 'f282375a9c5f4f849e2716d39bf1d627'
        self.body['cultureName'] = 'en-US'
        self.body['cwid'] = ''
        self.body['email'] = 'maldonado.py@gmail.com'
        self.body['ip'] = '172.30.28.28'
        self.body['userName'] = 'Ronald'
        self.body['roles'] = dict(
            {
                'name': 'dev-cp_iamauthservices_itaccess',
                'restriction_Codes': 'ab-xwy89-0201'
            }
        ),
        self.body['fields'] = []

    def test_method_add_external_user_invalid_system(self):
        self.header = set_header()
        self.set_body_default()
        self.body['appId'] = 'INVALID_APP_ID'
        resp = self.execute_request()
        if resp.status_code != 200 and resp.status_code != 400:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 3 - System not found or inactive!
        self.assertTrue(result.get('code') == 3, f'expected code: 3, returned: {result.get("code")}')

    def test_method_add_external_user_email_already_exists(self):
        self.header = set_header()
        self.set_body_default()
        self.body['email'] = 'gael@maldonado.com.br'
        resp = self.execute_request()
        if resp.status_code != 200 and resp.status_code != 400:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 50 - This email already are at using!
        self.assertTrue(result.get('code') == 50, f'expected code: 50, returned: {result.get("code")}')

    def test_method_add_external_user_invalid_role(self):
        self.header = set_header()
        self.set_body_default()
        self.body['roles'] = dict(
            {
                'name': 'INVALID_ROLE',
                'restriction_Codes': ''
            }
        ),
        resp = self.execute_request()
        if resp.status_code != 200 and resp.status_code != 400:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 5 - Roles not found!
        self.assertTrue(result.get('code') == 5, f'expected code: 5, returned: {result.get("code")}')

    def test_method_add_external_user_role_not_associate(self):
        self.header = set_header()
        self.set_body_default()
        self.body['roles'] = dict(
            {
                'name': 'DEV-CP_CAMBIO_CORRETORA',
                'restriction_Codes': ''
            }
        ),
        resp = self.execute_request()
        if resp.status_code != 200 and resp.status_code != 400:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 39 - Role is not associate the system!
        self.assertTrue(result.get('code') == 39, f'expected code: 39, returned: {result.get("code")}')

    def test_method_add_external_user_success(self):
        self.header = set_header()
        self.set_body_default()
        resp = self.execute_request()
        if resp.status_code != 200 and resp.status_code != 400:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 27 - Query was successful!
        self.assertTrue(result.get('code') == 27, f'expected code: 27, returned: {result.get("code")}')