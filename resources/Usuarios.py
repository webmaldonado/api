from ConnectionSQL import Session, or_
from models.Usuarios import UsuariosModel


class ClsUsuarios():
    pass

'''
    @classmethod
    def get(cls, cwid):
        session = Session()
        try:
            dados = session.query(UsuariosModel).filter(
                or_(UsuariosModel.DS_USERID == cwid,
                    UsuariosModel.DS_EMAIL == cwid)).one()
            return dados
        finally:
            session.close()
'''
