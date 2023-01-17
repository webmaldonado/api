import ldap
import functools
import re
import os
from resources.Message import MessagesCode

AD_ADDRESS = os.getenv('LDAP_ADDRESS')
DOMAIN = "AD-BAYER-CNB\\"
LDAP_BASE = "dc=bayer, dc=cnb"
USER_AD = os.getenv('LDAP_USER')
PASSWORD_AD = os.getenv('LDAP_PASS')


class AdBayer():

    def __init__(self):
        self.USER_AD = os.getenv('LDAP_USER')
        self.PASSWORD_AD = os.getenv('LDAP_PASS')

    @classmethod
    def generate_criteria_username_or_email(cls, parameter):
        return "(&(objectClass=user)(|(sAMAccountName=" + parameter + ")(Mail=" + parameter + ")))"

    @classmethod
    def generate_criteria_groupname(cls, parameter):
        return '(&(objectClass=GROUP)(cn=' + parameter + '))'

    @functools.lru_cache(maxsize=None)
    def authenticate(self, user, password):
        l = ldap.initialize(AD_ADDRESS)
        try:
            l.protocol_version = ldap.VERSION3
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(DOMAIN + user, password)
            return MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL
        except ldap.INVALID_CREDENTIALS:
            return MessagesCode.INVALID_CREDENTIALS
        finally:
            l.unbind()

    @functools.lru_cache(maxsize=None)
    def authenticate_sso(self, user):
        l = ldap.initialize(AD_ADDRESS)
        try:
            l.protocol_version = ldap.VERSION3
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(DOMAIN + self.USER_AD, self.PASSWORD_AD)
            criteria = self.generate_criteria_username_or_email(user)
            attributes = ['memberOf']
            result = l.search_s(LDAP_BASE, ldap.SCOPE_SUBTREE, criteria, attributes)
            results = [entry for dn, entry in result if isinstance(entry, dict)]
            if len(results) == 0:
                return MessagesCode.INVALID_CREDENTIALS
            return MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL
        except ldap.INVALID_CREDENTIALS:
            return MessagesCode.ACTIVE_DIRECTORY_IS_UNAVALIABLE
        finally:
            l.unbind()

    @functools.lru_cache(maxsize=None)
    def get_roles(self, user):
        l = ldap.initialize(AD_ADDRESS)
        try:
            l.protocol_version = ldap.VERSION3
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(DOMAIN + self.USER_AD, self.PASSWORD_AD)
            criteria = self.generate_criteria_username_or_email(user)
            attributes = ['memberOf']
            result = l.search_s(LDAP_BASE, ldap.SCOPE_SUBTREE, criteria, attributes)
            results = [entry for dn, entry in result if isinstance(entry, dict)]
            if len(results) == 0:
                return []
            objects = results[0]['memberOf']
            roles = []
            for item in objects:
                group_name_partial = str(item).split(",")
                roles.append(group_name_partial[0].replace("b'CN=", ""))
            return roles
        except ldap.INVALID_CREDENTIALS:
            return MessagesCode.ACTIVE_DIRECTORY_IS_UNAVALIABLE
        finally:
            l.unbind()

    @functools.lru_cache(maxsize=None)
    def get_account_name_by_email(self, email: str) -> str:
        account_name: str = None
        l = ldap.initialize(AD_ADDRESS)
        try:
            l.protocol_version = ldap.VERSION3
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(DOMAIN + self.USER_AD, self.PASSWORD_AD)
            criteria = self.generate_criteria_username_or_email(email)
            attributes = ['sAMAccountName']
            result = l.search_s(LDAP_BASE, ldap.SCOPE_SUBTREE, criteria, attributes)

            if isinstance(result, list) and len(result) > 0:
                account_name_tuple: tuple = result[0]
                account_name_dict: dict = account_name_tuple[1]
                account_name_list: list = account_name_dict['sAMAccountName']
                account_name_bytes: bytes = account_name_list[0]
                account_name = account_name_bytes.decode("utf-8")

            return account_name
        except Exception as e:
            return str(e)
        finally:
            l.unbind()

    @functools.lru_cache(maxsize=None)
    def get_info(self, identification: str, attributes: tuple) -> dict:
        l = ldap.initialize(AD_ADDRESS)
        try:
            l.protocol_version = ldap.VERSION3
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(DOMAIN + self.USER_AD, self.PASSWORD_AD)
            criteria = self.generate_criteria_username_or_email(identification)
            result = l.search_s(LDAP_BASE, ldap.SCOPE_SUBTREE, criteria, attributes)

            info_tuple: tuple = result[0] if len(result) > 0 else None
            info_dict: dict = info_tuple[1] if info_tuple else None

            info: dict = {}
            for key, value in info_dict.items():
                info[key] = str(value[0], 'utf-8')

            return info
        except:
            return None
        finally:
            l.unbind()

    @classmethod
    def get_info_by_users(cls, users: set) -> list:
        config_user_ad = USER_AD
        config_user_password = PASSWORD_AD
        l = ldap.initialize(AD_ADDRESS)
        try:
            l.protocol_version = ldap.VERSION3
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(DOMAIN + config_user_ad, config_user_password)

            list_of_info: list = []
            for user in users:

                # buscar as informacoes do usuario
                criteria = cls.generate_criteria_username_or_email(user)
                result = l.search_s(LDAP_BASE, ldap.SCOPE_SUBTREE, criteria, ('sAMAccountName', 'displayName', 'mail', 'memberOf'))

                info_tuple: tuple = result[0] if len(result) > 0 else None
                info_dict: dict = info_tuple[1] if info_tuple else None

                info: dict = {}
                for key, value in info_dict.items():
                    info[key] = str(value[0], 'utf-8')

                # buscar as roles do usuario
                results = [entry for dn, entry in result if isinstance(entry, dict)]
                if len(results) == 0:
                    return []
                objects = results[0]['memberOf']
                roles = []
                for item in objects:
                    group_name_partial = str(item).split(",")
                    roles.append(group_name_partial[0].replace("b'CN=", ""))

                info['roles'] = roles

                list_of_info.append(info)

            return list_of_info
        finally:
            l.unbind()

    @functools.lru_cache(maxsize=None)
    def get_group_members(self, group_name: str):
        members = []
        l = ldap.initialize(AD_ADDRESS)
        try:
            l.protocol_version = ldap.VERSION3
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(DOMAIN + self.USER_AD, self.PASSWORD_AD)
            criteria = self.generate_criteria_groupname(group_name)
            result = l.search_s(LDAP_BASE, ldap.SCOPE_SUBTREE, criteria)

            members_list = self.extract_members(result)

            pattern_search = 'CN=[a-zA-Z0-9]{5,20}'
            if members_list:
                for member in members_list:
                    find_result_list = re.findall(pattern_search, str(member, 'utf-8'))
                    find_str = find_result_list[0].replace('CN=', '') if find_result_list else None
                    if find_str:
                        members.append(find_str)

            return members
        finally:
            l.unbind()

    @classmethod
    def get_all_members_by_groups(cls, groups):
        config_user_ad = USER_AD
        config_password_ad = PASSWORD_AD
        members = []
        l = ldap.initialize(AD_ADDRESS)
        try:
            l.protocol_version = ldap.VERSION3
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(DOMAIN + config_user_ad, config_password_ad)

            for group in groups:

                if group.ROLE != None:
                    criteria = cls.generate_criteria_groupname(group.ROLE.FISICAL_ROLE_NAME)
                    result = l.search_s(LDAP_BASE, ldap.SCOPE_SUBTREE, criteria)

                    members_list = cls.extract_members(result)

                    pattern_search = 'CN=[a-zA-Z0-9]{5,20}'
                    if members_list:
                        for member in members_list:
                            find_result_list = re.findall(pattern_search, str(member, 'utf-8'))
                            find_str = find_result_list[0].replace('CN=', '') if find_result_list else None
                            if find_str:
                                members.append(find_str)


            return members
        finally:
            l.unbind()

    @classmethod
    def extract_members(cls, result) -> list:
        members_tuple: tuple = result[0] if len(result) > 0 else None
        members_dict: dict = members_tuple[1] if members_tuple else None
        members_list: list = members_dict['member'] if members_dict and 'member' in members_dict and len(
            members_dict) > 1 else None
        return members_list