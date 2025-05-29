from fastapi import APIRouter, Query, Path, Depends
from typing import Optional

from models import adoption_models
from apis.controller import adoption_controller
from utils.auth_utils import get_current_user

router = APIRouter()

# 提交领养申请
@router.post("/applications", response_model=adoption_models.AdoptionApplicationSubmitResponse)
async def submit_adoption_application(
    data: adoption_models.AdoptionApplicationSubmitRequest,
    current_user = Depends(get_current_user)
):
    return await adoption_controller.submit_adoption_application_func(data, current_user.user_id)

# 获取领养申请详情
@router.get("/applications/{application_id}", response_model=adoption_models.AdoptionApplicationDetailGetResponse)
async def get_adoption_application(
    application_id: str = Path(..., description="申请ID")
):
    return await adoption_controller.get_adoption_application_func(application_id)

# 获取领养申请列表
@router.get("/applications", response_model=adoption_models.AdoptionApplicationListResponse)
async def get_adoption_applications(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="申请状态"),
    animal_id: Optional[str] = Query(None, description="动物ID"),
    user_id: Optional[str] = Query(None, description="用户ID"),
    species: Optional[str] = Query(None, description="动物种类"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    sort: str = Query("created_at", description="排序字段"),
    order: str = Query("desc", description="排序方向")
):
    return await adoption_controller.get_adoption_applications_func(
        page, size, status, animal_id, user_id, species, keyword, sort, order
    )

# 审核领养申请
@router.put("/applications/{application_id}/review", response_model=adoption_models.AdoptionApplicationReviewResponse)
async def review_adoption_application(
    application_id: str = Path(..., description="申请ID"),
    data: adoption_models.AdoptionApplicationReviewRequest = None,
    current_user = Depends(get_current_user)
):
    # 验证权限（只有管理员可以审核）
    if current_user.user_type not in ['shelter_admin', 'system_admin']:
        return adoption_models.AdoptionApplicationReviewResponse(
            code=403,
            message="无权限操作"
        )
    return await adoption_controller.review_adoption_application_func(application_id, data, current_user.user_id)

# 取消领养申请
@router.put("/applications/{application_id}/cancel", response_model=adoption_models.AdoptionApplicationReviewResponse)
async def cancel_adoption_application(
    application_id: str = Path(..., description="申请ID"),
    current_user = Depends(get_current_user)
):
    return await adoption_controller.cancel_adoption_application_func(application_id, current_user.user_id)

# 获取用户的申请列表
@router.get("/my-applications", response_model=adoption_models.AdoptionApplicationListResponse)
async def get_my_adoption_applications(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="申请状态"),
    current_user = Depends(get_current_user)
):
    return await adoption_controller.get_adoption_applications_func(
        page, size, status, None, current_user.user_id, None, None, "created_at", "desc"
    ) 