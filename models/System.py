from ConnectionSQL import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.SystemRole import SystemRoleModel
from models.SystemComplementaryField import SystemComplementaryFieldModel

class SystemModel(Base):
    __tablename__ = 'System'

    ID_SYSTEM = Column(Integer, primary_key=True)
    SHORT_NAME = Column(String(50))
    INVENTORY_CODE = Column(String(20))
    FL_ACTIVE = Column(Boolean)
    LINK_INVENTORY = Column(String(250))
    APPKEY = Column(String(100))
    ALLOW_GUEST = Column(Boolean)
    ALLOW_BAYER_CONNECTED = Column(Boolean)
    ROLES = relationship("SystemRoleModel", lazy='selectin')
    FIELDS = relationship("SystemComplementaryFieldModel", lazy = 'selectin')
