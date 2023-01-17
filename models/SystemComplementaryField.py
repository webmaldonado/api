from ConnectionSQL import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.ComplementaryField import ComplementaryFieldModel


class SystemComplementaryFieldModel(Base):
    __tablename__ = 'SystemComplementaryField'

    ID_SYSTEM = Column(Integer, ForeignKey('System.ID_SYSTEM'), primary_key = True)
    ID_COMPLEMENTARY_FIELD = Column(Integer, ForeignKey('ComplementaryField.ID_COMPLEMENTARY_FIELD'), primary_key = True)
    FL_REQUIRED = Column(Boolean)

    FIELD = relationship("ComplementaryFieldModel", lazy = 'selectin')

    def __eq__(self, other):
        return self.FIELD.FIELD_NAME == other.FIELD_NAME
