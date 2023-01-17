from ConnectionSQL import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime


class SystemConfig(Base):
    __tablename__ = 'SystemSCA'

    IdSystemSCA = Column(Integer, primary_key=True)
    IdSystemClassification = Column(Integer)
    IdSCA = Column(Integer)
    ComKey = Column(String(100))
    ShortName = Column(String(100))
    LongName = Column(String(200))
    Description = Column(String(4000))
    Active = Column(Boolean)
    ChangeDate = Column(DateTime)
    ComKeyGenerationDate = Column(DateTime)
    MaxRowsByRequest = Column(Integer)
    ReviewExtUsers_DeadlineToAlert = Column(Integer)
    ReviewExtUsers_WarnOnDueDate = Column(Boolean)
    ReviewExtUsers_WarnDailyAfterExpiration = Column(Boolean)
    Prima_UpdateEmailMVBYV = Column(Boolean)
    Prima_EmailMVBYV = Column(String(250))
    ReviewExtUsers_FirstExecuteService = Column(String(250))
    ReviewExtUsers_NextReview = Column(Integer)
    API_NeedSendCredentials = Column(Boolean)
    API_User = Column(String(250))
    API_Password = Column(String(250))
