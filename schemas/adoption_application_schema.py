from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Enum, Text, Boolean, DateTime, Date, DECIMAL, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class ApplicationStatusEnum(enum.Enum):
    pending = "pending"
    under_review = "under_review" 
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"
    completed = "completed"

class AdoptionApplication(Base):
    __tablename__ = "adoption_applications"
    
    application_id = Column(String(36), primary_key=True, comment="申请ID")
    animal_id = Column(String(36), ForeignKey("animals.animal_id", ondelete="RESTRICT"), nullable=False, comment="动物ID")
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False, comment="申请人ID")
    status = Column(Enum(ApplicationStatusEnum), nullable=False, default=ApplicationStatusEnum.pending, comment="申请状态")
    application_data = Column(JSON, nullable=False, comment="申请详细信息")
    reason = Column(Text, comment="申请理由")
    previous_experience = Column(Text, comment="以往经验")
    living_situation = Column(JSON, comment="居住情况")
    family_info = Column(JSON, comment="家庭信息")
    veterinarian_info = Column(JSON, comment="兽医信息")
    references = Column(JSON, comment="推荐人信息")
    home_visit_required = Column(Boolean, default=True, comment="是否需要家访")
    home_visit_date = Column(DateTime, comment="家访时间")
    home_visit_notes = Column(Text, comment="家访备注")
    interview_date = Column(DateTime, comment="面试时间")
    interview_notes = Column(Text, comment="面试备注")
    approval_notes = Column(Text, comment="审批备注")
    rejection_reason = Column(Text, comment="拒绝原因")
    reviewed_by = Column(String(36), ForeignKey("users.user_id", ondelete="SET NULL"), comment="审核人ID")
    reviewed_at = Column(DateTime, comment="审核时间")
    adoption_date = Column(Date, comment="领养日期")
    adoption_fee_paid = Column(DECIMAL(10, 2), default=0.00, comment="已支付领养费")
    follow_up_required = Column(Boolean, default=True, comment="是否需要回访")
    follow_up_date = Column(Date, comment="回访日期")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    animal = relationship("Animal", back_populates="adoption_applications", foreign_keys=[animal_id])
    user = relationship("User", back_populates="adoption_applications", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    
    def __repr__(self):
        return f"<AdoptionApplication(application_id='{self.application_id}', animal_id='{self.animal_id}', status='{self.status}')>" 