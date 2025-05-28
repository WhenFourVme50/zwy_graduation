from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, DateTime, JSON, Boolean, func
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from schemas.user_schema import Base

# 动物图片模型
class AnimalImage(Base):
    __tablename__ = "animal_images"

    image_id = Column(String(36), primary_key=True, index=True, comment='图片ID')
    animal_id = Column(String(36), ForeignKey('animals.animal_id', ondelete='CASCADE'), 
                      nullable=False, comment='动物ID')
    url = Column(String(500), nullable=False, comment='图片URL')
    alt_text = Column(String(200), nullable=True, comment='替代文本')
    is_primary = Column(Boolean, default=False, comment='是否为主图')
    sort_order = Column(Integer, default=0, comment='排序')
    ai_analysis = Column(JSON, nullable=True, comment='AI分析结果')
    created_at = Column(DateTime, nullable=False, 
                       default=func.current_timestamp(), comment='创建时间')

    # 关系
    animal = relationship("Animal", back_populates="animal_images")
