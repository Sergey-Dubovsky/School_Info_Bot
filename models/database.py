from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, declared_attr
from config import CONN_STR


class Base:
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"


engine = create_engine(CONN_STR, echo=False, pool_recycle=3600)

Base = declarative_base(bind=engine, cls=Base)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
