from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Literal
from models.user_models import BaseResponse

# 救助站创建请求模型
class ShelterCreateRequest(BaseModel):
    name: str                                         # 救助站名称
    description: Optional[str] = None                 # 救助站描述
    address: str                                      # 地址
    city: str                                         # 城市
    province: str                                     # 省份
    postal_code: Optional[str] = None                 # 邮政编码
    phone: str                                        # 联系电话
    email: Optional[EmailStr] = None                  # 邮箱
    website: Optional[str] = None                     # 官网
    license_number: Optional[str] = None              # 许可证号
    capacity: Optional[int] = 0                       # 容量
    established_date: Optional[str] = None            # 成立日期 YYYY-MM-DD
    operating_hours: Optional[Dict[str, str]] = None  # 营业时间
    services: Optional[List[str]] = None              # 提供的服务

# 救助站更新请求模型
class ShelterUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    license_number: Optional[str] = None
    capacity: Optional[int] = None
    established_date: Optional[str] = None
    operating_hours: Optional[Dict[str, str]] = None
    services: Optional[List[str]] = None

# 救助站列表项模型（扩展版）
class ShelterListItem(BaseModel):
    shelter_id: str
    name: str
    description: Optional[str]
    address: str
    city: str
    province: str
    phone: str
    email: Optional[str]
    website: Optional[str]
    capacity: int
    current_animals: int
    status: str
    logo_url: Optional[str]
    images: Optional[List[str]]
    operating_hours: Optional[Dict[str, str]]
    services: Optional[List[str]]
    total_animals: int = 0      # 总动物数量
    available_animals: int = 0  # 可领养动物数量
    adopted_animals: int = 0    # 已领养动物数量

# 救助站详细信息响应模型
class ShelterDetailResponse(BaseModel):
    shelter_id: str
    name: str
    description: Optional[str]
    address: str
    city: str
    province: str
    postal_code: Optional[str]
    phone: str
    email: Optional[str]
    website: Optional[str]
    license_number: Optional[str]
    capacity: int
    current_animals: int
    established_date: Optional[str]
    status: str
    logo_url: Optional[str]
    images: Optional[List[str]]
    operating_hours: Optional[Dict[str, str]]
    services: Optional[List[str]]
    created_at: str

# 分页数据模型
class ShelterListData(BaseModel):
    items: List[ShelterListItem]
    total: int
    page: int
    size: int
    pages: int

# 救助站统计信息模型
class ShelterStatisticsData(BaseModel):
    total_animals: int = 0           # 总动物数量
    available_animals: int = 0       # 可领养动物数量
    adopted_animals: int = 0         # 已领养动物数量
    pending_applications: int = 0    # 待处理申请
    successful_adoptions: int = 0    # 成功领养数
    total_donations: int = 0         # 总捐赠次数
    total_donated_amount: float = 0.0 # 总捐赠金额
    volunteer_count: int = 0         # 志愿者数量
    monthly_expenses: float = 0.0    # 月度支出
    rescue_count: int = 0            # 救助数量

# 救助站管理员信息模型
class ShelterAdminInfo(BaseModel):
    id: str
    user_id: str
    username: str
    name: Optional[str]
    email: str
    role: str
    permissions: Optional[Dict[str, Any]]
    status: str
    created_at: str

# 添加管理员请求模型
class AddShelterAdminRequest(BaseModel):
    user_id: str
    role: Literal["owner", "admin", "staff"] = "staff"
    permissions: Optional[Dict[str, Any]] = None

# 更新管理员请求模型
class UpdateShelterAdminRequest(BaseModel):
    role: Optional[Literal["owner", "admin", "staff"]] = None
    permissions: Optional[Dict[str, Any]] = None
    status: Optional[Literal["active", "inactive"]] = None

# 响应模型
class ShelterCreateResponse(BaseResponse):
    data: Optional[ShelterDetailResponse] = None

class ShelterGetResponse(BaseResponse):
    data: Optional[ShelterDetailResponse] = None

class ShelterUpdateResponse(BaseResponse):
    data: Optional[ShelterDetailResponse] = None

class ShelterListResponse(BaseResponse):
    data: Optional[ShelterListData] = None

class ShelterStatisticsResponse(BaseResponse):
    data: Optional[ShelterStatisticsData] = None

class ShelterAdminListResponse(BaseResponse):
    data: Optional[List[ShelterAdminInfo]] = None

class ShelterAdminResponse(BaseResponse):
    data: Optional[ShelterAdminInfo] = None

class UploadShelterLogoResponse(BaseResponse):
    data: Optional[Dict[str, str]] = None

class UploadShelterImagesResponse(BaseResponse):
    data: Optional[Dict[str, List[str]]] = None
