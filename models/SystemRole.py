from ConnectionSQL import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.Role import RoleModel

class SystemRoleModel(Base):
    __tablename__ = 'SYSTEM_ROLE'

    ID_SYSTEM = Column(Integer, ForeignKey('System.ID_SYSTEM'), primary_key=True)
    ROLE_SEGREGATION_RESTRICTIONS = Column(String(100))
    ROLE_NAME = Column(String(200), ForeignKey('Role.NAME'), primary_key=True)
    ROLE = relationship("RoleModel", lazy='selectin')

    def __eq__(self, other):
        if (other == None):
            return False
        if (self.ROLE == None):
            return False
        return self.ROLE.NAME.upper() == other.NAME.upper()
