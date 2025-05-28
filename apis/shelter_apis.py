from fastapi import APIRouter, Query, Path
from typing import Optional

from models import shelter_models
from apis.controller import shelter_controller

router = APIRouter()

# 获取救助站列表
@router.get("/shelters", response_model=shelter_models.ShelterListResponse)
async def get_shelters(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    city: Optional[str] = Query(None, description="城市筛选"),
    province: Optional[str] = Query(None, description="省份筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    keyword: Optional[str] = Query(None, description="关键词搜索")
):
    return await shelter_controller.get_shelters_func(
        page=page,
        size=size,
        city=city,
        province=province,
        status=status,
        keyword=keyword
    )

# 获取救助站详情
@router.get("/shelters/{shelter_id}", response_model=shelter_models.ShelterGetResponse)
async def get_shelter(shelter_id: str = Path(..., description="救助站ID")):
    return await shelter_controller.get_shelter_func(shelter_id)

# 创建救助站
@router.post("/shelters", response_model=shelter_models.ShelterCreateResponse)
async def create_shelter(data: shelter_models.ShelterCreateRequest):
    return await shelter_controller.create_shelter_func(data)

# 更新救助站信息
@router.put("/shelters/{shelter_id}", response_model=shelter_models.ShelterUpdateResponse)
async def update_shelter(
    shelter_id: str = Path(..., description="救助站ID"),
    data: shelter_models.ShelterUpdateRequest = None
):
    return await shelter_controller.update_shelter_func(shelter_id, data)

# 获取救助站统计信息
@router.get("/shelters/{shelter_id}/statistics", response_model=shelter_models.ShelterStatisticsResponse)
async def get_shelter_statistics(shelter_id: str = Path(..., description="救助站ID")):
    return await shelter_controller.get_shelter_statistics_func(shelter_id)
