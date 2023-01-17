from ConnectionSQL import Session
from models.Log import LogModel


class ClsLog():

    @classmethod
    def add(cls, log_model):
        session = Session()
        session.add(log_model)
        session.commit()

    @classmethod
    def get_all(cls):
        session = Session()
        try:
            dados = session.query(LogModel).all()
            return dados
        finally:
            session.close()
