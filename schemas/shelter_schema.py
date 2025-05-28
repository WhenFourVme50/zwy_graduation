##

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Text, Integer, Date, DateTime, JSON, func
from sqlalchemy import Enum, Column, ForeignKey
from sqlalchemy.orm import relationship

from schemas.user_schema import Base

# 救助站模型
class Shelter(Base):
    __tablename__ = "shelters"

    shelter_id = Column(String(36), primary_key=True, index=True, comment='救助站ID')
    name = Column(String(200), nullable=False, comment='救助站名称')
    description = Column(Text, nullable=True, comment='救助站描述')
    address = Column(String(500), nullable=False, comment='地址')
    city = Column(String(100), nullable=False, comment='城市')
    province = Column(String(100), nullable=False, comment='省份')
    postal_code = Column(String(20), nullable=True, comment='邮政编码')
    phone = Column(String(20), nullable=False, comment='联系电话')
    email = Column(String(100), nullable=True, comment='邮箱')
    website = Column(String(500), nullable=True, comment='官网')
    license_number = Column(String(100), nullable=True, comment='许可证号')
    capacity = Column(Integer, default=0, comment='容量')
    current_animals = Column(Integer, default=0, comment='当前动物数量')
    established_date = Column(Date, nullable=True, comment='成立日期')
    status = Column(Enum('active', 'inactive', 'pending'), 
                   nullable=False, default='pending', comment='状态')
    logo_url = Column(String(500), nullable=True, comment='Logo URL')
    images = Column(JSON, nullable=True, comment='图片URLs')
    operating_hours = Column(JSON, nullable=True, comment='营业时间')
    services = Column(JSON, nullable=True, comment='提供的服务')
    created_at = Column(DateTime, nullable=False, 
                       default=func.current_timestamp(), comment='创建时间')
    updated_at = Column(DateTime, nullable=False, 
                       default=func.current_timestamp(), 
                       onupdate=func.current_timestamp(), comment='更新时间')

    # 关系
    admins = relationship("ShelterAdmin", back_populates="shelter", cascade="all, delete-orphan")


# 救助站管理员关联模型
class ShelterAdmin(Base):
    __tablename__ = "shelter_admins"

    id = Column(String(36), primary_key=True, index=True, comment='ID')
    shelter_id = Column(String(36), ForeignKey('shelters.shelter_id', ondelete='CASCADE'), 
                       nullable=False, comment='救助站ID')
    user_id = Column(String(36), ForeignKey('users.user_id', ondelete='CASCADE'), 
                    nullable=False, comment='用户ID')
    role = Column(Enum('owner', 'admin', 'staff'), 
                 nullable=False, default='staff', comment='角色')
    permissions = Column(JSON, nullable=True, comment='权限配置')
    status = Column(Enum('active', 'inactive'), 
                   nullable=False, default='active', comment='状态')
    created_at = Column(DateTime, nullable=False, 
                       default=func.current_timestamp(), comment='创建时间')
    updated_at = Column(DateTime, nullable=False, 
                       default=func.current_timestamp(), 
                       onupdate=func.current_timestamp(), comment='更新时间')

    # 关系
    shelter = relationship("Shelter", back_populates="admins")
    user = relationship("User")  # 需要在 user_schema.py 中导入此模型
