from ConnectionSQL import Session, or_
from models.Log import LogModel
from models.RoleApprove import RoleApproveModel
from models.RoleUser import RoleUserModel
from models.SystemLog import SystemLogModel
from models.UserBayerConnected import UserBayerConnectedModel
from resources.ComplementaryField import ClsComplementaryField
from resources.Message import MessagesCode
from resources.Log import ClsLog
from models.UserBayerConnectedComplementaryField import UserBayerConnectedComplementaryFieldModel
import datetime

from resources.Role import ClsRole
from resources.RoleUser import ClsRoleUser
from resources.System import ClsSystem

FUNCTION_NAME = '/AuthServices/RoleUser/Edit/'

USER_CHANGE = 'API Auth.Services'


def get_fisrt_name(name: str) -> str:
    try:
        return name.split()[0]
    except (Exception):
        return ''

def get_last_name(name: str) -> str:
    try:
        return name.split()[-1]
    except (Exception):
        return ''


class ClsUserBayerConnected():

    @classmethod
    def get_all(cls):
        session = Session()
        try:
            dados = session.query(UserBayerConnectedModel).all()
            return dados
        finally:
            session.close()

    @classmethod
    def get_by_identification(cls, identification) -> UserBayerConnectedModel:
        session = Session()
        try:
            dados = session.query(UserBayerConnectedModel).filter(
                or_(UserBayerConnectedModel.EMAIL == identification,
                    UserBayerConnectedModel.ID_BAYER_CONNECTED == identification)).one_or_none()
            return dados
        finally:
            session.close()

    @classmethod
    def authentication(cls, identification):
        session = Session()
        try:
            dados = session.query(UserBayerConnectedModel).filter(
                or_(UserBayerConnectedModel.EMAIL == identification,
                    UserBayerConnectedModel.ID_BAYER_CONNECTED == identification)).all()
            if len(dados) > 0:
                return MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL
            else:
                return MessagesCode.INVALID_CREDENTIALS
        finally:
            session.close()

    @classmethod
    def get_complementary_fields(cls, id_user_bayer_connected: str, id_system: str) -> list:
        session = Session()
        try:
            dados = session\
                .query(UserBayerConnectedComplementaryFieldModel)\
                .filter(UserBayerConnectedComplementaryFieldModel.ID_USER_BAYER_CONNECTED == id_user_bayer_connected)\
                .filter(UserBayerConnectedComplementaryFieldModel.ID_SYSTEM == id_system)\
                .all()
            return dados
        finally:
            session.close()

    @classmethod
    def save(cls, json: dict):
        session = Session()
        try:

            json = dict((k.lower(), v) for k, v in json.items())

            user = UserBayerConnectedModel()
            user_already_exist = ClsUserBayerConnected.get_by_identification(json['email'])
            system = ClsSystem.get_by_app_key(json['appid'])

            if user_already_exist is None:
                user.ID_BAYER_CONNECTED = json['email']
                user.EMAIL = json['email']
                user.FIRST_NAME = get_fisrt_name(json['username'])
                user.LAST_NAME = get_last_name(json['username'])
                user.NAME = json['username']
                session.add(user)

                user_new = session\
                    .query(UserBayerConnectedModel)\
                    .filter(UserBayerConnectedModel.EMAIL == user.EMAIL)\
                    .one()

                log = LogModel()
                log.ACTION_LOG = "Usuario"
                log.DT_LOG = datetime.datetime.now()
                log.IP_LOG = "127.0.0.0"
                log.USER_ID = user.ID_BAYER_CONNECTED
                log.NAME_USER = user.NAME
                log.NAME_SYSTEM = system.SHORT_NAME
                log.DESCRIPTION = f'User { user.NAME } registered.'
                session.add(log)

                system_log = SystemLogModel()
                system_log.IdSystemSCA = 1
                system_log.IdSystemLogAction = 6
                system_log.SystemLogDate = datetime.datetime.now()
                system_log.UserChange = USER_CHANGE
                system_log.FunctionName = '/AuthServices/UserBayerConnected/Edit/'
                system_log.Description = 'Insert User Bayer Connected'
                system_log.IdDocument = user_new.ID_USER_BAYER_CONNECTED
                session.add(system_log)

                for role in json['roles']:

                    role_name = str(role['name']).strip()

                    role_user = RoleUserModel()
                    role_user.ROLE_NAME = role_name
                    role_user.RESTRICTION_CODES = role['restriction_codes']
                    role_user.USER_IDENTIFICATION = user.EMAIL
                    session.add(role_user)

                    role_in_db = ClsRole.get_by_name(role_name)

                    if role_in_db.FL_APPROVE_REQUIRED:
                        role_approve = RoleApproveModel()
                        role_approve.ID_USER_BAYER_CONNECTED = user_new.ID_USER_BAYER_CONNECTED
                        role_approve.ROLE_NAME = role_name
                        session.add(role_approve)

                        system_log = SystemLogModel()
                        system_log.IdSystemSCA = 1
                        system_log.IdSystemLogAction = 6
                        system_log.SystemLogDate = datetime.datetime.now()
                        system_log.UserChange = USER_CHANGE
                        system_log.FunctionName = FUNCTION_NAME
                        system_log.Description = 'Role Waiting Approval'
                        system_log.IdDocument = f'{role_approve.ROLE_NAME}_{user.EMAIL}'
                        session.add(system_log)

                        log = LogModel()
                        log.ACTION_LOG = "Usuario"
                        log.DT_LOG = datetime.datetime.now()
                        log.IP_LOG = "127.0.0.0"
                        log.USER_ID = user.ID_BAYER_CONNECTED
                        log.NAME_USER = user.NAME
                        log.NAME_SYSTEM = system.SHORT_NAME
                        log.DESCRIPTION = f'Access requested to system {system.SHORT_NAME} for user ' \
                                          f'({user.ID_BAYER_CONNECTED}) {user.NAME} with profile {role_name}. ' \
                                          f'Waiting approval.'
                        session.add(log)
                    else:
                        log = LogModel()
                        log.ACTION_LOG = "Usuario"
                        log.DT_LOG = datetime.datetime.now()
                        log.IP_LOG = "127.0.0.0"
                        log.USER_ID = user.ID_BAYER_CONNECTED
                        log.NAME_USER = user.NAME
                        log.NAME_SYSTEM = system.SHORT_NAME
                        log.DESCRIPTION = f'Access requested to system {system.SHORT_NAME} for user ' \
                                          f'({user.ID_BAYER_CONNECTED}) {user.NAME} with profile {role_name}.'
                        session.add(log)

                        system_log = SystemLogModel()
                        system_log.IdSystemSCA = 1
                        system_log.IdSystemLogAction = 6
                        system_log.SystemLogDate = datetime.datetime.now()
                        system_log.UserChange = USER_CHANGE
                        system_log.FunctionName = FUNCTION_NAME
                        system_log.Description = 'Insert role approved'
                        system_log.IdDocument = f'{role_name}_{user.EMAIL}'
                        session.add(system_log)

                for field in json['fields']:

                    field_name = str(field['name']).strip()
                    field_value = str(field['value']).strip()

                    field_in_db = ClsComplementaryField.get_by_name(field_name)

                    user_field = UserBayerConnectedComplementaryFieldModel()
                    user_field.ID_USER_BAYER_CONNECTED = user.ID_USER_BAYER_CONNECTED
                    user_field.ID_COMPLEMENTARY_FIELD = field_in_db.ID_COMPLEMENTARY_FIELD
                    user_field.ID_SYSTEM = system.ID_SYSTEM
                    user_field.FIELD_VALUE = field_value
                    session.add(user_field)
            else:
                # update user

                system_log = SystemLogModel()
                system_log.IdSystemSCA = 1
                system_log.IdSystemLogAction = 6
                system_log.SystemLogDate = datetime.datetime.now()
                system_log.UserChange = USER_CHANGE
                system_log.FunctionName = '/AuthServices/UserBayerConnected/Edit/'
                system_log.Description = 'Update User Bayer Connected'
                system_log.IdDocument = user_already_exist.ID_USER_BAYER_CONNECTED
                session.add(system_log)

                for role in json['roles']:

                    role_name = str(role['name']).strip()
                    restriction_code = str(role['restriction_codes']).strip()

                    role_user = RoleUserModel()
                    role_user.ROLE_NAME = role_name
                    role_user.USER_IDENTIFICATION = user_already_exist.EMAIL
                    role_user.RESTRICTION_CODES = restriction_code

                    role_in_db = ClsRole.get_by_name(role_name)

                    user_list_of_roles = ClsRoleUser.get_by_identification(user_already_exist.EMAIL)

                    if role_user not in user_list_of_roles:
                        session.add(role_user)

                        # register log
                        log = LogModel()
                        log.ACTION_LOG = "Usuario"
                        log.DT_LOG = datetime.datetime.now()
                        log.IP_LOG = "127.0.0.0"
                        log.USER_ID = user.ID_BAYER_CONNECTED
                        log.NAME_USER = user_already_exist.NAME
                        log.NAME_SYSTEM = system.SHORT_NAME
                        log.DESCRIPTION = f'Access requested to system {system.SHORT_NAME} for user ' \
                                          f'({user_already_exist.ID_BAYER_CONNECTED}) {user_already_exist.NAME} with profile {role_name}. '
                        session.add(log)

                        if role_in_db.FL_APPROVE_REQUIRED:
                            role_approve = RoleApproveModel()
                            role_approve.ROLE_NAME = role_in_db.NAME
                            role_approve.ID_USER_BAYER_CONNECTED = user_already_exist.ID_USER_BAYER_CONNECTED
                            session.add(role_approve)

                            system_log = SystemLogModel()
                            system_log.IdSystemSCA = 1
                            system_log.IdSystemLogAction = 6
                            system_log.SystemLogDate = datetime.datetime.now()
                            system_log.UserChange = USER_CHANGE
                            system_log.FunctionName = FUNCTION_NAME
                            system_log.Description = 'Role Waiting Approval'
                            system_log.IdDocument = f'{role_approve.ROLE_NAME}_{user_already_exist.EMAIL}'
                            session.add(system_log)

                            log = LogModel()
                            log.ACTION_LOG = "Usuario"
                            log.DT_LOG = datetime.datetime.now()
                            log.IP_LOG = "127.0.0.0"
                            log.USER_ID = user_already_exist.ID_BAYER_CONNECTED
                            log.NAME_USER = user_already_exist.NAME
                            log.NAME_SYSTEM = system.SHORT_NAME
                            log.DESCRIPTION = f'Access requested to system {system.SHORT_NAME} for user ' \
                                              f'({user_already_exist.ID_BAYER_CONNECTED}) {user_already_exist.NAME} with profile {role_name}. ' \
                                              f'Waiting approval.'
                            session.add(log)
                        else:
                            system_log = SystemLogModel()
                            system_log.IdSystemSCA = 1
                            system_log.IdSystemLogAction = 6
                            system_log.SystemLogDate = datetime.datetime.now()
                            system_log.UserChange = USER_CHANGE
                            system_log.FunctionName = FUNCTION_NAME
                            system_log.Description = 'Insert role approved'
                            system_log.IdDocument = f'{role_in_db.NAME}_{user_already_exist.EMAIL}'
                            session.add(system_log)

            session.commit()
        except (Exception):
            session.rollback()
        finally:
            session.close()
