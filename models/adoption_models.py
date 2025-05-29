from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Literal
from decimal import Decimal
from models.user_models import BaseResponse

# 居住情况信息
class LivingSituationInfo(BaseModel):
    housing_type: str  # apartment, house, condo
    own_or_rent: str  # own, rent
    yard: bool = False  # 是否有院子
    other_pets: bool = False  # 是否有其他宠物
    children: bool = False  # 是否有孩子
    children_ages: Optional[List[int]] = None  # 孩子年龄

# 家庭信息
class FamilyInfo(BaseModel):
    family_size: int  # 家庭人口
    primary_caregiver: str  # 主要照顾者
    work_schedule: str  # 工作时间安排
    travel_frequency: str  # 出行频率

# 兽医信息
class VeterinarianInfo(BaseModel):
    clinic_name: str  # 诊所名称
    vet_name: str  # 兽医姓名
    phone: str  # 电话

# 推荐人信息
class ReferenceInfo(BaseModel):
    name: str  # 姓名
    relationship: str  # 关系
    phone: str  # 电话

# 领养申请提交请求
class AdoptionApplicationSubmitRequest(BaseModel):
    animal_id: str
    reason: str
    previous_experience: Optional[str] = None
    living_situation: LivingSituationInfo
    family_info: FamilyInfo
    veterinarian_info: Optional[VeterinarianInfo] = None
    references: Optional[List[ReferenceInfo]] = None

    @validator('reason')
    def validate_reason(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError('申请理由至少需要10个字符')
        return v.strip()

    @validator('living_situation')
    def validate_living_situation(cls, v):
        if v.children and not v.children_ages:
            raise ValueError('如果有孩子，请提供孩子年龄')
        return v

# 申请提交响应数据
class ApplicationSubmitData(BaseModel):
    application_id: str
    animal_id: str
    user_id: str
    status: str
    created_at: str

# 领养申请更新请求（管理员审核）
class AdoptionApplicationReviewRequest(BaseModel):
    status: Literal['under_review', 'approved', 'rejected']
    approval_notes: Optional[str] = None
    rejection_reason: Optional[str] = None
    home_visit_required: Optional[bool] = None
    interview_date: Optional[datetime] = None

# 面试和家访安排
class InterviewScheduleRequest(BaseModel):
    interview_date: datetime
    interview_notes: Optional[str] = None

class HomeVisitScheduleRequest(BaseModel):
    home_visit_date: datetime
    home_visit_notes: Optional[str] = None

# 简化的动物信息
class SimpleAnimalInfo(BaseModel):
    animal_id: str
    name: str
    species: str
    breed: Optional[str]
    age: Optional[int]
    size: str
    images: Optional[List[str]] = []

# 简化的用户信息
class SimpleUserInfo(BaseModel):
    user_id: str
    username: str
    name: Optional[str]
    email: str
    phone: str

# 领养申请详情响应
class AdoptionApplicationDetailResponse(BaseModel):
    application_id: str
    animal: SimpleAnimalInfo
    applicant: SimpleUserInfo
    status: str
    reason: str
    previous_experience: Optional[str]
    living_situation: Dict[str, Any]
    family_info: Dict[str, Any]
    veterinarian_info: Optional[Dict[str, Any]]
    references: Optional[List[Dict[str, Any]]]
    home_visit_required: bool
    home_visit_date: Optional[str]
    home_visit_notes: Optional[str]
    interview_date: Optional[str]
    interview_notes: Optional[str]
    approval_notes: Optional[str]
    rejection_reason: Optional[str]
    reviewer: Optional[SimpleUserInfo]
    reviewed_at: Optional[str]
    created_at: str
    updated_at: str

# 领养申请列表项
class AdoptionApplicationListItem(BaseModel):
    application_id: str
    animal_name: str
    animal_id: str
    animal_species: str
    applicant_name: str
    applicant_id: str
    status: str
    reason: str
    home_visit_required: bool
    home_visit_date: Optional[str]
    interview_date: Optional[str]
    created_at: str

# 分页数据
class AdoptionApplicationListData(BaseModel):
    items: List[AdoptionApplicationListItem]
    total: int
    page: int
    size: int
    pages: int

# 响应模型
class AdoptionApplicationSubmitResponse(BaseResponse):
    data: Optional[ApplicationSubmitData] = None

class AdoptionApplicationDetailGetResponse(BaseResponse):
    data: Optional[AdoptionApplicationDetailResponse] = None

class AdoptionApplicationListResponse(BaseResponse):
    data: Optional[AdoptionApplicationListData] = None

class AdoptionApplicationReviewResponse(BaseResponse):
    data: Optional[AdoptionApplicationDetailResponse] = None 