# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from models import Base, User, Post
from sqlalchemy.orm import sessionmaker


class MySQLconnector:
    def __init__(self, db_uri):
        self.db_uri = db_uri
    
    def connect_engine(self):
        return create_engine(self.db_uri)
    
    def connect_session(self):
        Session = sessionmaker(bind=self.connect_engine())
        return Session()
    
    # create tables
    def craete_tables(self):
        Base.metadata.create_all(bind=self.connect_engine())
    
    def drop_tables(self):
        Base.metadata.drop_all(bind=self.connect_engine())
   
    """
    insert, select,  :세션이 정의되어야 사용 가능하다.
    
    """
    @staticmethod
    def insert(objects):
        if type(objects) == list:       
            session.add_all(objects)
        else:
            session.add(objects)
        return session.commit()
    
    @staticmethod
    def select_all(model_name):
        return session.query(model_name).all()

    @staticmethod # 수정중.
    def set_query(model_name, **arg):
        return session.query(arg)
       
    @staticmethod # 수정중.
    def update(model_name, condtion):
        pass
    
    @staticmethod # 수정중.
    def delete(model_name, condtion):
        pass
    

"""
사용 예제.
db_uri = "mysql+pymysql://root:1234@127.0.0.1:3306/db_instagram"
my = MySQLconnector(db_uri)
session = my.connect_session()
my.craete_tables()   # 모든 모델에 관한 테이블을 생성
my.drop_tables()     # 모든 테이블을 지운다.

o_list1 = [User(1,1,1), User(11,1,1), User(111,1,1)]
my.insert(User(6,1,1)) # 단일 객체만 DB에 저장
my.insert(o_list1)     # 객체 리스트 DB에 저장

my.select(User, 'all') # 세션에 저장된 User의 모든 객체 정보를 반환
session.query(User).filter_by(user_id=6).first() <- 필터도 가능.


추가적으로 쿼리 사용예제
session = my.connect_session()
q = session.query(User.user_id, User.follower_count)
q.order_by("user_id").all()

"""