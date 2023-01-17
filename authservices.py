from flask import request, redirect
from flask_api import FlaskAPI, status
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger, swag_from
# from LDAP import AdBayer
from resources.System import ClsSystem
from resources.Message import MessagesCode, ClsMessage
from resources.UserBayerConnected import ClsUserBayerConnected
from resources.Users import ClsUsers
from resources.Parameter import ClsParameter
from resources.Role import ClsRole
from resources.ComplementaryField import ClsComplementaryField
from resources.SystemConfig import ClsSystemConfig
from models.Usuarios import UsuariosModel
from resources.Usuarios import ClsUsuarios
from utils.Result import Result
from utils.Functions import *
import base64
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

app = FlaskAPI(__name__)
auth = HTTPBasicAuth()

Swagger(app, template_file='swagger/Swagger.json')

@auth.verify_password
def verify_password(username, password):

    configs = ClsSystemConfig.get('f282375a9c5f4f849e2716d39bf1d627')

    if configs.API_NeedSendCredentials == False:
        return True

    password_bytes = password.encode('ascii')
    base64_bytes = base64.b64encode(password_bytes)
    base64_password = base64_bytes.decode('ascii')

    if username.lower() == configs.API_User.lower() and base64_password == configs.API_Password:
        return True

    return False


@app.route("/")
@app.route("/swagger")
@app.route("/swagger/")
def index():
    return redirect("/apidocs")


def request_args_get(dict_value: dict, key_name: str, default_value: str) :
    if dict_value is None:
        return default_value

    if not isinstance(dict_value, dict):
        return default_value

    dict_value = dict((k.lower(), v) for k, v in dict_value.items())

    if key_name.lower() not in dict_value:
        return default_value

    return dict_value.get(key_name.lower())


@app.route("/AuthServices/password-policy", methods=['GET'])
@auth.login_required
@swag_from('swagger/password_policy.yml')
def password_policy():
    log_model: LogModel = LogModel(ACTION_LOG='Password-Policy')

    culture = request_args_get(request.args, 'culture', 'en-us')

    try:
        messages: list = []

        message_qt_character = ClsMessage.get(MessagesCode.QT_CHARACTER.value, culture).DESCRIPTION
        message_qt_attemp = ClsMessage.get(MessagesCode.QT_ATTEMPT.value, culture).DESCRIPTION
        message_qt_history = ClsMessage.get(MessagesCode.QT_PASSWORD_HISTORY.value, culture).DESCRIPTION
        message_char_special = ClsMessage.get(MessagesCode.CHARACTER_SPECIAL.value, culture).DESCRIPTION
        message_password_numbers = ClsMessage.get(MessagesCode.PASSWORD_NUMBERS.value, culture).DESCRIPTION
        message_password_chars = ClsMessage.get(MessagesCode.PASSWORD_CHARACTERS.value, culture).DESCRIPTION
        message_uppercase = ClsMessage.get(MessagesCode.UPPERCASE.value, culture).DESCRIPTION

        parameter_db = ClsParameter.get()

        message_qt_character = message_qt_character.replace('{0}', str(parameter_db.QT_CHARACTER))
        message_qt_attemp = message_qt_attemp.replace('{0}', str(parameter_db.QT_ATTEMPT))
        message_qt_history = message_qt_history.replace('{0}', str(parameter_db.QT_PASSWORD_HISTORY))
        message_char_special = message_char_special.replace('{0}', str(parameter_db.CHARACTER_SPECIAL))
        message_password_numbers = message_password_numbers.replace('{0}', str(parameter_db.PASSWORD_NUMBERS))
        message_password_chars = message_password_chars.replace('{0}', str(parameter_db.PASSWORD_CHARACTERS))
        message_uppercase = message_uppercase.replace('{0}', str(parameter_db.QT_MIN_UPPERCASE))

        messages.extend([message_qt_character,
                         message_qt_attemp,
                         message_qt_history,
                         message_char_special,
                         message_password_numbers,
                         message_password_chars,
                         message_uppercase])

        policies = {
            'policy': messages
        }

        _return = policies

    except Exception as e:
        return handle_exception(e, culture, log_model)
    else:
        return handle_request_successful(_return, culture, log_model)
    finally:
        save_log(log_model)
# *****************************************************************************************


@app.route('/AuthServices/user-data-restriction', methods=['GET'])
@auth.login_required
@swag_from('swagger/user_data_restriction.yml')
def user_data_restriction():

    log_model: LogModel = LogModel(ACTION_LOG="GetUserDataRestriction")

    args = request.args

    app_id = request_args_get(args, 'appId', '')
    login = request_args_get(args, 'login', '')
    ip = request_args_get(args, 'ip', '')
    role = request_args_get(args, 'role', '')
    culture = request_args_get(args, 'culture', 'en-us')

    try:
        if app_id == '':
            return error_field_is_required('appId', culture, log_model)

        if login == '':
            return error_field_is_required('login', culture, log_model)

        if ip == '':
            return error_field_is_required('ip', culture, log_model)

        system = ClsSystem.get_by_app_key(app_id)

        if system is None:
            return error_system_not_found(app_id, culture, log_model)

        log_model.NAME_SYSTEM = system.SHORT_NAME
        log_model.USER_ID = login
        log_model.IP_LOG = ip

        roles_allowed = []
        system_roles = system.ROLES

        if role is not None and role != '':
            system_roles = [item_role for item_role in system.ROLES if item_role.ROLE_NAME.lower() == role.lower()]

        # authentication in AD (active directory) by 'cwid' and e-mail
        ad = AdBayer()
        ret_authentication = ad.authenticate_sso(login)
        info = ad.get_info(login, ('sAMAccountName', 'displayName', 'mail'))
        if info is not None:
            _email = ''
            if info is not None:
                if (info.keys().__contains__('mail')):
                    _email = info['mail']
            user = UsuariosModel(info['displayName'], _email, info['sAMAccountName'])
            if user is not None:
                user_fisical_roles = ad.get_roles(login)
                roles_allowed = get_restriction_code_by_internal_user(user_fisical_roles,
                                                                      system_roles,
                                                                      user.IDENTIFICATION)

        # authentication in Bayer Connected (Gigya) by e-mail
        if ret_authentication != MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL:
            ret_authentication = ClsUserBayerConnected.authentication(login)
            user = ClsUserBayerConnected.get_by_identification(login)
            if user is not None:
                user_roles = ClsRoleUser.get_by_identification(user.EMAIL)
                user_roles = filter_only_approved(user_roles, user.ID_USER_BAYER_CONNECTED, user.EMAIL)
                roles_allowed = get_restriction_code_by_external_user(user_roles, system_roles)

        # authentication in EXTERNAL Users (Auth.Services) by 'cwid' and e-mail
        if ret_authentication != MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL:
            ret_authentication = ClsUsers.authentication(login)
            user = ClsUsers.get_by_identification(login)
            if user is not None:
                user_roles = ClsRoleUser.get_by_identification(user.ID_USER)
                roles_allowed = get_restriction_code_by_external_user(user_roles, system_roles)

        if ret_authentication != MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL:
            _message_result = Result(MessagesCode.USER_INACTIVE_OR_INVALID.value, culture).get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        user_name: str = user.NAME.strip()
        log_model.NAME_USER = user_name

        if len(roles_allowed) == 0:
            _message_result = Result(MessagesCode.USER_WITHOUT_ACCESS.value, culture).get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        _return = {
            "levels": roles_allowed
        }

    except Exception as e:
        return handle_exception(e, culture, log_model)
    else:
        return handle_request_successful(_return, culture, log_model)
    finally:
        save_log(log_model)
# *****************************************************************************************


@app.route('/AuthServices/users-by-system', methods=['GET'])
@auth.login_required
@swag_from('swagger/users_by_system.yml')
def users_by_system():

    log_model: LogModel = LogModel(ACTION_LOG='GetUserBySystem')

    args = request.args
    culture: str = request_args_get(args, 'culture', 'en-US')
    app_id: str = request_args_get(args, 'appId', '')
    ip: str = request_args_get(args, 'ip', '')
    login: str = request_args_get(args, 'login', '')
    role: str = request_args_get(args, 'role', '')

    _return: list = []

    try:
        if app_id == '':
            return error_field_is_required('appId', culture, log_model)

        system = ClsSystem.get_by_app_key(app_id)

        if system is None:
            return error_system_not_found(app_id, culture, log_model)

        log_model.NAME_SYSTEM = system.SHORT_NAME

        if ip == '':
            return error_field_is_required('ip', culture, log_model)

        log_model.IP_LOG = ip

        system_roles: list = [system_role for system_role in system.ROLES
                              if system_role.ROLE_NAME.upper() == role.upper() or role == '']

        system_roles: list = [sr for sr in system_roles
                              if sr.ROLE != None]

        if role != '' and len(system_roles) == 0:
            _message_result = Result(MessagesCode.ROLES_NOT_FOUND.value, culture, role).get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            log_model.USER_ID = login
            return get_return(_message_result), status.HTTP_200_OK

        users_in_ad_list = []
        users_in_external = []
        ad = AdBayer()

        users_in_ad_list.extend(AdBayer.get_all_members_by_groups(system_roles))
        users_in_external.extend(ClsRoleUser.get_members_by_roles(system_roles))

        # users in ad bayer
        users_in_ad_list = set(users_in_ad_list)

        if login != '':
            info = ad.get_info(login, ('sAMAccountName', 'displayName', 'mail'))
            if info is not None:
                users_in_ad_list = [info['sAMAccountName']]
            else:
                users_in_ad_list = []


        infos = ad.get_info_by_users(users_in_ad_list)
        for info in infos:
            if info is not None:

                info_display_name = ''
                if 'displayName' in info.keys():
                    info_display_name = info['displayName']

                info_mail = ''
                if 'mail' in info.keys():
                    info_mail = info['mail']

                info_account_name = ''
                if 'sAMAccountName' in info.keys():
                    info_account_name = info['sAMAccountName']

                user = UsuariosModel(info_display_name, info_mail, info_account_name)
                if user is not None:
                    roles_allowed = []
                    _return_item = get_user_info_return(user.NAME, user.EMAIL, False, system.SHORT_NAME,
                                                        user.IDENTIFICATION)
                    user_fisical_roles = info['roles']
                    roles_allowed = get_user_fisical_roles_return(user_fisical_roles, system_roles, user.IDENTIFICATION)
                    _return_item['roles'] = roles_allowed
                    _return.append(_return_item)
                    log_model.USER_ID = login if login != '' else None
                    log_model.NAME_USER = user.NAME if login != '' else None


        users_in_external = set(users_in_external)
        if login != '':
            info = ClsUsers.get_by_identification(login)
            if info is not None:
                users_in_external = [str(info.ID_USER)]
            else:
                users_in_external = [user_ex for user_ex in users_in_external if user_ex.upper() == login.upper()]

        for user_ex in users_in_external:

            if user_ex.isnumeric():
                # users external
                user = ClsUsers.get_by_id_user(user_ex)
                if user is not None:
                    roles_allowed = []
                    _return_item = get_user_info_return(user.NAME.strip(), user.EMAIL, False, system.SHORT_NAME,
                                                        user.USER_IDENTIFICATION, user.DT_LAST_LOGIN)
                    user_roles = ClsRoleUser.get_by_identification(user.ID_USER)
                    roles_allowed = get_user_roles_return(user_roles, system_roles)
                    _return_item['roles'] = roles_allowed
                    _return.append(_return_item)
                    log_model.USER_ID = login if login != '' else None
                    log_model.NAME_USER = user.NAME.strip() if login != '' else None
            else:
                # users bayer connected
                user = ClsUserBayerConnected.get_by_identification(user_ex)
                if user is not None:
                    roles_allowed = []
                    _return_item = get_user_info_return(user.NAME, user.EMAIL, False, system.SHORT_NAME, user.EMAIL)
                    user_roles = ClsRoleUser.get_by_identification(user.EMAIL)
                    user_roles = filter_only_approved(user_roles, user.ID_USER_BAYER_CONNECTED, user.EMAIL)
                    roles_allowed = get_user_roles_return(user_roles, system_roles)
                    _return_item['roles'] = roles_allowed
                    _return_item['complementaryFields'] = get_complementary_fields(user.ID_USER_BAYER_CONNECTED,
                                                                                   system.ID_SYSTEM)
                    _return.append(_return_item)
                    log_model.USER_ID = login if login != '' else None
                    log_model.NAME_USER = user.NAME if login != '' else None


        if login != '' and len(_return) == 0:
            _message_result = Result(MessagesCode.USER_WITHOUT_ACCESS.value, culture).get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            log_model.USER_ID = login
            return get_return(_message_result), status.HTTP_200_OK

    except Exception as e:
        return handle_exception(e, culture, log_model)
    else:
        return handle_request_successful(_return, culture, log_model)
    finally:
        save_log(log_model)
# *****************************************************************************************


@app.route("/AuthServices/roles-by-system", methods=['GET'])
@auth.login_required
@swag_from('swagger/roles_by_system.yml')
def roles_by_system():

    log_model: LogModel = LogModel(ACTION_LOG = "GetRolesBySystem")

    args = request.args
    app_id = request_args_get(args, 'appId', '')
    culture = request_args_get(args, 'culture', 'en-us')
    allow_external_user = request_args_get(args, 'allowExternalUser', '')

    try:
        if app_id == '':
            return error_field_is_required('appId', culture, log_model)

        system = ClsSystem.get_by_app_key(app_id)

        if system is None:
            return error_system_not_found(app_id, culture, log_model)

        system_roles = system.ROLES

        if allow_external_user != '':
            allow_external_user = allow_external_user.upper() == 'TRUE'
            system_roles = [item for item in system.ROLES if item.ROLE is not None and item.ROLE.ALLOW_EXTERNAL_USER == bool(allow_external_user)]

        _return_roles = []
        for system_role in system_roles:
            if system_role.ROLE is not None:
                _return_roles.append({
                    "name": system_role.ROLE.NAME,
                    "description": system_role.ROLE.ROLE_DESCRIPTION,
                    "owners": system_role.ROLE.RESPONSIBLE_OWNERS,
                    "approveRequired": system_role.ROLE.FL_APPROVE_REQUIRED,
                    "level": {
                        "name": str(system_role.ROLE.NAME).split("_")[-1],
                        "restrictionCodes": None
                    }
                })

        _return = {
            "name": system.SHORT_NAME,
            "inventory": system.INVENTORY_CODE,
            "active": system.FL_ACTIVE,
            "link": system.LINK_INVENTORY,
            "appKey": system.APPKEY,
            "allowGuest": system.ALLOW_GUEST,
            "roles": _return_roles
        }
    except Exception as e:
        log_model.NAME_SYSTEM = system.SHORT_NAME
        return handle_exception(e, culture, log_model)
    else:
        log_model.NAME_SYSTEM = system.SHORT_NAME
        return handle_request_successful(_return, culture, log_model)
    finally:
        save_log(log_model)
# *****************************************************************************************


@app.route("/AuthServices/logout", methods=['POST'])
@auth.login_required
@swag_from('swagger/logout.yml')
def logout():

    log_model: LogModel = LogModel(ACTION_LOG='LogOut')
    #culture_name = "en-US"

    if request.json is None:
        return error_generic(log_model)

    args = request.json
    culture_name = request_args_get(args, 'cultureName', 'en-us')
    login = request_args_get(args, 'login', '')
    app_id = request_args_get(args, 'appId', '')
    ip = request_args_get(args, 'ip', '')

    try:

        # login
        if login == '':
            return error_field_is_required('login', culture_name, log_model)
        log_model.USER_ID = login

        # appId
        if app_id  == '':
            return error_field_is_required('appId', culture_name, log_model)
        system = ClsSystem.get_by_app_key(app_id)
        if system is None:
            return error_system_not_found(app_id, culture_name, log_model)
        log_model.NAME_SYSTEM = system.SHORT_NAME

        # ip
        if ip  == '':
            return error_field_is_required('ip', culture_name, log_model)
        log_model.IP_LOG = ip

        user_name = ''

        # get info in AD (active directory) by 'cwid' and e-mail
        ad = AdBayer()
        info = ad.get_info(login, ('sAMAccountName', 'displayName', 'mail'))
        user_name = info['displayName'] if info is not None else ''

        # get user info Bayer Connected (Gigya) by e-mail
        if info is None:
            info = ClsUserBayerConnected.get_by_identification(login)
            user_name = info.NAME if info is not None else ''

        # get user info EXTERNAL Users (Auth.Services) by 'cwid' and e-mail
        if info is None:
            info = ClsUsers.get_by_identification(login)
            user_name = info.NAME if info is not None else ''

        log_model.NAME_USER = user_name

        if info is None:
            _message_result = Result(MessagesCode.USER_INACTIVE_OR_INVALID.value, culture_name).get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

    except Exception as e:
        return handle_exception(e, culture_name, log_model)
    else:
        return handle_request_successful(None, culture_name, log_model)
    finally:
        save_log(log_model)
# *****************************************************************************************


@app.route('/AuthServices/login', methods=['POST'])
@auth.login_required
@swag_from('swagger/login.yml')
def login():
    roles_name: str = ''
    model_log: LogModel = LogModel(ACTION_LOG='Login')

    if request.json is None:
        return error_generic(model_log)
    args = request.json
    culture_name = request_args_get(args, 'culturename', 'en-US')
    app_id = request_args_get(args, 'appid', '')
    login = request_args_get(args, 'login', '')
    password = request_args_get(args, 'password', '')
    ip = request_args_get(args, 'ip', '')

    try:

        # appId
        if app_id == '':
            return error_field_is_required('appid', culture_name, model_log)
        system = ClsSystem.get_by_app_key(app_id)
        if system is None:
            return error_system_not_found(app_id, culture_name, model_log)
        model_log.NAME_SYSTEM = system.SHORT_NAME

        # login
        if login == '':
            return error_field_is_required('login', culture_name, model_log)
        model_log.USER_ID = login

        # password
        if password == '':
            return error_field_is_required('password', culture_name, model_log)

        # ip
        if ip == '':
            return error_field_is_required('ip', culture_name, model_log)
        model_log.IP_LOG = ip

        system_roles = system.ROLES
        roles_allowed = []


        # authentication in EXTERNAL Users (Auth.Services) by 'cwid' and e-mail
        password_bytes = password.encode('ascii')
        base64_bytes = base64.b64encode(password_bytes)
        base64_password = base64_bytes.decode('ascii')
        ret_authentication = ClsUsers.authentication_with_password(login, base64_password)
        if ret_authentication == MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL:
            user = ClsUsers.get_by_identification(login)
            if user is not None:
                _return = get_user_info_return(user.NAME.strip(), user.EMAIL, False, system.SHORT_NAME,
                                                user.USER_IDENTIFICATION, user.DT_LAST_LOGIN)
                user_roles = ClsRoleUser.get_by_identification(user.ID_USER)
                roles_allowed = get_user_roles_return(user_roles, system_roles)

        # end EXT USERS
        

        # authentication in AD (active directory) by 'cwid' and e-mail
        ad = AdBayer()
        if ret_authentication != MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL:
            if '@' in login:
                cwid: str = ad.get_account_name_by_email(login)
                if cwid is None or cwid == '':
                    _message_result = Result(MessagesCode.INVALID_CREDENTIALS.value, culture_name).get_result()
                    model_log.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                    return get_return(_message_result), status.HTTP_200_OK

                ret_authentication = ad.authenticate(cwid, password)
            else:
                ret_authentication = ad.authenticate(login, password)

        if ret_authentication != MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL:
            _message_result = Result(ret_authentication.value, culture_name).get_result()
            model_log.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        user = None
        info = ad.get_info(login, ('sAMAccountName', 'displayName', 'mail'))
        if info is not None:
            _email = ''
            if info is not None:
                if (info.keys().__contains__('mail')):
                    _email = info['mail']
            user = UsuariosModel(info['displayName'], _email, info['sAMAccountName'])

        if user is not None:
            _return = get_user_info_return(user.NAME, user.EMAIL, False, system.SHORT_NAME, user.IDENTIFICATION)
            user_fisical_roles = ad.get_roles(login)
            roles_allowed = get_user_fisical_roles_return(user_fisical_roles, system_roles, user.IDENTIFICATION)

            user_name: str = user.NAME.strip()
            model_log.NAME_USER = user_name

        if ret_authentication != MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL:
            _message_result = Result(ret_authentication.value, culture_name).get_result()
            model_log.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        if system.ALLOW_GUEST is False and len(roles_allowed) == 0:
            _message_result = Result(MessagesCode.USER_WITHOUT_ACCESS.value, culture_name).get_result()
            model_log.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        if system.ALLOW_GUEST is True and len(roles_allowed) == 0:
            roles_allowed = get_role_guest()

        _return['roles'] = roles_allowed

        roles_name = ', '.join([role_allow['name'] for role_allow in roles_allowed])

    except Exception as e:
        return handle_exception(e, culture_name, model_log)
    else:
        return handle_login_successful(_return, culture_name, model_log, roles_name)
    finally:
        save_log(model_log)
# *****************************************************************************************


@app.route('/AuthServices/loginsso', methods=['POST'])
@auth.login_required
@swag_from('swagger/login_sso.yml')
def login_sso():
    log_model: LogModel = LogModel(ACTION_LOG='LoginSSO')

    roles_name: str = ''

    if request.json is None:
        return error_generic(log_model)
    args = request.json
    culture_name = request_args_get(args, 'cultureName', 'en-US')
    app_id = request_args_get(args, 'appId', '')
    login = request_args_get(args, 'login', '')
    ip = request_args_get(args, 'ip', '')

    try:

        # appId
        if app_id == '':
            return error_field_is_required('appId', culture_name, log_model)
        system = ClsSystem.get_by_app_key(app_id)
        if system is None:
            return error_system_not_found(app_id, culture_name, log_model)
        log_model.NAME_SYSTEM = system.SHORT_NAME

        # login
        if login == '':
            return error_field_is_required('login', culture_name, log_model)
        log_model.USER_ID = login

        # ip
        if ip == '':
            return error_field_is_required('ip', culture_name, log_model)
        log_model.IP_LOG = ip

        system_roles = system.ROLES
        roles_allowed = []
        complementary_fields = []

        # authentication in AD (active directory) by 'cwid' and e-mail
        ad = AdBayer()
        ret_authentication = ad.authenticate_sso(login)

        user = None
        if ret_authentication == MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL:
            info = ad.get_info(login, ('sAMAccountName', 'displayName', 'mail'))
            _email = ''
            if info is not None:
                if (info.keys().__contains__('mail')):
                    _email = info['mail']
                user = UsuariosModel(info['displayName'], _email, info['sAMAccountName'])

        if user is not None:
            _return = get_user_info_return(user.NAME, user.EMAIL, False, system.SHORT_NAME, user.IDENTIFICATION)
            user_fisical_roles = ad.get_roles(login)
            roles_allowed = get_user_fisical_roles_return(user_fisical_roles, system_roles, user.IDENTIFICATION)

        # authentication in Bayer Connected (Gigya) by e-mail
        if ret_authentication != MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL:
            ret_authentication = ClsUserBayerConnected.authentication(login)
            user = ClsUserBayerConnected.get_by_identification(login)
            if user is not None:
                _return = get_user_info_return(user.NAME, user.EMAIL, False, system.SHORT_NAME, user.EMAIL)
                user_roles = ClsRoleUser.get_by_identification(user.EMAIL)
                user_roles = filter_only_approved(user_roles, user.ID_USER_BAYER_CONNECTED, user.EMAIL)
                roles_allowed = get_user_roles_return(user_roles, system_roles)
                complementary_fields = get_complementary_fields(user.ID_USER_BAYER_CONNECTED, system.ID_SYSTEM)

        # authentication in EXTERNAL Users (Auth.Services) by 'cwid' and e-mail
        if ret_authentication != MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL:
            ret_authentication = ClsUsers.authentication(login)
            user = ClsUsers.get_by_identification(login)
            if user is not None:
                _return = get_user_info_return(user.NAME.strip(), user.EMAIL, False, system.SHORT_NAME,
                                               user.USER_IDENTIFICATION, user.DT_LAST_LOGIN)
                user_roles = ClsRoleUser.get_by_identification(user.ID_USER)
                roles_allowed = get_user_roles_return(user_roles, system_roles)

        if ret_authentication != MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL:
            _message_result = Result(ret_authentication.value, culture_name).get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        user_name = login
        if user:
            user_name: str =  user.NAME.strip()

        log_model.NAME_USER = user_name

        if system.ALLOW_GUEST is False and len(roles_allowed) == 0:
            _message_result = Result(MessagesCode.USER_WITHOUT_ACCESS.value, culture_name).get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        if system.ALLOW_GUEST is True and len(roles_allowed) == 0:
            roles_allowed = get_role_guest()

        _return['roles'] = roles_allowed
        _return['complementaryFields'] = complementary_fields

        roles_name: str = ', '.join([role_allow['name'] for role_allow in roles_allowed])

    except Exception as e:
        return handle_exception(e, culture_name, log_model)
    else:
        return handle_login_successful(_return, culture_name, log_model, roles_name)
    finally:
        save_log(log_model)
# *****************************************************************************************


@app.route("/AuthServices/add-external-user", methods=['POST'])
@auth.login_required
@swag_from('swagger/add_external_user.yml')
def add_external_user():

    log_model: LogModel = LogModel(ACTION_LOG = "AddExternalUser")

    if request.json is None:
        return error_generic(log_model)

    args = request.json
    culture_name = request_args_get(args, 'cultureName', 'en-US')
    app_id = request_args_get(args, 'appId', '')
    user_name = request_args_get(args, 'userName', '')
    email = request_args_get(args, 'email', '')
    ip = request_args_get(args, 'ip', '')
    roles = request_args_get(args, 'roles', '')
    fields = request_args_get(args, 'fields', '')

    try:

        # appId
        if app_id == '':
            return error_field_is_required('appId', culture_name, log_model)
        system = ClsSystem.get_by_app_key(app_id)
        if system is None:
            return error_system_not_found(app_id, culture_name, log_model)
        log_model.NAME_SYSTEM = system.SHORT_NAME

        if not system.ALLOW_BAYER_CONNECTED:
            _message_result = Result(MessagesCode.SYSTEM_NOT_ALLOW_USERS_BAYER_CONNECTED.value, culture_name, app_id) \
                .get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            log_model.NAME_SYSTEM = app_id
            return get_return(_message_result), status.HTTP_200_OK

        # userName
        if user_name == '':
            return error_field_is_required('userName', culture_name, log_model)
        if len(user_name) <= 5:
            _message_result = Result(MessagesCode.USER_NAME_IS_NOT_VALID.value, culture_name, user_name).get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK
        log_model.NAME_USER = user_name

        # email
        if email == '':
            return error_field_is_required('email', culture_name, log_model)
        log_model.USER_ID = email

        if not email_is_valid(email):
            _message_result = Result(MessagesCode.EMAIL_IS_NOT_VALID.value, culture_name, email).get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        if email_already_in_use(email):
            _message_result = Result(MessagesCode.THIS_EMAIL_ALREADY_ARE_AT_USING.value, culture_name, email).get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        # ip
        if ip == '':
            return error_field_is_required('ip', culture_name, log_model)
        log_model.IP_LOG = ip

        # roles
        if roles == '':
            return error_field_is_required('roles', culture_name, log_model)

        if not isinstance(roles, list):
            _message_result = Result(MessagesCode.ERROR.value,
                                     'en-US',
                                     'roles parameter is not list type.').get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        # cast items to key lower
        new_roles = list()
        for item_role in roles:
            item_role = dict((k.lower(), v) for k, v in item_role.items())
            new_roles.append(item_role)
        roles = new_roles

        if not system.ALLOW_GUEST and (roles is None or len(roles) == 0):
            _message_result = Result(MessagesCode.IT_IS_MANDATORY_TO_ASSOCIATE_ROLES.value, culture_name, 'roles')\
                .get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        for role in roles:
            if not isinstance(role, dict):
                _message_result = Result(MessagesCode.ERROR.value, 'en-US',
                                         'role object in roles is not json type.').get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            if not role.keys().__contains__('name'):
                _message_result = Result(MessagesCode.ERROR.value, 'en-US',
                                         'role object not contains the property "name".').get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            role_name: str = str(role['name']).strip()

            if not role.keys().__contains__('restriction_codes'):
                _message_result = Result(MessagesCode.ERROR.value, 'en-US',
                                         'role object not contains the property "restriction_Codes".').get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            role_restriction_codes: str = role['restriction_codes']

            if role_name is None or len(role_name) == 0:
                return error_field_is_required('roles >> name', culture_name, log_model)

            role_in_db = ClsRole.get_by_name(role_name)

            if role_in_db is None or not role_in_db.FL_ACTIVE:
                _message_result = Result(MessagesCode.ROLES_NOT_FOUND.value, culture_name, role_name) \
                    .get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            if role_in_db not in system.ROLES:
                _message_result = Result(MessagesCode.ROLE_IS_NOT_ASSOCIATE_THE_SYSTEM.value, culture_name,
                                         role_name).get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            if not role_in_db.ALLOW_EXTERNAL_USER:
                _message_result = Result(MessagesCode.ROLE_NOT_ALLOW_EXTERNAL_USER.value, culture_name,
                                         role_name).get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            role_is_duplicate = check_list_is_duplicate(roles, role_name)
            if role_is_duplicate:
                _message_result = Result(MessagesCode.DUPLICATE_ROLE_EXISTS_IN_LIST.value, culture_name,
                                         role_name).get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            role['name'] = role_in_db.NAME

        # complementary fields
        if fields == '':
            return error_field_is_required('fields', culture_name, log_model)

        if not isinstance(fields, list):
            _message_result = Result(MessagesCode.ERROR.value,
                                     'en-US',
                                     'fields parameter is not list type.').get_result()
            log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
            return get_return(_message_result), status.HTTP_200_OK

        # cast items to key lower
        new_fields = list()
        for item_field in fields:
            item_field = dict((k.lower(), v) for k, v in item_field.items())
            new_fields.append(item_field)
        fields = new_fields

        fields_required = [x for x in system.FIELDS if x.FL_REQUIRED]

        for field in fields:
            if not isinstance(field, dict):
                _message_result = Result(MessagesCode.ERROR.value, 'en-US',
                                         'field object in fields is not json type.').get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            if not field.keys().__contains__('name'):
                _message_result = Result(MessagesCode.ERROR.value, 'en-US',
                                         'field object not contains the property "name".').get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            field_name: str = str(field['name']).strip()

            if not field.keys().__contains__('value'):
                _message_result = Result(MessagesCode.ERROR.value, 'en-US',
                                         'field object not contains the property "value".').get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            field_value: str = str(field['value']).strip()

            field_in_db = ClsComplementaryField.get_by_name(field_name)

            if field_in_db is None:
                _message_result = Result(MessagesCode.ERROR.value, 'en-US',
                                         'field not found. ' + field_name).get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            if field_in_db not in system.FIELDS:
                _message_result = Result(MessagesCode.FIELD_IS_NOT_ASSOCIATE_THE_SYSTEM.value, culture_name,
                                         field_name).get_result()
                log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
                return get_return(_message_result), status.HTTP_200_OK

            if field_in_db in fields_required and len(field_value) == 0:
                return error_field_is_required(field_name, culture_name, log_model)

        for field_required in [x.FIELD.FIELD_NAME.upper() for x in system.FIELDS if x.FL_REQUIRED]:
            if field_required not in [str(x['name']).upper() for x in fields]:
                return error_field_is_required(field_required + ' in fields.', culture_name, log_model)


        request.json['roles'] = roles
        request.json['fields'] = fields

        ClsUserBayerConnected.save(request.json)

    except Exception as e:
        return handle_exception(e, culture_name, log_model)
    else:
        return handle_request_operation_successful(None, culture_name, log_model)
    finally:
        save_log(log_model)
# *****************************************************************************************


if __name__ == "__main__":
    app.run(debug=True)
