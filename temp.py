import os

from LDAP import AdBayer
from pprint import pprint
from datetime import datetime, timedelta

from models.System import SystemModel
from resources.RoleUser import ClsRoleUser
from resources.System import ClsSystem
from resources.SystemConfig import ClsSystemConfig
from resources.Users import ClsUsers
from resources.UserBayerConnected import ClsUserBayerConnected
from resources.Log import ClsLog
from resources.Message import ClsMessage, MessagesCode
import timeit
import socket
import re
from dotenv import load_dotenv
import ldap

load_dotenv()  # take environment variables from .env.


name_user = 'AD-BAYER-CNB\\ETVBO'
# name_user = 'ETVBO'
# name_user = 'ronald.maldonado.ext@bayer.com'
# pass_user = 'Bayer160Bayer160'
# name_user = 'ad-pt.intranet.cnb\\ETVBO'
pass_user = 'Bayer160Bayer160'

LDAP_PATH = 'ldap://ad-pt.intranet.cnb'
# LDAP_PATH = 'ldap://by0w3f.azure.cnb'
# LDAP_PATH = 'ldap://azure.cnb'
# LDAP_PATH = 'ldap://bayer.cnb'

# LDAP_BASE = "dc=ad-pt.intranet, dc=cnb"
LDAP_BASE = "dc=bayer, dc=cnb"
# LDAP_BASE = "dc=azure, dc=cnb"

parameter = 'GDEVS'


configs = ClsSystemConfig.get('f282375a9c5f4f849e2716d39bf1d627')
print(configs)

'''
ad = AdBayer()
groups = ad.get_roles('etvbo')
for group in groups:
    print(group)
print (str(len(groups)) + ' roles encontradas...')
'''

'''
systems = ClsSystem.get_all()
print(systems)
'''

'''
l = ldap.initialize(LDAP_PATH)
try:
    l.protocol_version = ldap.VERSION3
    l.set_option(ldap.OPT_REFERRALS, 0)
    l.simple_bind_s(name_user, pass_user)

    criteria = "(&(objectClass=user)(|(sAMAccountName=" + parameter + ")(Mail=" + parameter + ")))"
    attributes = ['memberOf']
    result = l.search_s(LDAP_BASE, ldap.SCOPE_SUBTREE, criteria, attributes)
    results = [entry for dn, entry in result if isinstance(entry, dict)]

    if len(results) == 0:
        print(' !! CREDENCIAIS INVALIDAS !! ')

    print(' ******* LOGIN REALIZADO COM SUCESSO ****** ')

except ldap.INVALID_CREDENTIALS as exception:
    print(' !! Wrong username or password. !! ' + str(exception))
except ldap.SERVER_DOWN as exception:
    print(' !! LDAP server not available. !! ' + str(exception))
finally:
    l.unbind()
'''


'''
if 'SQLAZURECONNSTR_authservices_conn' in os.environ:
    print('AZURE : ' + os.getenv('SQLAZURECONNSTR_authservices_conn'))
else:
    print('LOCAL : ' + config.config_db)
'''


'''
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
'''

'''
import pyodbc
print([x for x in pyodbc.drivers()])
'''


'''
credential = ClientSecretCredential(
    tenant_id = 'fcb2b37b-5da0-466b-9b83-0014b67a7c78',
    client_id = 'e20c8713-e150-4ab2-b3e5-e7a29767d335',
    client_secret = '4mEM8cgc.2qcd7g4Q_ZHPjGOV~73_Vob6-'
)

compute_client = ComputeManagementClient(
    credential = credential,
    subscription_id = '634f5c30-a363-4b45-b280-20a6cd989853'
)

for vm in compute_client.virtual_machines.list_all():
    print(vm.name)
'''



'''
ad = AD_Bayer()
pprint(ad.GetRoles("etvbo"))
# print(timeit.timeit('ad.Authenticate("etzza", "Bayer150Bayer150")', globals=globals(), number=1))
'''


'''
ad = AdBayer()
groups = ad.get_roles('gdevs')
for group in groups:
    print(group)
print (str(len(groups)) + ' roles encontradas...')
'''


'''
ad = AD_Bayer()
ret_auth = ad.Authenticate('etzza', 'Bayer150Bayer150')
print(ret_auth[1])
'''

'''
ad = AD_Bayer()
ret_auth = ad.AuthenticateSSO('mmorr1')
print(ret_auth)
'''

'''
system = clsSystem.Get(5591)
print(system.ToJson())
'''


'''
systems = clsSystem.GetAll()
for system in systems:
    print(system.ToJson())
'''

'''
usuario = clsUsuarios.Get('etvbo')
print(usuario.ToJson())
'''

'''
users = clsUsers.GetAll()
for user in users:
    print(user.ToJson())
'''

'''
users = clsUserBayerConnected.GetAll()
for user in users:
    print(user.ToJson())
'''

'''
logs = clsLog.GetAll()
for log in logs:
    print(log.ToJson())
'''

'''
logs = clsLog.GetAll()
print(len(logs))
'''

# messages = clsMessage.GetAll()
# for msg in messages:
#     print(msg.ToJson())


'''
message = clsMessage.Get(27, 'en-us')
print(message.ToJson()) if message else print('message not found')
'''


'''
print(timeit.timeit('clsLog.GetAll()', globals=globals(), number=1))
'''

'''
# get ip and hostname
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
print('hostname : ' + hostname)
print('IP : ' + IP)
'''


'''
message_code = MessagesCode.QUERY_WAS_SUCCESSFUL.value
message_name = MessagesCode.QUERY_WAS_SUCCESSFUL.name
print(message_code)
print(type(message_code))
print(message_name)
'''


'''
login: str = input('digite o login : ')
password: str = 'Bayer152Bayer152'
cwid: str = ''
ad = AD_Bayer()
if '@' in login:
    cwid: str = ad.GetAccountNameByEmail(login)
    if cwid:
        ret_ad: MessagesCode = ad.Authenticate(cwid, password)
        print(ret_ad)
    else:
        print('cwid not exists...')
else:
    cwid = login
    ret_ad = ad.Authenticate(cwid, password)
    print(ret_ad)
'''


'''
ad = AD_Bayer()

attributes = ['sAMAccountName',
              'displayName',
              'mail',
              'whenCreated',
              'whenChanged',
              'lastLogonTimestamp',
              'lockoutTime']

info_list: list = ad.GetInfo('etvbo', attributes)
info_tuple: tuple = info_list[0] if len(info_list) > 0 else None
info_dict: dict = info_tuple[1] if info_tuple else None

print('**********************************************************')
print(type(info_dict))
print('**********************************************************')
pprint(info_dict)
print('**********************************************************')

info: dict = {}
for key, value in info_dict.items():
    info[key] = str(value[0], 'utf-8')

pprint(info)

print('**********************************************************')


# print(type(info))
# print(info)
'''

'''
ad = AD_Bayer()

system: list = clsSystem.GetByAppKey('f282375a9c5f4f849e2716d39bf1d627')


def show_members(fisical_role: str):
    # production
    group_to_find = fisical_role

    # quality
    # group_to_find = 'bs.a.qa-cp_iamauthservices_systemowner'

    members = ad.GetGroupMembers(group_to_find)
    
    # member = str(b'CN=ronald.maldonado,OU=Users,OU=BR,OU=Countries,DC=bayer,DC=cnb', 'utf-8')
    # pattern = 'CN=[a-zA-Z0-9]{5,20}'
    # find_result_list = re.findall(pattern, member)
    # find_str = find_result_list[0].replace('CN=', '') if find_result_list else None

    # print()
    # print('**************************************')
    # print(group_to_find)
    # print('**************************************')

    attributes = ['displayName', 'sAMAccountName']

    print('*******************************************')
    print(f'group_name : { group_to_find }')
    print('*******************************************')

    for member in members:
        info = ad.GetInfo(member, attributes)
        print(info)
        # user = clsUsuarios.Get(member)
        # print(user.DS_USERID, user.DS_NOMENOTES)

    print()


for system_role in system.ROLES:
    show_members(system_role.ROLE.FISICAL_ROLE_NAME)

'''

'''
ad = AD_Bayer()

attributes = []

info_list = ad.GetInfo('ETVBO', attributes)
print('**********************************************************')
pprint(info_list)
print('**********************************************************')
print('**********************************************************')
'''