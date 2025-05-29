from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from decimal import Decimal
from models.user_models import BaseResponse

# 回访计划项
class FollowUpItem(BaseModel):
    date: date  # 回访日期
    type: str  # 回访类型：phone, visit, email
    status: str = "pending"  # 状态：pending, completed, cancelled
    notes: Optional[str] = None  # 备注
    completed_at: Optional[datetime] = None  # 完成时间

# 领养记录创建请求
class AdoptionRecordCreateRequest(BaseModel):
    application_id: str
    adoption_date: date
    adoption_fee: float = 0.00
    contract_signed: bool = False
    contract_url: Optional[str] = None
    microchip_id: Optional[str] = None
    return_policy: Optional[str] = None
    follow_up_schedule: Optional[List[FollowUpItem]] = None
    notes: Optional[str] = None

    @validator('adoption_fee')
    def validate_adoption_fee(cls, v):
        if v < 0:
            raise ValueError('领养费用不能为负数')
        return v

    @validator('adoption_date')
    def validate_adoption_date(cls, v):
        if v > date.today():
            raise ValueError('领养日期不能是未来日期')
        return v

# 领养记录更新请求
class AdoptionRecordUpdateRequest(BaseModel):
    adoption_date: Optional[date] = None
    adoption_fee: Optional[float] = None
    contract_signed: Optional[bool] = None
    contract_url: Optional[str] = None
    microchip_id: Optional[str] = None
    return_policy: Optional[str] = None
    follow_up_schedule: Optional[List[FollowUpItem]] = None
    notes: Optional[str] = None

    @validator('adoption_fee')
    def validate_adoption_fee(cls, v):
        if v is not None and v < 0:
            raise ValueError('领养费用不能为负数')
        return v

# 简化的申请信息
class SimpleApplicationInfo(BaseModel):
    application_id: str
    status: str
    created_at: str

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

# 简化的救助站信息
class SimpleShelterInfo(BaseModel):
    shelter_id: str
    name: str
    city: str
    phone: str

# 领养记录详情响应
class AdoptionRecordDetailResponse(BaseModel):
    record_id: str
    application: SimpleApplicationInfo
    animal: SimpleAnimalInfo
    adopter: SimpleUserInfo
    shelter: SimpleShelterInfo
    adoption_date: str
    adoption_fee: float
    contract_signed: bool
    contract_url: Optional[str]
    microchip_id: Optional[str]
    return_policy: Optional[str]
    follow_up_schedule: Optional[List[Dict[str, Any]]]
    notes: Optional[str]
    created_at: str
    updated_at: str

# 领养记录列表项
class AdoptionRecordListItem(BaseModel):
    record_id: str
    application_id: str
    animal_name: str
    animal_id: str
    animal_species: str
    adopter_name: str
    adopter_id: str
    shelter_name: str
    shelter_id: str
    adoption_date: str
    adoption_fee: float
    contract_signed: bool
    microchip_id: Optional[str]
    created_at: str

# 分页数据
class AdoptionRecordListData(BaseModel):
    items: List[AdoptionRecordListItem]
    total: int
    page: int
    size: int
    pages: int

# 领养统计数据
class AdoptionStatisticsData(BaseModel):
    total_adoptions: int = 0
    this_month_adoptions: int = 0
    this_year_adoptions: int = 0
    total_fees_collected: float = 0.0
    average_adoption_fee: float = 0.0
    by_species: Dict[str, int] = {}
    by_shelter: Dict[str, int] = {}
    by_month: Dict[str, int] = {}
    contract_signed_rate: float = 0.0
    microchip_rate: float = 0.0

# 回访统计数据
class FollowUpStatisticsData(BaseModel):
    total_follow_ups: int = 0
    pending_follow_ups: int = 0
    completed_follow_ups: int = 0
    overdue_follow_ups: int = 0
    upcoming_follow_ups: int = 0
    completion_rate: float = 0.0

# 响应模型
class AdoptionRecordCreateResponse(BaseResponse):
    data: Optional[AdoptionRecordDetailResponse] = None

class AdoptionRecordGetResponse(BaseResponse):
    data: Optional[AdoptionRecordDetailResponse] = None

class AdoptionRecordUpdateResponse(BaseResponse):
    data: Optional[AdoptionRecordDetailResponse] = None

class AdoptionRecordListResponse(BaseResponse):
    data: Optional[AdoptionRecordListData] = None

class AdoptionRecordDeleteResponse(BaseResponse):
    pass

class AdoptionStatisticsResponse(BaseResponse):
    data: Optional[AdoptionStatisticsData] = None

class FollowUpStatisticsResponse(BaseResponse):
    data: Optional[FollowUpStatisticsData] = None

# 合同上传响应
class ContractUploadResponse(BaseResponse):
    data: Optional[Dict[str, str]] = None  # {"contract_url": "..."} 