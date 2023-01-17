from ConnectionSQL import Session
from models.System import SystemModel


class ClsSystem():

    @classmethod
    def get_all(cls):
        session = Session()
        try:
            dados = session.query(SystemModel).all()
            return dados
        finally:
            session.close()

    @classmethod
    def get(cls, id_system):
        session = Session()
        try:
            dados = session.query(SystemModel).filter(SystemModel.ID_SYSTEM == id_system).one_or_none()
            return dados
        finally:
            session.close()

    @classmethod
    def get_by_app_key(cls, app_key) -> SystemModel:
        session = Session()
        try:
            dados = session.query(SystemModel).filter(SystemModel.APPKEY == app_key).one_or_none()
            return dados
        finally:
            session.close()
