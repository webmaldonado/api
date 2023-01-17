from ConnectionSQL import Base
from sqlalchemy import Column, Integer, String, DateTime

class LogModel(Base):
    __tablename__ = 'Log'

    ID = Column(Integer, primary_key=True)
    DESCRIPTION = Column(String(1000))
    USER_ID = Column(String(100))
    DT_LOG = Column(String(DateTime))
    IP_LOG = Column(String(100))
    NAME_USER = Column(String(1000))
    NAME_SYSTEM = Column(String(1000))
    ACTION_LOG = Column(String(500))

    def ToJson(self):
        return {
            'ID' : self.ID,
            'DESCRIPTION' : self.DESCRIPTION,
            'USER_ID' : self.USER_ID,
            'DT_LOG' : self.DT_LOG,
            'IP_LOG' : self.IP_LOG,
            'NAME_USER' : self.NAME_USER,
            'NAME_SYSTEM' : self.NAME_SYSTEM,
            'ACTION_LOG' : self.ACTION_LOG
        }