from ConnectionSQL import Session, or_
from models.Users import UsersModel
from resources.Message import MessagesCode


class ClsUsers():

    @classmethod
    def get_all(cls):
        session = Session()
        try:
            dados = session.query(UsersModel).all()
            return dados
        finally:
            session.close()

    @classmethod
    def get_by_identification(cls, identification: str) -> UsersModel:
        session = Session()
        try:
            dados = session.query(UsersModel).filter(
                or_(UsersModel.USER_IDENTIFICATION == identification,
                    UsersModel.EMAIL == identification)).one_or_none()
            return dados
        finally:
            session.close()

    @classmethod
    def get_by_id_user(cls, id_user) -> UsersModel:
        session = Session()
        try:
            dados = session.query(UsersModel).filter(UsersModel.ID_USER == id_user).one_or_none()
            return dados
        finally:
            session.close()

    @classmethod
    def authentication(cls, identification):
        session = Session()
        try:
            dados = session.query(UsersModel).filter(
                or_(UsersModel.USER_IDENTIFICATION == identification,
                    UsersModel.EMAIL == identification)).all()
            if len(dados) > 0:
                return MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL
            else:
                return MessagesCode.INVALID_CREDENTIALS
        finally:
            session.close()


    @classmethod
    def authentication_with_password(cls, identification, password):
        session = Session()
        try:
            dados = session.query(UsersModel).filter(
                or_(UsersModel.USER_IDENTIFICATION == identification,
                    UsersModel.EMAIL == identification), UsersModel.PASSWORD == password).all()
            if len(dados) > 0:
                return MessagesCode.YOUR_LOGIN_ATTEMPT_WAS_SUCCESSFUL
            else:
                return MessagesCode.INVALID_CREDENTIALS
        finally:
            session.close()
