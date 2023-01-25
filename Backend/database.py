from typing import Generator
from sqlmodel import SQLModel, Session, create_engine

sqlite_file_name:str = 'acc.db'
sqlite_url:str = f'sqlite:///{sqlite_file_name}'

connect_args:dict = {"check_same_thread" : False}
echo:bool = False

engine = create_engine(sqlite_url, echo=echo, connect_args=connect_args)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator:
    with Session(engine) as session:
        yield session