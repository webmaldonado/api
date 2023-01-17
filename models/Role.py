from ConnectionSQL import Base
from sqlalchemy import Column, String, Boolean

class RoleModel(Base):
    __tablename__ = 'Role'

    NAME = Column(String(200), primary_key=True)
    RESPONSIBLE_OWNERS = Column(String(200))
    FISICAL_ROLE_NAME = Column(String(200))
    FL_ACTIVE = Column(Boolean)
    ALLOW_EXTERNAL_USER = Column(Boolean)
    FL_DATA_RESTRICT_REQUIRED = Column(Boolean)
    ROLE_DESCRIPTION = Column(String(200))
    FL_APPROVE_REQUIRED = Column(Boolean)

'''
    def __eq__(self, other):
        return self.NAME.upper() == other.NAME.upper()
'''
