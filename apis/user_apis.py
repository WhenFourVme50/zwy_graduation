from fastapi import APIRouter, UploadFile, File, HTTPException, Path
from fastapi import Form

from typing import Annotated

from models import user_models

from apis.controller import user_controller

router = APIRouter()

# 新的用户注册接口
@router.post("/auth/register", response_model=user_models.UserRegisterResponse)
async def user_register(data: user_models.UserRegisterRequest):
    return await user_controller.user_register_func(data)

# 获取用户信息
@router.get("/users/{user_id}", response_model=user_models.GetUserResponse)
async def get_user(user_id: str = Path(..., description="用户ID")):
    return await user_controller.get_user_func(user_id)

# 更新用户信息
@router.put("/users/{user_id}", response_model=user_models.UpdateUserResponse)
async def update_user(
    user_id: str = Path(..., description="用户ID"),
    data: user_models.UpdateUserRequest = None
):
    return await user_controller.update_user_func(user_id, data)

# 上传用户头像
@router.post("/users/{user_id}/avatar", response_model=user_models.UploadAvatarResponse)
async def upload_avatar(
    user_id: str = Path(..., description="用户ID"),
    avatar: UploadFile = File(..., description="头像文件")
):
    return await user_controller.upload_avatar_func(user_id, avatar)

# 获取用户统计信息
@router.get("/users/{user_id}/statistics", response_model=user_models.UserStatisticsResponse)
async def get_user_statistics(user_id: str = Path(..., description="用户ID")):
    return await user_controller.get_user_statistics_func(user_id)

# 用户邮箱登录接口
@router.post("/login_by_email", response_model=user_models.UserLoginResponse)
async def user_login_by_email(data: user_models.UserLoginByEmailRequest):
    return await user_controller.user_login_by_email_func(data)

# 用户手机号登录接口
@router.post("/login_by_phone", response_model=user_models.UserLoginResponse)
async def user_login_by_id(data: user_models.UserLoginByPhoneRequest):
    return await user_controller.user_login_by_phone_func(data)

# 原有用户注册按钮（保持兼容性）
@router.post("/logup", response_model=user_models.UserLogupResponse)
async def user_logup(data: user_models.UserLogupRequest):
    return await user_controller.user_logup_func(data)

# 用户修改基本型信息
@router.post("/update_info", response_model=user_models.UserUpdateInfoResponse)
async def user_update_info(data: Annotated[user_models.UserUpdateInfoRequest, Form()]):
    return await user_controller.user_update_info_func(data)