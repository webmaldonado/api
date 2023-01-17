from ConnectionSQL import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class RoleApproveModel(Base):
    __tablename__ = 'RoleApprove'
    __table_args__ = {'implicit_returning': False}

    ID_ROLE_APPROVE = Column(Integer, primary_key = True)
    ROLE_NAME = Column(String(200))
    ID_USER_BAYER_CONNECTED = Column(Integer)
    FL_APPROVE = Column(Boolean)
    ID_OWNER = Column(String(50))
    DT_ACTION = Column(String(DateTime))
    DESCRIPTION = Column(String(500))
