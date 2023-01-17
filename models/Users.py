from ConnectionSQL import Base
from sqlalchemy import Column, String, Integer, DateTime, Boolean

class UsersModel(Base):
    __tablename__ = 'users'

    ID_USER = Column(Integer, primary_key=True)
    NAME = Column(String(200))
    PASSWORD = Column(String(100))
    FAILED_LOGON_ATTEMPTS = Column(Integer)
    DT_LAST_PASSWORD_CHANGE = Column(DateTime)
    DT_LAST_LOGIN = Column(DateTime)
    STATUS = Column(String(50))
    USER_IDENTIFICATION = Column(String(250))
    DT_NEXT_PASSWORD_CHANGE = Column(DateTime)
    EMAIL = Column(String(200))
    FL_SEND_EMAIL_PASSWORD = Column(Boolean)

    def ToJson(self):
        return {
            'ID_USER' : self.ID_USER,
            'NAME' : self.NAME,
            'PASSWORD' : self.PASSWORD,
            'FAILED_LOGON_ATTEMPTS' : self.FAILED_LOGON_ATTEMPTS,
            'DT_LAST_PASSWORD_CHANGE' : self.DT_LAST_PASSWORD_CHANGE,
            'DT_LAST_LOGIN' : self.DT_LAST_LOGIN,
            'STATUS' : self.STATUS,
            'USER_IDENTIFICATION' : self.USER_IDENTIFICATION,
            'DT_NEXT_PASSWORD_CHANGE' : self.DT_NEXT_PASSWORD_CHANGE,
            'EMAIL' : self.EMAIL,
            'FL_SEND_EMAIL_PASSWORD' : self.FL_SEND_EMAIL_PASSWORD
        }