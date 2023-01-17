from ConnectionSQL import Session
from models.Message import MessageModel
from enum import Enum


class ClsMessage():

    @classmethod
    def get_all(cls):
        session = Session()
        try:
            dados = session.query(MessageModel).all()
            return dados
        finally:
            session.close()

    @classmethod
    def get(cls, code, culture_name):
        session = Session()
        try:
            dados = session.query(MessageModel).filter(MessageModel.CODE == code,
                                                       MessageModel.CULTURE_NAME == culture_name).first()
            return dados
        finally:
            session.close()


class MessagesCode(Enum):
    NO_MESSAGE_WAS_FOUND = 0
    YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL = 1
    INVALID_CREDENTIALS = 2
    SYSTEM_NOT_FOUND_OR_INACTIVE = 3
    USER_INACTIVE_OR_INVALID = 4
    ROLES_NOT_FOUND = 5
    LOGOUT_SUCCESSFUL = 8
    USER_WITHOUT_ACCESS = 13
    QUERY_WAS_SUCCESSFUL = 27
    ERROR = 29
    ROLE_IS_NOT_ASSOCIATE_THE_SYSTEM = 39
    SUCCESSFUL_OPERATION = 40
    IT_IS_MANDATORY_TO_ASSOCIATE_ROLES = 41
    EMAIL_IS_NOT_VALID = 44
    USER_NAME_IS_NOT_VALID = 45
    ROLE_NOT_ALLOW_EXTERNAL_USER = 46
    DUPLICATE_ROLE_EXISTS_IN_LIST = 47
    ACTIVE_DIRECTORY_IS_UNAVALIABLE = 48
    SYSTEM_NOT_ALLOW_USERS_BAYER_CONNECTED = 49
    THIS_EMAIL_ALREADY_ARE_AT_USING = 50
    FIELD_IS_NOT_ASSOCIATE_THE_SYSTEM = 51
    FIELD_IS_REQUIRED = 52

    # this messages are password policy
    QT_CHARACTER = 30
    QT_ATTEMPT = 31
    QT_PASSWORD_HISTORY = 32
    CHARACTER_SPECIAL = 33
    PASSWORD_NUMBERS = 34
    PASSWORD_CHARACTERS = 35
    UPPERCASE = 36

