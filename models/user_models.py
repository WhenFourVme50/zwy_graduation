from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict

class UserLoginByEmailRequest(BaseModel):
    user_email: EmailStr
    user_pwd: str

class UserLoginByPhoneRequest(BaseModel):
    user_phone: str
    user_pwd: str

class UserLogupRequest(BaseModel):
    user_name: str
    user_email: EmailStr
    user_phone: str
    user_pwd: str

class UserUpdatePwdByEmailRequest(BaseModel):
    user_email : str
    auth_code : str

class UserInfoResponse(BaseModel):
    user_id: str = None
    user_name: str = None
    user_email: EmailStr = None
    user_status: str = None
    user_phone: str = None
    user_role: str = None
    user_registeredAt: datetime = None
    user_lastLogin : datetime = None

class UserLoginResponse(BaseModel):
    is_allow : bool = False,
    status : int = None,
    message : str = None
    user_info_response : UserInfoResponse = UserInfoResponse()

class UserLogupResponse(BaseModel):
    is_allow : bool = False
    status : int = None
    message : str = None