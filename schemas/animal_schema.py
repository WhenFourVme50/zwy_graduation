from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Text, Integer, Date, DateTime, JSON, Boolean, DECIMAL, func
from sqlalchemy import Enum, Column, ForeignKey
from sqlalchemy.orm import relationship

from schemas.user_schema import Base

# 动物模型
class Animal(Base):
    __tablename__ = "animals"

    animal_id = Column(String(36), primary_key=True, index=True, comment='动物ID')
    name = Column(String(100), nullable=False, comment='动物名称')
    species = Column(Enum('cat', 'dog', 'rabbit', 'bird', 'other'), 
                    nullable=False, comment='物种')
    breed = Column(String(100), nullable=True, comment='品种')
    age = Column(Integer, nullable=True, comment='年龄（月）')
    age_category = Column(Enum('baby', 'young', 'adult', 'senior'), 
                         default='adult', comment='年龄段')
    gender = Column(Enum('male', 'female', 'unknown'), 
                   nullable=False, comment='性别')
    size = Column(Enum('small', 'medium', 'large', 'extra_large'), 
                 default='medium', comment='体型')
    weight = Column(DECIMAL(5, 2), nullable=True, comment='体重（kg）')
    color = Column(String(100), nullable=True, comment='颜色')
    description = Column(Text, nullable=True, comment='描述')
    personality = Column(JSON, nullable=True, comment='性格特点')
    health_status = Column(Text, nullable=True, comment='健康状况')
    medical_history = Column(JSON, nullable=True, comment='医疗历史')
    is_neutered = Column(Boolean, default=False, comment='是否绝育')
    is_vaccinated = Column(Boolean, default=False, comment='是否接种疫苗')
    vaccination_records = Column(JSON, nullable=True, comment='疫苗记录')
    special_needs = Column(Text, nullable=True, comment='特殊需求')
    good_with_kids = Column(Boolean, nullable=True, comment='是否适合有孩子的家庭')
    good_with_pets = Column(Boolean, nullable=True, comment='是否适合有其他宠物的家庭')
    energy_level = Column(Enum('low', 'medium', 'high'), 
                         default='medium', comment='活跃度')
    training_level = Column(Enum('none', 'basic', 'intermediate', 'advanced'), 
                           default='none', comment='训练程度')
    shelter_id = Column(String(36), ForeignKey('shelters.shelter_id', ondelete='RESTRICT'), 
                       nullable=False, comment='所属救助站ID')
    status = Column(Enum('available', 'pending', 'adopted', 'medical_hold', 'not_available'), 
                   nullable=False, default='available', comment='状态')
    location = Column(String(200), nullable=True, comment='当前位置')
    rescue_date = Column(Date, nullable=True, comment='救助日期')
    rescue_story = Column(Text, nullable=True, comment='救助故事')
    adoption_fee = Column(DECIMAL(10, 2), default=0.00, comment='领养费用')
    images = Column(JSON, nullable=True, comment='图片URLs')
    videos = Column(JSON, nullable=True, comment='视频URLs')
    ai_features = Column(JSON, nullable=True, comment='AI提取的特征数据')
    view_count = Column(Integer, default=0, comment='浏览次数')
    favorite_count = Column(Integer, default=0, comment='收藏次数')
    created_at = Column(DateTime, nullable=False, 
                       default=func.current_timestamp(), comment='创建时间')
    updated_at = Column(DateTime, nullable=False, 
                       default=func.current_timestamp(), 
                       onupdate=func.current_timestamp(), comment='更新时间')

    # 关系
    shelter = relationship("Shelter", back_populates="animals")
    animal_images = relationship("AnimalImage", back_populates="animal", cascade="all, delete-orphan")
