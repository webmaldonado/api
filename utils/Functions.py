from LDAP import AdBayer
from models.RoleUser import RoleUserModel
from resources.RoleApprove import ClsRoleApprove
from resources.RoleUser import ClsRoleUser
from resources.Log import ClsLog
from resources.UserBayerConnected import ClsUserBayerConnected
from resources.Users import ClsUsers
from models.Log import LogModel
import datetime
from utils.Result import Result
from resources.Message import MessagesCode
from flask_api import status


def get_return(_result, _return = None):
    return {"result": _result, "return": _return}


def get_user_info_return(nome_notes, email, is_internal, system_name, cwid, dt_last_login = None):
    return {
        "nameUser": nome_notes,
        "email": email,
        "isInternal": is_internal,
        "systemName": system_name,
        "cwid": cwid,
        "dtLastLogin": dt_last_login,
        "roles": [],
        "complementaryFields": []
        }


def get_user_fisical_roles_return(user_fisical_roles, system_roles, identification):
    roles_allowed = []
    system_fisical_roles = [item.ROLE.FISICAL_ROLE_NAME for item in system_roles if item.ROLE is not None]

    restriction_codes = ClsRoleUser.get_by_identification(identification)

    for user_fisical_role in user_fisical_roles:
        if user_fisical_role in system_fisical_roles:
            item_allowed = next(item for item in system_roles if item.ROLE is not None and item.ROLE.FISICAL_ROLE_NAME == user_fisical_role)
            roles_allowed.append({
                "name": item_allowed.ROLE.NAME,
                "description": None,
                "owners": item_allowed.ROLE.RESPONSIBLE_OWNERS,
                "approveRequired": item_allowed.ROLE.FL_APPROVE_REQUIRED,
                "level": {
                    "name": str(item_allowed.ROLE.NAME).split("_")[-1],
                    "restrictionCodes": get_restriction_codes(restriction_codes, item_allowed.ROLE.NAME, item_allowed.ROLE.FL_DATA_RESTRICT_REQUIRED)
                }
            })
    return roles_allowed


def get_restriction_codes(restrictions_user, role_name, restriction_is_required):
    if restrictions_user is None:
        return ["Role Need DataRestrict"] if restriction_is_required else None

    restriction_code = [restriction for restriction in restrictions_user
                        if restriction.ROLE_NAME == role_name]

    if len(restriction_code) == 0:
        return ["Role Need DataRestrict"] if restriction_is_required else None

    return [code.strip() for code in restriction_code[0].RESTRICTION_CODES.split(';')] \
        if restriction_code[0].RESTRICTION_CODES is not None else None


def get_user_roles_return(user_roles, system_roles):
    roles_allowed = []

    if user_roles is None or system_roles is None:
        return roles_allowed

    user_roles_names = [item.ROLE_NAME for item in user_roles]
    system_roles_names = [item.ROLE.NAME for item in system_roles if item.ROLE is not None]

    for user_role_name in user_roles_names:
        if user_role_name in system_roles_names:
            item_allowed = next(item for item in system_roles if item.ROLE is not None and item.ROLE.NAME == user_role_name )
            item_allowed_restriction = next(item for item in user_roles if item.ROLE_NAME == user_role_name)
            roles_allowed.append({
                "name": item_allowed.ROLE.NAME,
                "description": None,
                "owners": item_allowed.ROLE.RESPONSIBLE_OWNERS,
                "approveRequired": item_allowed.ROLE.FL_APPROVE_REQUIRED,
                "level": {
                    "name": str(item_allowed.ROLE.NAME).split("_")[-1],
                    "restrictionCodes":
                        [code.strip() for code in item_allowed_restriction.RESTRICTION_CODES.split(';')]
                        if item_allowed_restriction.RESTRICTION_CODES is not None
                        else ["Role Need DataRestrict"] if item_allowed.ROLE.FL_DATA_RESTRICT_REQUIRED else None
                }
            })
    return roles_allowed


def get_role_guest():
    roles_allowed = []

    roles_allowed.append({
        "name": "GUEST",
        "description": None,
        "owners": None,
        "approveRequired": False,
        "level": {
            "name": "GUEST",
            "restrictionCodes": None
        }
    })
    return roles_allowed


def save_log(log_model: LogModel) -> None:
    log_model.DT_LOG = datetime.datetime.now()
    ClsLog.add(log_model)


def get_restriction_code_by_internal_user(user_fisical_roles, system_roles, identification):
    roles_allowed = []
    system_fisical_roles = [item.ROLE.FISICAL_ROLE_NAME for item in system_roles if item.ROLE is not None]

    restriction_codes = ClsRoleUser.get_by_identification(identification)

    for user_fisical_role in user_fisical_roles:
        if user_fisical_role in system_fisical_roles:
            item_allowed = next(item for item in system_roles if item.ROLE is not None and item.ROLE.FISICAL_ROLE_NAME == user_fisical_role)

            restriction_code = get_restriction_codes(restriction_codes, item_allowed.ROLE.NAME, item_allowed.ROLE.FL_DATA_RESTRICT_REQUIRED)

            if restriction_code is not None and restriction_code != ['Role Need DataRestrict']:
                roles_allowed.append(
                    {
                        "name": str(item_allowed.ROLE.NAME).split("_")[-1],
                        "restrictionCodes": restriction_code
                    })
    return roles_allowed


def get_restriction_code_by_external_user(user_roles, system_roles):
    roles_allowed = []

    if user_roles is None or system_roles is None:
        return roles_allowed

    user_roles_names = [item.ROLE_NAME for item in user_roles]
    system_roles_names = [item.ROLE.NAME for item in system_roles if item.ROLE is not None]

    for user_role_name in user_roles_names:
        if user_role_name in system_roles_names:
            item_allowed = next(item for item in system_roles if item.ROLE is not None and item.ROLE.NAME == user_role_name)
            item_allowed_restriction = next(item for item in user_roles if item.ROLE_NAME == user_role_name)
            roles_allowed.append(
                {
                    "name": str(item_allowed.ROLE.NAME).split("_")[-1],
                    "restrictionCodes":
                        [code.strip() for code in item_allowed_restriction.RESTRICTION_CODES.split(';')]
                        if item_allowed_restriction.RESTRICTION_CODES is not None
                        else ["Role Need DataRestrict"] if item_allowed.ROLE.FL_DATA_RESTRICT_REQUIRED else None
                })
    return roles_allowed


def get_complementary_fields(id_user_bayer_connected: str, id_system: str) -> list:
    list_of_fields = []
    fields = ClsUserBayerConnected.get_complementary_fields(id_user_bayer_connected, id_system)
    for field in fields:
        list_of_fields.append({
            "name": field.COMPLEMENTARY_FIELD.FIELD_NAME,
            "value": field.FIELD_VALUE
        })
    return list_of_fields


def email_is_valid(email: str) -> bool:
    return '@' in email


def email_already_in_use(email: str) -> bool:
    is_in_use = True
    attributes = tuple('mail')
    email_in_use_user_external = ClsUsers.get_by_identification(email) is not None
    ad = ad = AdBayer()
    email_in_use_user_ad = ad.get_info(email, attributes) is not None
    is_in_use = email_in_use_user_external or email_in_use_user_ad
    return is_in_use


def check_list_is_duplicate(list_of_items: list, param: str) -> bool:
    """ this function verify if item is duplicate in list """
    return len([item['name'] for item in list_of_items
                if str(item['name']).lower().strip() == param.lower().strip()]) > 1


def filter_only_approved(list_of_roles: list, id_user_bayer_connected: int, email: str) -> list:

    def get_instance_role_user(role_name):
        role_user = RoleUserModel()
        role_user.ROLE_NAME = role_name
        role_user.USER_IDENTIFICATION = email
        return role_user

    list_of_roles_approved = []
    list_of_roles_not_approved = ClsRoleApprove.get_all_not_approved(id_user_bayer_connected)
    list_of_roles_not_approved = [get_instance_role_user(item.ROLE_NAME) for item in list_of_roles_not_approved]
    for role in list_of_roles:
        if role not in list_of_roles_not_approved:
            list_of_roles_approved.append(role)

    return list_of_roles_approved


def handle_exception(e: Exception, culture: str, log_model: LogModel):
    _ret_result = Result(MessagesCode.ERROR.value, culture, str(e))
    _message_result = _ret_result.get_result()
    log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
    return get_return(_message_result), status.HTTP_200_OK


def handle_request_successful(_return, culture: str, log_model: LogModel, roles_name = ''):
    _message_result = Result(MessagesCode.QUERY_WAS_SUCCESSFUL.value, culture).get_result()
    log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
    if roles_name != '':
        log_model.DESCRIPTION = log_model.DESCRIPTION + ' | ROLES: ' + roles_name
    return get_return(_message_result, _return), status.HTTP_200_OK

def handle_request_operation_successful(_return, culture: str, log_model: LogModel):
    _message_result = Result(MessagesCode.SUCCESSFUL_OPERATION.value, culture).get_result()
    log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
    return get_return(_message_result, _return), status.HTTP_200_OK

def handle_login_successful(_return, culture: str, log_model: LogModel, roles_name = ''):
    _message_result = Result(MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL.value, culture).get_result()
    log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
    if roles_name != '':
        log_model.DESCRIPTION = log_model.DESCRIPTION + ' | ROLES: ' + roles_name
    return get_return(_message_result, _return), status.HTTP_200_OK


def error_field_is_required(field_name: str, culture: str, log_model: LogModel):
    _message_result = Result(MessagesCode.FIELD_IS_REQUIRED.value, culture, field_name).get_result()
    log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
    return get_return(_message_result), status.HTTP_200_OK


def error_system_not_found(app_id: str, culture: str, log_model: LogModel):
    _message_result = Result(MessagesCode.SYSTEM_NOT_FOUND_OR_INACTIVE.value, culture, app_id).get_result()
    log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
    log_model.NAME_SYSTEM = app_id
    return get_return(_message_result), status.HTTP_200_OK

def error_generic(log_model: LogModel):
    _message_result = Result(MessagesCode.ERROR.value, 'en-US', 'Send json in request body.').get_result()
    log_model.DESCRIPTION = _message_result['description'] + _message_result['errorResult']
    return get_return(_message_result), status.HTTP_200_OK
