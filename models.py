from sqlalchemy.sql.expression import text
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_no = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    trek_destination = relationship('TrekDestination', back_populates="owner") #to get all trekdestinations posted by this user





class TrekDestination(Base): #POST
    __tablename__ = "trek_destinations"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    days = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)
    total_cost = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    owner = relationship("User", back_populates="trek_destination") #who wrote this trekdestination
    itenaries = relationship("Itenary", back_populates='itenaries') #to get all iternaries of the trek destination
    comments = relationship("Comment", back_populates='comments') #to get all comment on the trek_destinations
    votes = relationship('Vote', back_populates='votes')    #to get votes on the trekdestination


class Itenary(Base):
    __tablename__ = 'iternaries'
    trek_destination_id = Column(Integer, ForeignKey("trek_destinations.id", ondelete='CASCADE'), primary_key=True)
    day = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    day_cost = Column(Integer, nullable=False)
    itenaries = relationship('TrekDestination', back_populates='itenaries')


class Comment(Base):
    __tablename__ ='comments'
    id = Column(Integer, primary_key=True, nullable=False) #isnt there any elegant solution ? 
    comment_on = Column(Integer, ForeignKey("trek_destinations.id", ondelete='CASCADE'))
    comment_by = Column(Integer, ForeignKey("users.id", ondelete= 'CASCADE')) #subject to change to set null
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    comment = Column(String, nullable=False)

    comments = relationship('TrekDestination', back_populates='comments')   

class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    trek_destination_id = Column(Integer, ForeignKey('trek_destinations.id', ondelete='CASCADE'), primary_key=True)
    votes = relationship('TrekDestination', back_populates='votes')