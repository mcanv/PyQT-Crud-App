from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import os
import datetime

load_dotenv()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
engine = create_engine(f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4", encoding='utf-8', echo=True)
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()