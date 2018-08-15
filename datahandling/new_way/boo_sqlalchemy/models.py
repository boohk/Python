# -*- coding: utf-8 -*-

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, TIMESTAMP, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
 

Base = declarative_base()
########################################################################
class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True)
    follwing_count = Column(Integer)
    follower_count = Column(Integer)
    
        #----------------------------------------------------------------------
    def __init__(self, user_id, follwing_count, follower_count):
        """"""
        self.user_id = user_id
        self.follwing_count = follwing_count
        self.follower_count = follower_count


    def __repr__(self):
         return "<User('%d', '%d', '%d')>" % (self.user_id, self.follwing_count, self.follower_count)



class Post(Base):
    """"""
    __tablename__ = "posts"
    post_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'))
    timestamp = Column(TIMESTAMP) 
    extracted_tags = Column(String(10000))
    contents_url = Column(String(1000))
    like_count = Column(Integer)
    comment_count = Column(Integer)
    
    #----------------------------------------------------------------------
    def __init__(self, post_id, user_id, timestamp, extracted_tags, contents_url, like_count, comment_count):
        """"""
        self.post_id = post_id
        self.user_id = user_id
        self.timestamp = str(timestamp)
        self.extracted_tags = extracted_tags
        self.contents_url = contents_url
        self.like_count = like_count
        self.comment_count = comment_count

    
    def __repr__(self):
         return "<Post('%d', '%s', '%d', '%s', '%s', '%d', '%d')>" % (self.post_id, self.user_id, self.timestamp, self.extracted_tags, self.contents_url, self.like_count, self.comment_count)