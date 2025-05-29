from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, DECIMAL, Boolean, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class AdoptionRecord(Base):
    __tablename__ = "adoption_records"
    
    record_id = Column(String(36), primary_key=True, comment="记录ID")
    application_id = Column(String(36), ForeignKey("adoption_applications.application_id", ondelete="RESTRICT"), 
                           nullable=False, unique=True, comment="申请ID")
    animal_id = Column(String(36), ForeignKey("animals.animal_id", ondelete="RESTRICT"), 
                      nullable=False, comment="动物ID")
    adopter_id = Column(String(36), ForeignKey("users.user_id", ondelete="RESTRICT"), 
                       nullable=False, comment="领养人ID")
    shelter_id = Column(String(36), ForeignKey("shelters.shelter_id", ondelete="RESTRICT"), 
                       nullable=False, comment="救助站ID")
    adoption_date = Column(Date, nullable=False, comment="领养日期")
    adoption_fee = Column(DECIMAL(10, 2), default=0.00, comment="领养费用")
    contract_signed = Column(Boolean, default=False, comment="是否签署合同")
    contract_url = Column(String(500), comment="合同文件URL")
    microchip_id = Column(String(50), comment="芯片ID")
    return_policy = Column(Text, comment="退还政策")
    follow_up_schedule = Column(JSON, comment="回访计划")
    notes = Column(Text, comment="备注")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    application = relationship("AdoptionApplication", back_populates="adoption_record")
    animal = relationship("Animal", back_populates="adoption_records")
    adopter = relationship("User", back_populates="adoption_records", foreign_keys=[adopter_id])
    shelter = relationship("Shelter", back_populates="adoption_records")
    
    def __repr__(self):
        return f"<AdoptionRecord(record_id='{self.record_id}', animal_id='{self.animal_id}', adopter_id='{self.adopter_id}')>" 