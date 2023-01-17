from ConnectionSQL import Session
from models.SystemConfig import SystemConfig


class ClsSystemConfig():

    @classmethod
    def get(cls, comkey) -> SystemConfig:
        session = Session()
        try:
            dados = session.query(SystemConfig).filter(SystemConfig.ComKey == comkey).one_or_none()
            return dados
        finally:
            session.close()
