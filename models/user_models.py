from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from fastapi import UploadFile, File, Form


class BaseResponse(BaseModel):
    status: int = None
    message: str = None

# 用户邮箱登录请求模型
class UserLoginByEmailRequest(BaseModel):
    user_email: EmailStr
    user_pwd: str

# 用户手机号登录请求模型
class UserLoginByPhoneRequest(BaseModel):
    user_phone: str
    user_pwd: str

# 用户注册请求模型
class UserLogupRequest(BaseModel):
    user_name: str
    user_email: EmailStr
    user_phone: str
    user_pwd: str

# 用户通过邮箱更新密码请求模型
class UserUpdatePwdByEmailRequest(BaseModel):
    user_email : str
    auth_code : str

# 用户基本信息响应模型
class UserInfoResponse(BaseModel):
    user_id: str = None
    user_name: str = None
    user_email: EmailStr = None
    user_status: str = None
    user_phone: str = None
    user_role: str = None
    user_registeredAt: datetime = None
    user_lastLogin : datetime = None

# 用户登录响应模型
class UserLoginResponse(BaseResponse):
    is_allow : bool = False,
    user_info_response : UserInfoResponse = UserInfoResponse()

# 用户注册响应模型
class UserLogupResponse(BaseResponse):
    is_allow : bool = False


# 用户修改基本信息请求模型
class UserUpdateInfoRequest(BaseModel):
    user_phone : Optional[str] = Form(None)
    user_name : Optional[str] = Form(None)
    user_avatar : Optional[UploadFile] = File(None)
    user_gender : Optional[str] = Form(None)
    user_exp : Optional[str] = Form(None)
    user_job : Optional[str] = Form(None)
    user_intro : Optional[str] = Form(None)

class UserUpdateInfoResponse(BaseResponse):
    ...

