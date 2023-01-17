from ConnectionSQL import Base
from sqlalchemy import Column, Integer, String, CHAR


class MessageModel(Base):
    __tablename__ = 'Message'

    ID = Column(Integer, primary_key=True)
    CULTURE_NAME = Column(CHAR(10))
    CODE = Column(Integer)
    TYPE = Column(String(100))
    DESCRIPTION = Column(String(1000))
    CULTURE_UI_NAME = Column(String(10))
    
    def ToJson(self):
        return {
            'ID': self.ID,
            'CULTURE_NAME': self.CULTURE_NAME,
            'CODE': self.CODE,
            'TYPE': self.TYPE,
            'DESCRIPTION': self.DESCRIPTION,
            'CULTURE_UI_NAME': self.CULTURE_UI_NAME
        }