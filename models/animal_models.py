from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Literal
from decimal import Decimal
from models.user_models import BaseResponse

# 动物创建请求模型
class AnimalCreateRequest(BaseModel):
    name: str                                                           # 动物名称
    species: Literal['cat', 'dog', 'rabbit', 'bird', 'other']         # 物种
    breed: Optional[str] = None                                         # 品种
    age: Optional[int] = None                                           # 年龄（月）
    age_category: Optional[Literal['baby', 'young', 'adult', 'senior']] = 'adult'  # 年龄段
    gender: Literal['male', 'female', 'unknown']                       # 性别
    size: Optional[Literal['small', 'medium', 'large', 'extra_large']] = 'medium'  # 体型
    weight: Optional[float] = None                                      # 体重（kg）
    color: Optional[str] = None                                         # 颜色
    description: Optional[str] = None                                   # 描述
    personality: Optional[List[str]] = None                             # 性格特点
    health_status: Optional[str] = None                                 # 健康状况
    medical_history: Optional[List[Dict[str, Any]]] = None             # 医疗历史
    is_neutered: Optional[bool] = False                                 # 是否绝育
    is_vaccinated: Optional[bool] = False                               # 是否接种疫苗
    vaccination_records: Optional[List[Dict[str, Any]]] = None         # 疫苗记录
    special_needs: Optional[str] = None                                 # 特殊需求
    good_with_kids: Optional[bool] = None                               # 是否适合有孩子的家庭
    good_with_pets: Optional[bool] = None                               # 是否适合有其他宠物的家庭
    energy_level: Optional[Literal['low', 'medium', 'high']] = 'medium' # 活跃度
    training_level: Optional[Literal['none', 'basic', 'intermediate', 'advanced']] = 'none'  # 训练程度
    shelter_id: str                                                     # 所属救助站ID
    location: Optional[str] = None                                      # 当前位置
    rescue_date: Optional[str] = None                                   # 救助日期 YYYY-MM-DD
    rescue_story: Optional[str] = None                                  # 救助故事
    adoption_fee: Optional[float] = 0.00                                # 领养费用

    @validator('age')
    def validate_age(cls, v):
        if v is not None and v < 0:
            raise ValueError('年龄不能为负数')
        return v

    @validator('weight')
    def validate_weight(cls, v):
        if v is not None and v <= 0:
            raise ValueError('体重必须大于0')
        return v

    @validator('adoption_fee')
    def validate_adoption_fee(cls, v):
        if v is not None and v < 0:
            raise ValueError('领养费用不能为负数')
        return v

# 动物更新请求模型
class AnimalUpdateRequest(BaseModel):
    name: Optional[str] = None
    species: Optional[Literal['cat', 'dog', 'rabbit', 'bird', 'other']] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    age_category: Optional[Literal['baby', 'young', 'adult', 'senior']] = None
    gender: Optional[Literal['male', 'female', 'unknown']] = None
    size: Optional[Literal['small', 'medium', 'large', 'extra_large']] = None
    weight: Optional[float] = None
    color: Optional[str] = None
    description: Optional[str] = None
    personality: Optional[List[str]] = None
    health_status: Optional[str] = None
    medical_history: Optional[List[Dict[str, Any]]] = None
    is_neutered: Optional[bool] = None
    is_vaccinated: Optional[bool] = None
    vaccination_records: Optional[List[Dict[str, Any]]] = None
    special_needs: Optional[str] = None
    good_with_kids: Optional[bool] = None
    good_with_pets: Optional[bool] = None
    energy_level: Optional[Literal['low', 'medium', 'high']] = None
    training_level: Optional[Literal['none', 'basic', 'intermediate', 'advanced']] = None
    status: Optional[Literal['available', 'pending', 'adopted', 'medical_hold', 'not_available']] = None
    location: Optional[str] = None
    rescue_date: Optional[str] = None
    rescue_story: Optional[str] = None
    adoption_fee: Optional[float] = None

# 救助站信息模型（简化版）
class ShelterInfo(BaseModel):
    shelter_id: str
    name: str
    city: str
    phone: str
    address: str

# 动物图片信息模型
class AnimalImageInfo(BaseModel):
    image_id: str
    url: str
    alt_text: Optional[str]
    is_primary: bool
    sort_order: int

# 动物列表项模型
class AnimalListItem(BaseModel):
    animal_id: str
    name: str
    species: str
    breed: Optional[str]
    age: Optional[int]
    age_category: str
    gender: str
    size: str
    weight: Optional[float]
    color: Optional[str]
    description: Optional[str]
    personality: Optional[List[str]]
    health_status: Optional[str]
    is_neutered: bool
    is_vaccinated: bool
    good_with_kids: Optional[bool]
    good_with_pets: Optional[bool]
    energy_level: str
    training_level: str
    shelter_id: str
    shelter_name: Optional[str]
    shelter_city: Optional[str]
    status: str
    rescue_date: Optional[str]
    adoption_fee: float
    images: Optional[List[str]]  # 只返回URL列表
    videos: Optional[List[str]]
    view_count: int
    favorite_count: int
    pending_applications: int = 0  # 待处理申请数量
    created_at: str

# 动物详细信息响应模型
class AnimalDetailResponse(BaseModel):
    animal_id: str
    name: str
    species: str
    breed: Optional[str]
    age: Optional[int]
    age_category: str
    gender: str
    size: str
    weight: Optional[float]
    color: Optional[str]
    description: Optional[str]
    personality: Optional[List[str]]
    health_status: Optional[str]
    medical_history: Optional[List[Dict[str, Any]]]
    is_neutered: bool
    is_vaccinated: bool
    vaccination_records: Optional[List[Dict[str, Any]]]
    special_needs: Optional[str]
    good_with_kids: Optional[bool]
    good_with_pets: Optional[bool]
    energy_level: str
    training_level: str
    shelter: ShelterInfo
    status: str
    location: Optional[str]
    rescue_date: Optional[str]
    rescue_story: Optional[str]
    adoption_fee: float
    images: Optional[List[AnimalImageInfo]]
    videos: Optional[List[str]]
    ai_features: Optional[Dict[str, Any]]
    view_count: int
    favorite_count: int
    pending_applications: int = 0
    created_at: str
    updated_at: str

# 分页数据模型
class AnimalListData(BaseModel):
    items: List[AnimalListItem]
    total: int
    page: int
    size: str
    pages: int

# 动物搜索筛选模型
class AnimalSearchFilters(BaseModel):
    species: Optional[str] = None
    age_category: Optional[str] = None
    gender: Optional[str] = None
    size: Optional[str] = None
    good_with_kids: Optional[bool] = None
    good_with_pets: Optional[bool] = None
    energy_level: Optional[str] = None
    is_neutered: Optional[bool] = None
    is_vaccinated: Optional[bool] = None
    shelter_id: Optional[str] = None
    status: Optional[str] = None
    min_fee: Optional[float] = None
    max_fee: Optional[float] = None

# 响应模型
class AnimalCreateResponse(BaseResponse):
    data: Optional[AnimalDetailResponse] = None

class AnimalGetResponse(BaseResponse):
    data: Optional[AnimalDetailResponse] = None

class AnimalUpdateResponse(BaseResponse):
    data: Optional[AnimalDetailResponse] = None

class AnimalListResponse(BaseResponse):
    data: Optional[AnimalListData] = None

class AnimalDeleteResponse(BaseResponse):
    pass

class AnimalRecommendationsResponse(BaseResponse):
    data: Optional[List[AnimalListItem]] = None

# 图片上传响应模型
class AnimalImageUploadResponse(BaseResponse):
    data: Optional[Dict[str, Any]] = None

# 动物统计信息模型
class AnimalStatisticsData(BaseModel):
    total_animals: int = 0
    available_animals: int = 0
    adopted_animals: int = 0
    pending_animals: int = 0
    by_species: Dict[str, int] = {}
    by_age_category: Dict[str, int] = {}
    by_size: Dict[str, int] = {}
    average_adoption_fee: float = 0.0
    total_views: int = 0
    total_favorites: int = 0

class AnimalStatisticsResponse(BaseResponse):
    data: Optional[AnimalStatisticsData] = None
