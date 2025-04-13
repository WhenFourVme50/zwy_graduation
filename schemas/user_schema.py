from sqlalchemy import create_engine, Column, Integer, String, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum

# 创建基类
Base = declarative_base()

# 创建 User 模型
class User(Base):
    __tablename__ = "users"

    users_id = Column(String(20), primary_key=True, index=True)
    users_name = Column(String(100), nullable=False)
    users_email = Column(String(255), nullable=False, unique=True)
    users_phone = Column(String(20), nullable=False, unique=True)
    users_role = Column(Enum('admin','users'), nullable=False)
    users_status = Column(Enum('active', 'inactive', name="user_status"), default='active', nullable=False)
    users_registeredAt = Column(Date, nullable=False)
    users_lastLogin = Column(Date, nullable=False)
    users_pwd = Column(String,nullable=False)
