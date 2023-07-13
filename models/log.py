from models.mixins import LogTimestampMixin
from sqlalchemy import Column, String, Numeric, Boolean
from .database import Base

# таблица для сохранения логов

class Log(Base, LogTimestampMixin):
    info= Column(String(50), nullable=True, index=True)  
    user_id = Column(Numeric(precision=10, scale=0), nullable=True, index=True)
    user_username = Column(String(25), nullable=True, index=True)  
    user_firstname = Column(String(25), nullable=True, index=True)  
    user_lastname = Column(String(25), nullable=True, index=True)  

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"info={self.info!r},"
            f"user_id={self.user_id!r},"
            f"user_username={self.user_username!r},"
            f"user_firstname={self.user_firstname!r},"
            f"user_lastname={self.user_lastname!r},"
        )

    def __repr__(self):
        return str(self)
