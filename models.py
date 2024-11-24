from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine, Integer, Text, LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker, mapped_column, Session

Base = declarative_base()
engine = create_engine('sqlite:///tickets.db')
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Users(Base):
    __tablename__ = 'Users'

    Id = mapped_column(Integer, primary_key=True)
    UserName = mapped_column(Text, nullable=False)
    Role = mapped_column(Text, nullable=False)
    PasswordSalt = mapped_column(LargeBinary, nullable=False)
    HashedPassword = mapped_column(LargeBinary, nullable=False)


def get_db_conn():
    con = None
    try:
        con = session()
        yield con
    finally:
        if con is not None:
            con.close()


Db = Annotated[Session, Depends(get_db_conn)]
