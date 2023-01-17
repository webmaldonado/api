from ConnectionSQL import Base
from sqlalchemy import Column, String, Integer, DateTime

class ParameterModel(Base):
    __tablename__ = 'Parameter'

    ID_PARAMETER = Column(Integer, primary_key=True)
    QT_DAY_ALTER = Column(Integer)
    QT_DAY_BLOCK = Column(Integer)
    QT_DAY_INACTIVE = Column(Integer)
    QT_DAY_NOTIFY = Column(Integer)
    QT_DAY_NOTIFY_FREQUENCY = Column(Integer)
    QT_DAY_NOTIFY_APPROVAL = Column(Integer)
    QT_CHARACTER = Column(Integer)
    QT_ATTEMPT = Column(Integer)
    QT_PASSWORD_HISTORY = Column(Integer)
    CHARACTER_SPECIAL = Column(String(20))
    DT_CREATE = Column(DateTime(20))
    QT_ATTEMPT_ALERT = Column(Integer)
    QT_MIN_UPPERCASE = Column(Integer)
    PASSWORD_CHARACTERS = Column(String(50))
    PASSWORD_NUMBERS = Column(String(10))
