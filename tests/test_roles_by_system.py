import unittest
from authservices import *
from models import SystemRole
from .request_common.functions import set_header

class test_roles_by_system(unittest.TestCase):

    header = {}
    client = app.test_client()
    url = '/AuthServices/roles-by-system'

    def test_method_roles_by_system_return_Ok(self):

        app_id = 'f282375a9c5f4f849e2716d39bf1d627'
        system = ClsSystem.get_by_app_key(app_id)
        numbers_of_system_roles = len(system.ROLES)

        self.header = set_header()
        resp = self.client.get(self.url + f'?appId={app_id}', headers = self.header)

        if resp.status_code != 200:
            self.fail(f'{resp.status}')

        result: dict = dict(resp.json).get('result')
        # 27 - Query was successful!
        self.assertTrue(result.get('code') == 27, f'27 <> {result.get("code")}')

        return_dict = dict(resp.json).get('return')
        numbers_of_roles_returned = len(return_dict.get('roles'))
        self.assertTrue(numbers_of_roles_returned == numbers_of_system_roles, f'numbers of system_roles: {numbers_of_system_roles}, returned: {numbers_of_roles_returned}')


    def test_method_roles_by_system_return_external_users(self):

        app_id = 'f282375a9c5f4f849e2716d39bf1d627'
        system = ClsSystem.get_by_app_key(app_id)
        list_of_external_roles = [system_role.ROLE for system_role in system.ROLES if system_role.ROLE.ALLOW_EXTERNAL_USER]
        numbers_of_external_system_roles = len(list_of_external_roles)

        self.header = set_header()
        resp = self.client.get(self.url + f'?appId={app_id}&allowExternalUser=True', headers = self.header)

        if resp.status_code != 200:
            self.fail(f'{resp.status}')

        result: dict = dict(resp.json).get('result')
        # 27 - Query was successful!
        self.assertTrue(result.get('code') == 27, f'27 <> {result.get("code")}')

        return_dict = dict(resp.json).get('return')
        numbers_of_roles_returned = len(return_dict.get('roles'))
        self.assertTrue(numbers_of_roles_returned == numbers_of_external_system_roles, f'numbers of external system_roles: {numbers_of_external_system_roles}, returned: {numbers_of_roles_returned}')


    def test_method_roles_by_system_invalid_system(self):
        app_id = 'INVALID_APP_ID'
        self.header = set_header()
        resp = self.client.get(self.url + f'?appId={app_id}', headers = self.header)
        if resp.status_code != 200 and resp.status_code != 400:
            self.fail(f'{resp.status}')
        result: dict = dict(resp.json).get('result')
        # 3 - System not found or inactive!
        self.assertTrue(result.get('code') == 3, f'expect code: 3, returned: {result.get("code")}')