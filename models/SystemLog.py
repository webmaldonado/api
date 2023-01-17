from ConnectionSQL import Base
from sqlalchemy import Column, Integer, String, DateTime


class SystemLogModel(Base):
    __tablename__ = 'SystemLog'

    IdSystemLog = Column(Integer, primary_key = True)
    IdSystemSCA = Column(Integer)
    IdSystemLogAction = Column(Integer)
    SystemLogDate = Column(String(DateTime))
    UserChange = Column(String(100))
    FunctionName = Column(String(100))
    Description = Column(String(1000))
    IdDocument = Column(String(1000))
