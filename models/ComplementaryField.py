from ConnectionSQL import Base
from sqlalchemy import Column, String, Integer

class ComplementaryFieldModel(Base):
    __tablename__ = 'ComplementaryField'

    ID_COMPLEMENTARY_FIELD = Column(Integer, primary_key=True)
    FIELD_NAME = Column(String(100))
