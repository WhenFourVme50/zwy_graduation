from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Literal
from models.user_models import BaseResponse

# 回访记录创建请求
class FollowUpRecordCreateRequest(BaseModel):
    adoption_record_id: str
    follow_up_date: date
    follow_up_type: Literal['phone', 'visit', 'video', 'email']
    animal_condition: Literal['excellent', 'good', 'fair', 'poor', 'concerning']
    living_condition: Optional[str] = None
    health_status: Optional[str] = None
    behavioral_notes: Optional[str] = None
    concerns: Optional[str] = None
    recommendations: Optional[str] = None
    next_follow_up_date: Optional[date] = None
    images: Optional[List[str]] = None  # 图片URL列表
    satisfaction_score: Optional[int] = None

    @validator('follow_up_date')
    def validate_follow_up_date(cls, v):
        if v > date.today():
            raise ValueError('回访日期不能是未来日期')
        return v

    @validator('satisfaction_score')
    def validate_satisfaction_score(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError('满意度评分必须在1-10之间')
        return v

    @validator('next_follow_up_date')
    def validate_next_follow_up_date(cls, v):
        if v is not None and v <= date.today():
            raise ValueError('下次回访日期必须是未来日期')
        return v

# 回访记录更新请求
class FollowUpRecordUpdateRequest(BaseModel):
    follow_up_date: Optional[date] = None
    follow_up_type: Optional[Literal['phone', 'visit', 'video', 'email']] = None
    animal_condition: Optional[Literal['excellent', 'good', 'fair', 'poor', 'concerning']] = None
    living_condition: Optional[str] = None
    health_status: Optional[str] = None
    behavioral_notes: Optional[str] = None
    concerns: Optional[str] = None
    recommendations: Optional[str] = None
    next_follow_up_date: Optional[date] = None
    images: Optional[List[str]] = None
    satisfaction_score: Optional[int] = None

    @validator('satisfaction_score')
    def validate_satisfaction_score(cls, v):
        if v is not None and (v < 1 or v > 10):
            raise ValueError('满意度评分必须在1-10之间')
        return v

# 简化的领养记录信息
class SimpleAdoptionRecordInfo(BaseModel):
    record_id: str
    animal_name: str
    animal_id: str
    adopter_name: str
    adopter_id: str
    adoption_date: str

# 简化的回访人信息
class SimpleConductorInfo(BaseModel):
    user_id: str
    username: str
    name: Optional[str]
    user_type: str

# 回访记录详情响应
class FollowUpRecordDetailResponse(BaseModel):
    follow_up_id: str
    adoption_record: SimpleAdoptionRecordInfo
    follow_up_date: str
    follow_up_type: str
    conductor: SimpleConductorInfo
    animal_condition: str
    living_condition: Optional[str]
    health_status: Optional[str]
    behavioral_notes: Optional[str]
    concerns: Optional[str]
    recommendations: Optional[str]
    next_follow_up_date: Optional[str]
    images: Optional[List[str]]
    satisfaction_score: Optional[int]
    created_at: str

# 回访记录列表项
class FollowUpRecordListItem(BaseModel):
    follow_up_id: str
    adoption_record_id: str
    animal_name: str
    adopter_name: str
    follow_up_date: str
    follow_up_type: str
    animal_condition: str
    conductor_name: str
    satisfaction_score: Optional[int]
    next_follow_up_date: Optional[str]
    has_concerns: bool  # 是否有关注点
    created_at: str

# 分页数据
class FollowUpRecordListData(BaseModel):
    items: List[FollowUpRecordListItem]
    total: int
    page: int
    size: int
    pages: int

# 回访统计数据
class FollowUpStatisticsData(BaseModel):
    total_follow_ups: int = 0
    this_month_follow_ups: int = 0
    this_year_follow_ups: int = 0
    by_type: Dict[str, int] = {}
    by_condition: Dict[str, int] = {}
    by_conductor: Dict[str, int] = {}
    average_satisfaction_score: float = 0.0
    concerning_cases: int = 0
    overdue_follow_ups: int = 0
    upcoming_follow_ups: int = 0
    completion_rate: float = 0.0

# 动物健康趋势数据
class AnimalHealthTrendData(BaseModel):
    animal_id: str
    animal_name: str
    follow_up_history: List[Dict[str, Any]]  # 回访历史记录
    condition_trend: str  # improving, stable, declining
    latest_condition: str
    concerns_count: int
    satisfaction_trend: float

# 回访提醒数据
class FollowUpReminderData(BaseModel):
    adoption_record_id: str
    animal_name: str
    adopter_name: str
    last_follow_up_date: Optional[str]
    next_follow_up_date: str
    days_overdue: int = 0
    priority: Literal['high', 'medium', 'low']

# 响应模型
class FollowUpRecordCreateResponse(BaseResponse):
    data: Optional[FollowUpRecordDetailResponse] = None

class FollowUpRecordGetResponse(BaseResponse):
    data: Optional[FollowUpRecordDetailResponse] = None

class FollowUpRecordUpdateResponse(BaseResponse):
    data: Optional[FollowUpRecordDetailResponse] = None

class FollowUpRecordListResponse(BaseResponse):
    data: Optional[FollowUpRecordListData] = None

class FollowUpRecordDeleteResponse(BaseResponse):
    pass

class FollowUpStatisticsResponse(BaseResponse):
    data: Optional[FollowUpStatisticsData] = None

class AnimalHealthTrendResponse(BaseResponse):
    data: Optional[List[AnimalHealthTrendData]] = None

class FollowUpRemindersResponse(BaseResponse):
    data: Optional[List[FollowUpReminderData]] = None

# 图片上传响应
class FollowUpImageUploadResponse(BaseResponse):
    data: Optional[Dict[str, List[str]]] = None  # {"image_urls": [...]} 