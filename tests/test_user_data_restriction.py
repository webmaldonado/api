import unittest
from authservices import *
from .request_common.functions import set_header

class test_user_data_restriction(unittest.TestCase):

    header = {}
    client = app.test_client()
    url = '/AuthServices/user-data-restriction'

    def test_method_user_data_restriction_with_cwid_bayer(self):
        app_id = 'f282375a9c5f4f849e2716d39bf1d627'
        login = 'ETVBO'
        ip = '172.30.28.28'
        self.header = set_header()
        url_with_parameters = f'{self.url}?appId={app_id}&login={login}&ip={ip}'
        resp = self.client.get(url_with_parameters, headers=self.header)
        if resp.status_code != 200 and resp.status_code != 401:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 27 - Query was successful!
        self.assertTrue(result.get('code') == 27, f'expected code: 27, returned: {result.get("code")}')

    def test_method_user_data_restriction_with_email_bayer(self):
        app_id = 'f282375a9c5f4f849e2716d39bf1d627'
        login = 'ronald.maldonado.ext@bayer.com'
        ip = '172.30.28.28'
        self.header = set_header()
        url_with_parameters = f'{self.url}?appId={app_id}&login={login}&ip={ip}'
        resp = self.client.get(url_with_parameters, headers=self.header)
        if resp.status_code != 200 and resp.status_code != 401:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 27 - Query was successful!
        self.assertTrue(result.get('code') == 27, f'expected code: 27, returned: {result.get("code")}')

    def test_method_user_data_restriction_with_cwid_external(self):
        app_id = 'f282375a9c5f4f849e2716d39bf1d627'
        login = 'GAEL'
        ip = '172.30.28.28'
        self.header = set_header()
        url_with_parameters = f'{self.url}?appId={app_id}&login={login}&ip={ip}'
        resp = self.client.get(url_with_parameters, headers=self.header)
        if resp.status_code != 200 and resp.status_code != 401:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 27 - Query was successful!
        self.assertTrue(result.get('code') == 27, f'expected code: 27, returned: {result.get("code")}')

    def test_method_data_restriction_with_email_external(self):
        app_id = 'f282375a9c5f4f849e2716d39bf1d627'
        login = 'gael@maldonado.com.br'
        ip = '172.30.28.28'
        self.header = set_header()
        url_with_parameters = f'{self.url}?appId={app_id}&login={login}&ip={ip}'
        resp = self.client.get(url_with_parameters, headers=self.header)
        if resp.status_code != 200 and resp.status_code != 401:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 27 - Query was successful!
        self.assertTrue(result.get('code') == 27, f'expected code: 27, returned: {result.get("code")}')

    def test_method_data_restriction_with_email_gigya(self):
        app_id = 'f282375a9c5f4f849e2716d39bf1d627'
        login = 'maldonado.py@gmail.com'
        ip = '172.30.28.28'
        self.header = set_header()
        url_with_parameters = f'{self.url}?appId={app_id}&login={login}&ip={ip}'
        resp = self.client.get(url_with_parameters, headers=self.header)
        if resp.status_code != 200 and resp.status_code != 401:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 27 - Query was successful!
        self.assertTrue(result.get('code') == 27, f'expected code: 27, returned: {result.get("code")}')

    def test_method_user_data_restriction_invalid_system(self):
        app_id = 'INVALID_APP_ID'
        login = 'INVALID_LOGIN'
        ip = 'INVALID_IP'
        self.header = set_header()
        url_with_parameters = f'{self.url}?appId={app_id}&login={login}&ip={ip}'
        resp = self.client.get(url_with_parameters, headers = self.header)
        if resp.status_code != 200 and resp.status_code != 400:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 3 - System not found or inactive!
        self.assertTrue(result.get('code') == 3, f'expected code: 3, returned: {result.get("code")}')

    def test_method_user_data_restriction_invalid_login(self):
        app_id = 'f282375a9c5f4f849e2716d39bf1d627'
        login = 'INVALID_LOGIN'
        ip = 'INVALID_IP'
        self.header = set_header()
        url_with_parameters = f'{self.url}?appId={app_id}&login={login}&ip={ip}'
        resp = self.client.get(url_with_parameters, headers = self.header)
        if resp.status_code != 200 and resp.status_code != 401:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 4 - User inactive or invalid!
        self.assertTrue(result.get('code') == 4, f'expected code: 3, returned: {result.get("code")}')
