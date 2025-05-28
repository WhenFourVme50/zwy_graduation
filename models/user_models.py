from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, Literal, Dict, Any
from fastapi import UploadFile, File, Form


class BaseResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None

# 新的用户注册请求模型
class UserRegisterRequest(BaseModel):
    username: str                                    # 用户名，3-50字符
    email: EmailStr                                  # 邮箱地址
    phone: str                                       # 手机号码
    password: str                                    # 密码，8-20字符
    name: str                                        # 真实姓名
    user_type: Literal["user", "shelter_admin", "volunteer"] = "user"  # 用户类型
    gender: Literal["male", "female", "other"] = "other"               # 性别
    birthday: Optional[str] = None                   # 生日 YYYY-MM-DD
    address: Optional[str] = None                    # 地址
    occupation: Optional[str] = None                 # 职业
    pet_experience: Literal["none", "beginner", "experienced", "expert"] = "none"  # 养宠经验

# 用户注册响应数据模型
class UserRegisterData(BaseModel):
    user_id: str
    username: str
    email: str
    user_type: str
    status: str
    created_at: datetime

# 用户注册响应模型
class UserRegisterResponse(BaseResponse):
    data: Optional[UserRegisterData] = None

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
    user_birthday : Optional[str] = Form(None)

class UserUpdateInfoResponse(BaseResponse):
    ...

# 用户详细信息响应模型
class UserDetailResponse(BaseModel):
    user_id: str
    username: str
    email: str
    phone: str
    name: Optional[str]
    gender: Optional[str]
    birthday: Optional[str]
    address: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    pet_experience: Optional[str]
    occupation: Optional[str]
    living_condition: Optional[str]
    family_members: Optional[int]
    has_other_pets: Optional[bool]
    user_type: str
    status: str
    created_at: str

# 获取用户信息响应模型
class GetUserResponse(BaseResponse):
    data: Optional[UserDetailResponse] = None

# 更新用户信息请求模型
class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    gender: Optional[Literal["male", "female", "other"]] = None
    birthday: Optional[str] = None
    address: Optional[str] = None
    bio: Optional[str] = None
    occupation: Optional[str] = None
    living_condition: Optional[str] = None
    family_members: Optional[int] = None
    has_other_pets: Optional[bool] = None

# 更新用户信息响应模型
class UpdateUserResponse(BaseResponse):
    data: Optional[UserDetailResponse] = None

# 上传头像响应模型
class UploadAvatarResponse(BaseResponse):
    data: Optional[dict] = None

# 用户统计信息数据模型
class UserStatisticsData(BaseModel):
    total_applications: int = 0           # 总申请数
    successful_adoptions: int = 0         # 成功领养数
    total_donations: int = 0              # 总捐赠次数
    total_donated_amount: float = 0.0     # 总捐赠金额
    activities_participated: int = 0       # 参与活动数
    total_volunteer_hours: float = 0.0    # 总志愿服务时长
    favorite_animals: int = 0             # 收藏动物数

# 用户统计信息响应模型
class UserStatisticsResponse(BaseResponse):
    data: Optional[UserStatisticsData] = None

# 统一登录请求模型
class UserLoginRequest(BaseModel):
    username: str                           # 用户名或邮箱
    password: str                          # 密码
    remember: Optional[bool] = False       # 是否记住登录

# 登录用户信息模型
class LoginUserInfo(BaseModel):
    user_id: str
    username: str
    email: str
    user_type: str
    avatar_url: Optional[str]

# 登录响应数据模型
class LoginResponseData(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    user: LoginUserInfo

# 统一登录响应模型
class LoginResponse(BaseResponse):
    data: Optional[LoginResponseData] = None

# Token刷新请求模型
class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Token刷新响应模型
class RefreshTokenResponse(BaseResponse):
    data: Optional[Dict[str, Any]] = None

# 登出请求模型
class LogoutRequest(BaseModel):
    access_token: str

# 登出响应模型
class LogoutResponse(BaseResponse):
    pass

