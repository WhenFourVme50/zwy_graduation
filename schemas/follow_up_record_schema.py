from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Enum, Text, JSON, Integer, DateTime, ForeignKey
from datetime import datetime
import enum

Base = declarative_base()

class FollowUpTypeEnum(enum.Enum):
    phone = "phone"
    visit = "visit"
    video = "video"
    email = "email"

class AnimalConditionEnum(enum.Enum):
    excellent = "excellent"
    good = "good"
    fair = "fair"
    poor = "poor"
    concerning = "concerning"

class FollowUpRecord(Base):
    __tablename__ = "follow_up_records"
    
    follow_up_id = Column(String(36), primary_key=True, comment="回访ID")
    adoption_record_id = Column(String(36), ForeignKey("adoption_records.record_id", ondelete="CASCADE"), 
                               nullable=False, comment="领养记录ID")
    follow_up_date = Column(Date, nullable=False, comment="回访日期")
    follow_up_type = Column(Enum(FollowUpTypeEnum), nullable=False, comment="回访方式")
    conducted_by = Column(String(36), ForeignKey("users.user_id", ondelete="RESTRICT"), 
                         nullable=False, comment="回访人ID")
    animal_condition = Column(Enum(AnimalConditionEnum), nullable=False, comment="动物状况")
    living_condition = Column(Text, comment="生活条件")
    health_status = Column(Text, comment="健康状况")
    behavioral_notes = Column(Text, comment="行为备注")
    concerns = Column(Text, comment="关注点")
    recommendations = Column(Text, comment="建议")
    next_follow_up_date = Column(Date, comment="下次回访日期")
    images = Column(JSON, comment="回访图片")
    satisfaction_score = Column(Integer, comment="满意度评分(1-10)")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    
    def __repr__(self):
        return f"<FollowUpRecord(follow_up_id='{self.follow_up_id}', adoption_record_id='{self.adoption_record_id}', follow_up_date='{self.follow_up_date}')>" 