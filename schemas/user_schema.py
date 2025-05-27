from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Date, DateTime, Boolean, Text, func
from sqlalchemy import Enum, Column

# 创建基类
Base = declarative_base()

# 创建 User 模型
class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, index=True, comment='用户ID，使用UUID')
    username = Column(String(50), nullable=False, unique=True, comment='用户名')
    email = Column(String(100), nullable=False, unique=True, comment='邮箱地址')
    phone = Column(String(20), nullable=False, unique=True, comment='手机号码')
    password_hash = Column(String(255), nullable=False, comment='密码哈希值')
    user_type = Column(Enum('user', 'shelter_admin', 'system_admin', 'volunteer'), 
                      nullable=False, default='user', comment='用户类型')
    status = Column(Enum('active', 'inactive', 'banned'), 
                   nullable=False, default='active', comment='用户状态')
    name = Column(String(100), nullable=True, comment='真实姓名')
    gender = Column(Enum('male', 'female', 'other'), default='other', comment='性别')
    birthday = Column(Date, nullable=True, comment='生日')
    address = Column(String(500), nullable=True, comment='地址')
    avatar_url = Column(String(500), nullable=True, comment='头像URL')
    bio = Column(Text, nullable=True, comment='个人简介')
    pet_experience = Column(Enum('none', 'beginner', 'experienced', 'expert'), 
                           default='none', comment='养宠经验')
    occupation = Column(String(100), nullable=True, comment='职业')
    living_condition = Column(Text, nullable=True, comment='居住条件')
    family_members = Column(Integer, default=1, comment='家庭成员数量')
    has_other_pets = Column(Boolean, default=False, comment='是否有其他宠物')
    email_verified = Column(Boolean, default=False, comment='邮箱是否验证')
    phone_verified = Column(Boolean, default=False, comment='手机是否验证')
    last_login_at = Column(DateTime, nullable=True, comment='最后登录时间')
    created_at = Column(DateTime, nullable=False, 
                       default=func.current_timestamp(), comment='创建时间')
    updated_at = Column(DateTime, nullable=False, 
                       default=func.current_timestamp(), 
                       onupdate=func.current_timestamp(), comment='更新时间')

