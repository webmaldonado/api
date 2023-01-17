from ConnectionSQL import Base
from sqlalchemy import Column, String


class UsuariosModel():

    def __init__(self, name, email, identification):
        self.NAME = name
        self.EMAIL = email
        self.IDENTIFICATION = identification

    '''
    __tablename__ = 'usuarios'

    DS_USERID = Column(String(8), primary_key=True)
    DS_NOMECOMPLETO = Column(String(1024))
    CARGO = Column(String(128))
    DS_CODTK = Column(String(3))
    DS_CODCC = Column(String(20))
    DS_AREA = Column(String(10))
    DS_EMAIL = Column(String(128))
    DS_CODEMPRESA = Column(String(10))
    DS_EMPRESA = Column(String(128))
    COUNTRY_CODE = Column(String(3))
    DS_CIDADELOCAL = Column(String(100))
    DS_USERIDGESTOR = Column(String(8))
    DS_NOMECOMPLETOGESTOR = Column(String(1024))
    DS_EMAILGESTOR = Column(String(128))
    DS_NOMENOTES = Column(String(1024))

    def ToJson(self):
        return {
            'DS_USERID' : self.DS_USERID,
            'DS_NOMECOMPLETO' : self.DS_NOMECOMPLETO,
            'CARGO' : self.CARGO,
            'DS_CODTK' : self.DS_CODTK,
            'DS_CODCC' : self.DS_CODCC,
            'DS_AREA' : self.DS_AREA,
            'DS_EMAIL' : self.DS_EMAIL,
            'DS_CODEMPRESA' : self.DS_CODEMPRESA,
            'DS_EMPRESA' : self.DS_EMPRESA,
            'COUNTRY_CODE' : self.COUNTRY_CODE,
            'DS_CIDADELOCAL' : self.DS_CIDADELOCAL,
            'DS_USERIDGESTOR' : self.DS_USERIDGESTOR,
            'DS_NOMECOMPLETOGESTOR' : self.DS_NOMECOMPLETOGESTOR,
            'DS_EMAILGESTOR' : self.DS_EMAILGESTOR,
            'DS_NOMENOTES' : self.DS_NOMENOTES
        }
    '''
