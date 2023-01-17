from ConnectionSQL import Session
from models.Parameter import ParameterModel


class ClsParameter():

    @classmethod
    def get(cls) -> ParameterModel:
        session = Session()
        try:
            dados = session.query(ParameterModel).one_or_none()
            return dados
        finally:
            session.close()
