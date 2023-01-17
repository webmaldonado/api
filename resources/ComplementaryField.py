from ConnectionSQL import Session
from models.ComplementaryField import ComplementaryFieldModel


class ClsComplementaryField:

    @classmethod
    def get_by_name(cls, field_name: str) -> ComplementaryFieldModel:
        session = Session()
        try:
            dados = session\
                .query(ComplementaryFieldModel)\
                .filter(ComplementaryFieldModel.FIELD_NAME == field_name)\
                .one_or_none()
            return dados
        finally:
            session.close()
