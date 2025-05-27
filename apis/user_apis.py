from fastapi import APIRouter
from fastapi import Form

from typing import Annotated

from models import user_models

from apis.controller import user_controller

router = APIRouter()

# 新的用户注册接口
@router.post("/auth/register", response_model=user_models.UserRegisterResponse)
async def user_register(data: user_models.UserRegisterRequest):
    return await user_controller.user_register_func(data)

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