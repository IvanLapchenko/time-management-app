from sqlalchemy import Column, Integer, Date, Time, String, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_login import UserMixin


engine = create_engine("sqlite:///app.db?check_same_thread=False")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column("id", Integer, primary_key=True)
    date = Column("date", Date)
    time = Column("time", Time, nullable=True)
    header = Column("header", String(80))
    describe = Column("describe", String(240), nullable=True)
    user = Column("user", Integer, ForeignKey("users.id"))

    def __init__(self, date, time, header, describe, user):
        super().__init__()
        self.date = date
        self.time = time
        self.header = header
        self.describe = describe
        self.user = user


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, nickname, email, password):
        super().__init__()
        self.nickname = nickname
        self.email = email
        self.password = password


#create database
Base.metadata.create_all(engine)
