import unittest
from authservices import *
from .request_common.functions import set_header

class test_password_policy(unittest.TestCase):

    header = {}
    client = app.test_client()
    url = '/AuthServices/password-policy'

    def test_method_password_policy_return_200(self):
        self.header = set_header()
        resp = self.client.get(self.url, headers = self.header)
        self.assertTrue(resp.status_code == 200, f'{resp.status}')

    def test_method_password_policy_return_Ok(self):
        self.header = set_header()
        resp = self.client.get(self.url, headers = self.header)
        if resp.status_code != 200:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        self.assertTrue(result.get('code') == 27) # 27 - OK

    def test_method_password_policy_return_msg_EN(self):
        self.header = set_header()
        resp = self.client.get(self.url, headers = self.header)
        if resp.status_code != 200:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        description = result.get('description')
        self.assertTrue(description == 'Query was successful!')

    def test_method_password_policy_return_msg_BR(self):
        self.header = set_header()
        resp = self.client.get(self.url + '?culture=pt-BR', headers = self.header)
        if resp.status_code != 200:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        description = result.get('description')
        self.assertTrue(description == 'Consulta efetuada com sucesso!')