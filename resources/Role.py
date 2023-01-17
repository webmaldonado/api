from ConnectionSQL import Session
from models.Role import RoleModel

class ClsRole():

    @classmethod
    def get_by_name(cls, role_name: str) -> RoleModel:
        session = Session()
        try:
            dados = session.query(RoleModel).filter(RoleModel.NAME == role_name).one_or_none()
            return dados
        finally:
            session.close()
