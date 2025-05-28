from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from models.user_models import BaseResponse

# 动物图片创建请求模型
class AnimalImageCreateRequest(BaseModel):
    animal_id: str                                    # 动物ID
    url: str                                          # 图片URL
    alt_text: Optional[str] = None                    # 替代文本
    is_primary: Optional[bool] = False                # 是否为主图
    sort_order: Optional[int] = 0                     # 排序
    ai_analysis: Optional[Dict[str, Any]] = None      # AI分析结果

    @validator('url')
    def validate_url(cls, v):
        if not v or not v.strip():
            raise ValueError('图片URL不能为空')
        return v.strip()

    @validator('sort_order')
    def validate_sort_order(cls, v):
        if v is not None and v < 0:
            raise ValueError('排序值不能为负数')
        return v

# 动物图片更新请求模型
class AnimalImageUpdateRequest(BaseModel):
    url: Optional[str] = None
    alt_text: Optional[str] = None
    is_primary: Optional[bool] = None
    sort_order: Optional[int] = None
    ai_analysis: Optional[Dict[str, Any]] = None

# 批量上传图片请求模型
class AnimalImageBatchUploadRequest(BaseModel):
    animal_id: str
    images: List[Dict[str, Any]]  # 包含url, alt_text, sort_order等信息

# 动物图片响应模型
class AnimalImageResponse(BaseModel):
    image_id: str
    animal_id: str
    url: str
    alt_text: Optional[str]
    is_primary: bool
    sort_order: int
    ai_analysis: Optional[Dict[str, Any]]
    created_at: str

# 动物图片列表响应模型
class AnimalImageListResponse(BaseResponse):
    data: Optional[List[AnimalImageResponse]] = None

# 单个动物图片响应模型
class AnimalImageSingleResponse(BaseResponse):
    data: Optional[AnimalImageResponse] = None

# 批量操作响应模型
class AnimalImageBatchResponse(BaseResponse):
    data: Optional[Dict[str, Any]] = None

# 图片统计信息模型
class AnimalImageStatistics(BaseModel):
    total_images: int = 0
    images_with_ai: int = 0
    primary_images: int = 0
    animals_with_images: int = 0
    average_images_per_animal: float = 0.0

class AnimalImageStatisticsResponse(BaseResponse):
    data: Optional[AnimalImageStatistics] = None

# 设置主图请求模型
class SetPrimaryImageRequest(BaseModel):
    image_id: str

# 重新排序请求模型
class ReorderImagesRequest(BaseModel):
    image_orders: List[Dict[str, int]]  # [{"image_id": "xxx", "sort_order": 1}, ...]

# AI分析结果更新请求模型
class UpdateAIAnalysisRequest(BaseModel):
    ai_analysis: Dict[str, Any] 