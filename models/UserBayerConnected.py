from ConnectionSQL import Base
from sqlalchemy import Column, String, Integer

class UserBayerConnectedModel(Base):
    __tablename__ = 'UserBayerConnected'

    ID_USER_BAYER_CONNECTED = Column(Integer, primary_key=True)
    ID_BAYER_CONNECTED = Column(String(200))
    EMAIL = Column(String(100))
    FIRST_NAME = Column(String(50))
    LAST_NAME = Column(String(50))
    NAME = Column(String(100))

    def ToJson(self):
        return {
            'ID_USER_BAYER_CONNECTED' : self.ID_USER_BAYER_CONNECTED,
            'ID_BAYER_CONNECTED' : self.ID_BAYER_CONNECTED,
            'EMAIL' : self.EMAIL,
            'FIRST_NAME' : self.FIRST_NAME,
            'LAST_NAME' : self.LAST_NAME,
            'NAME' : self.NAME
        }