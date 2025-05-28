from fastapi import APIRouter, Query, Path, UploadFile, File, Form
from typing import Optional, List

from models import animal_models
from apis.controller import animal_controller

router = APIRouter()

# 获取动物列表
@router.get("/animals", response_model=animal_models.AnimalListResponse)
async def get_animals(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    species: Optional[str] = Query(None, description="物种筛选"),
    breed: Optional[str] = Query(None, description="品种筛选"),
    age_category: Optional[str] = Query(None, description="年龄段筛选"),
    gender: Optional[str] = Query(None, description="性别筛选"),
    size_filter: Optional[str] = Query(None, alias="size", description="体型筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    shelter_id: Optional[str] = Query(None, description="救助站ID"),
    city: Optional[str] = Query(None, description="城市筛选"),
    good_with_kids: Optional[bool] = Query(None, description="适合有孩子的家庭"),
    good_with_pets: Optional[bool] = Query(None, description="适合有其他宠物的家庭"),
    is_neutered: Optional[bool] = Query(None, description="是否绝育"),
    is_vaccinated: Optional[bool] = Query(None, description="是否接种疫苗"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    sort: str = Query("created_at", description="排序字段"),
    order: str = Query("desc", description="排序方向")
):
    return await animal_controller.get_animals_func(
        page=page,
        size=size,
        species=species,
        breed=breed,
        age_category=age_category,
        gender=gender,
        size_filter=size_filter,
        status=status,
        shelter_id=shelter_id,
        city=city,
        good_with_kids=good_with_kids,
        good_with_pets=good_with_pets,
        is_neutered=is_neutered,
        is_vaccinated=is_vaccinated,
        keyword=keyword,
        sort=sort,
        order=order
    )

# 获取动物详情
@router.get("/animals/{animal_id}", response_model=animal_models.AnimalGetResponse)
async def get_animal(animal_id: str = Path(..., description="动物ID")):
    return await animal_controller.get_animal_func(animal_id)

# 创建动物信息
@router.post("/animals", response_model=animal_models.AnimalCreateResponse)
async def create_animal(data: animal_models.AnimalCreateRequest):
    return await animal_controller.create_animal_func(data)

# 更新动物信息
@router.put("/animals/{animal_id}", response_model=animal_models.AnimalUpdateResponse)
async def update_animal(
    animal_id: str = Path(..., description="动物ID"),
    data: animal_models.AnimalUpdateRequest = None
):
    return await animal_controller.update_animal_func(animal_id, data)

# 删除动物信息
@router.delete("/animals/{animal_id}", response_model=animal_models.AnimalDeleteResponse)
async def delete_animal(animal_id: str = Path(..., description="动物ID")):
    return await animal_controller.delete_animal_func(animal_id)

# 上传动物图片
@router.post("/animals/{animal_id}/images", response_model=animal_models.AnimalImageUploadResponse)
async def upload_animal_images(
    animal_id: str = Path(..., description="动物ID"),
    images: List[UploadFile] = File(..., description="图片文件"),
    alt_text: Optional[List[str]] = Form(None, description="替代文本"),
    is_primary: Optional[List[bool]] = Form(None, description="是否为主图")
):
    return await animal_controller.upload_animal_images_func(animal_id, images, alt_text, is_primary)

# 获取推荐动物
@router.get("/animals/recommendations", response_model=animal_models.AnimalRecommendationsResponse)
async def get_recommendations(
    user_id: Optional[str] = Query(None, description="用户ID"),
    limit: int = Query(10, ge=1, le=50, description="推荐数量")
):
    return await animal_controller.get_recommendations_func(user_id, limit)
