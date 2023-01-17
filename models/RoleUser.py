from ConnectionSQL import Base
from sqlalchemy import Column, String


class RoleUserModel(Base):
    __tablename__ = 'ROLE_USER'

    ROLE_NAME = Column(String(200), primary_key = True)
    USER_IDENTIFICATION = Column(String(250), primary_key = True)
    RESTRICTION_CODES = Column(String(200))

    def __eq__(self, other):
        return self.ROLE_NAME == other.ROLE_NAME and self.USER_IDENTIFICATION == other.USER_IDENTIFICATION
