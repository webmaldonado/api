from ConnectionSQL import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.ComplementaryField import ComplementaryFieldModel


class UserBayerConnectedComplementaryFieldModel(Base):
    __tablename__ = 'UserBayerConnectedComplementaryField'

    ID_USER_BAYER_CONNECTED = Column(Integer, primary_key = True)
    ID_COMPLEMENTARY_FIELD = Column(Integer, ForeignKey('ComplementaryField.ID_COMPLEMENTARY_FIELD'), primary_key = True)
    ID_SYSTEM = Column(Integer, primary_key = True)
    FIELD_VALUE = Column(String(100))
    COMPLEMENTARY_FIELD: ComplementaryFieldModel = relationship("ComplementaryFieldModel", lazy = 'selectin')
