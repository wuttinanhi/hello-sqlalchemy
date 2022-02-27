from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError


engine: Engine = create_engine('sqlite:///database.db', echo=False)

Base = declarative_base()
SessionMaker = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f"<User(id='{self.id}', username='{self.username}')>"


# create table
Base.metadata.create_all(engine)

# create session
session: Session = SessionMaker()

# create user Andy
try:
    session.add(User(username="Andy", password="AndyPassword"))
    session.commit()
except SQLAlchemyError as exception:
    print(type(exception))
    session.rollback()

# create user Bobby
try:
    session.add(User(username="Bobby", password="BobbyPassword"))
    session.commit()
except SQLAlchemyError as exception:
    print(type(exception))
    session.rollback()


# get all user
try:
    print("GET ALL USER")

    get_all_user = session.query(User).all()

    for each_user in get_all_user:
        print(each_user)

    assert len(get_all_user) == 2
finally:
    session.rollback()


# get filter
try:
    print("GET WITH FILTER")

    get_user_filter = session.query(User).filter(User.username == "Andy")

    for each_user in get_user_filter:
        assert each_user.username == "Andy"
        assert each_user.password == "AndyPassword"
        print(each_user)
finally:
    session.rollback()


# update user
try:
    print("UPDATE SEQUENCE")

    user_to_update = session.query(User).limit(1).one()
    user_to_update.username = "UpdatedUsername"
    user_to_update.password = "UpdatedPassword"

    updated_user = session.query(User).get(user_to_update.id)

    assert updated_user.username == "UpdatedUsername"
    assert updated_user.password == "UpdatedPassword"

    print(f"Updated User: {updated_user}")
finally:
    session.rollback()


# delete user
try:
    print("DELETE SEQUENCE")

    # get user to delete
    user_to_delete = session.query(User).filter(User.username == "Andy").one()

    # delete user
    session.delete(user_to_delete)

    # get all user after delete
    get_all_user_after_delete = session.query(User).all()

    assert len(get_all_user_after_delete) == 1

    for each_user in get_all_user_after_delete:
        print(each_user)
finally:
    session.rollback()
