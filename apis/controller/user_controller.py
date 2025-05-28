from typing import Dict
from datetime import datetime, date
import hashlib
from models import user_models
from db import session
from crud import user_crud

from utils import random_utils, time_utils

import os
import uuid
from fastapi import UploadFile

async def user_register_func(data: user_models.UserRegisterRequest):
    """
    新的用户注册方法
    :param data: 用户注册数据模型
    :return: 注册响应
    """
    db_session = session.get_session()
    
    try:
        # 检查用户名是否已存在
        existing_user = user_crud.get_user_by_username(db_session, data.username)
        if existing_user:
            return user_models.UserRegisterResponse(
                code=400,
                message="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        existing_email = user_crud.get_user_by_email(db_session, data.email)
        if existing_email:
            return user_models.UserRegisterResponse(
                code=400,
                message="邮箱已被注册"
            )
        
        # 检查手机号是否已存在
        existing_phone = user_crud.get_user_by_phone(db_session, data.phone)
        if existing_phone:
            return user_models.UserRegisterResponse(
                code=400,
                message="手机号已被注册"
            )
        
        # 密码加密
        password_hash = hashlib.sha256(data.password.encode()).hexdigest()
        
        # 处理生日格式
        birthday = None
        if data.birthday:
            try:
                birthday = datetime.strptime(data.birthday, "%Y-%m-%d").date()
            except ValueError:
                return user_models.UserRegisterResponse(
                    code=400,
                    message="生日格式错误，请使用YYYY-MM-DD格式"
                )
        
        # 创建用户
        new_user = user_crud.create_user(
            db=db_session,
            username=data.username,
            email=data.email,
            phone=data.phone,
            password_hash=password_hash,
            name=data.name,
            user_type=data.user_type,
            gender=data.gender,
            birthday=birthday,
            address=data.address,
            occupation=data.occupation,
            pet_experience=data.pet_experience
        )
        
        # 构造响应数据
        response_data = user_models.UserRegisterData(
            user_id=new_user.user_id,
            username=new_user.username,
            email=new_user.email,
            user_type=new_user.user_type,
            status=new_user.status,
            created_at=new_user.created_at
        )
        
        return user_models.UserRegisterResponse(
            code=200,
            message="注册成功",
            data=response_data
        )
        
    except Exception as e:
        print(f"Registration error: {e}")
        return user_models.UserRegisterResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def user_login_by_phone_func(data: user_models.UserLoginByPhoneRequest):
    """
    用户手机号登录方法
    :param data: 用户手机号登录数据模型
    :return: 除密码外的用户信息字典
    """
    # 建立数据库会话
    db_session = session.get_session()

    # 提取数据并进行数据检验
    try:
        user_info = user_crud.get_user_by_phone(db_session, data.user_phone)

        if user_info:
            # 检查密码是否匹配（需要适配新的字段名）
            if user_info.password_hash == data.user_pwd:
                # 创建UserInfoResponse对象
                user_info_response = user_models.UserInfoResponse(
                    user_id=user_info.user_id,
                    user_name=user_info.username,
                    user_email=user_info.email,
                    user_phone=user_info.phone,
                    user_role=user_info.user_type,
                    user_registeredAt=user_info.created_at,
                    user_lastLogin=user_info.last_login_at,
                    user_status=user_info.status,
                )

                # 返回登录响应
                return user_models.UserLoginResponse(
                    is_allow=True,
                    status=200,
                    message="登录成功",
                    user_info_response=user_info_response
                )

            # 如果密码不匹配，返回密码错误
            user_info_response = user_models.UserInfoResponse()
            return user_models.UserLoginResponse(
                is_allow=False,
                status=3102,
                message="密码错误",
                user_info_response=user_info_response
            )

        # 如果用户不存在，返回用户不存在
        user_info_response = user_models.UserInfoResponse()
        return user_models.UserLoginResponse(
            is_allow=False,
            status=3101,
            message="用户不存在",
            user_info_response=user_info_response
        )

    except Exception as e:
        # 捕获异常并记录日志
        user_info_response = user_models.UserInfoResponse()
        return user_models.UserLoginResponse(
            is_allow=False,
            status=4100,
            message="服务器发生错误",
            user_info_response=user_info_response
        )

async def user_login_by_email_func(data: user_models.UserLoginByEmailRequest):
    """
    用户邮箱登录方法
    :param data: 用户邮箱登录数据模型
    :return: 用户信息字典
    """
    # 获取数据库会话
    db_session = session.get_session()

    try:
        # 从数据库获取用户信息
        user_info = user_crud.get_user_by_email(db_session, data.user_email)

        if user_info:
            # 检查密码是否匹配
            if user_info.users_pwd == data.user_pwd:
                # 创建UserInfoResponse对象
                user_info_response = user_models.UserInfoResponse(
                    user_id=user_info.users_id,
                    user_name=user_info.users_name,
                    user_email=user_info.users_email,
                    user_phone=user_info.users_phone,
                    user_role=user_info.users_role,
                    user_registeredAt=user_info.users_registeredAt,
                    user_lastLogin=user_info.users_lastLogin,
                    user_status=user_info.users_status,
                )

                # 返回登录响应
                return user_models.UserLoginResponse(
                    is_allow=True,
                    status=200,
                    message="登录成功",
                    user_info_response=user_info_response  # 返回用户信息
                )

            # 如果密码不匹配，返回密码错误
            user_info_response = user_models.UserInfoResponse()  # 仍然返回空的用户信息
            return user_models.UserLoginResponse(
                is_allow=False,  # 登录失败
                status=3102,  # 密码错误状态码
                message="密码错误",
                user_info_response=user_info_response  # 返回空的用户信息
            )

        # 如果用户不存在，返回用户不存在
        user_info_response = user_models.UserInfoResponse()  # 仍然返回空的用户信息
        return user_models.UserLoginResponse(
            is_allow=False,  # 登录失败
            status=3101,  # 用户不存在状态码
            message="用户不存在",
            user_info_response=user_info_response  # 返回空的用户信息
        )

    except Exception as e:
        # 捕获异常并记录日志
        user_info_response = user_models.UserInfoResponse()  # 仍然返回空的用户信息
        return user_models.UserLoginResponse(
            is_allow=False,  # 登录失败
            status=4100,  # 服务器错误状态码
            message="服务器发生错误",
            user_info=user_info_response  # 返回空的用户信息
        )

async def user_logup_func(data: user_models.UserLogupRequest):
    """
    用户注册方法
    :param data:
    :return:
    """
    # 获取数据库会话
    db_session = session.get_session()

    try:
        # 检查用户是否已经存在
        user_info = user_crud.get_user_by_phone(db_session, data.user_phone)
        if user_info:
            return user_models.UserLogupResponse(
                is_allow = False,
                status = 3103,
                message = "注册手机号或邮箱已存在"
            )

        # 向数据库中添加用户
        user_crud.add_user(
            db = db_session,
            user_id = random_utils.get_user_id(),
            user_name = data.user_name,
            user_email = data.user_email,
            user_phone = data.user_phone,
            user_role = "1",
            user_status = "active",
            user_registeredAt = time_utils.get_current_date(),
            user_lastLogin = time_utils.get_current_date(),
            user_pwd = data.user_pwd,
            user_gender = "其他",
            user_avatar = None,
            user_exp = "暂无养宠经验",
            user_job = "暂无",
            user_intro = " ",
            user_birthday = '2025-01-01'

        )
        return user_models.UserLogupResponse(
            is_allow = True,
            status = 200,
            message = "注册成功"
        )

    except Exception as e:
        # 捕获异常并记录日志
        print(e)
        return user_models.UserLoginResponse(
            is_allow=False,
            status=4100,
            message="服务器发生错误",
        )

async def user_update_info_func(data: user_models.UserUpdateInfoRequest):
    """
    用户更新信息方法
    :param data:
    :return:
    """
    # 建立数据库会话
    db_session = session.get_session()

    # 验证用户是否存在
    user_info = user_crud.get_user_by_phone(db_session, data.user_phone)
    try:
        print(user_info.users_id)
        if user_info:
            user_avatar_data =await data.user_avatar.read()  # 读取文件内容
            print(user_avatar_data)

            # 修改用户信息
            user_crud.update_user(
                db=db_session,
                user_id=user_info.users_id,
                user_name=data.user_name or user_info.users_name,
                user_phone=user_info.users_phone,
                user_email=user_info.users_email,
                user_role=user_info.users_role,
                user_status=user_info.users_status,
                user_pwd=user_info.users_pwd,
                user_avatar=user_avatar_data or user_info.users_avatar,  # 使用文件内容（二进制数据）
                user_gender=data.user_gender or user_info.users_gender,
                user_intro=data.user_intro or user_info.users_intro,
                user_job=data.user_job or user_info.users_job,
                user_exp=data.user_exp or user_info.users_exp,
                user_registeredAt=user_info.users_registeredAt,
                user_lastLogin=user_info.users_lastLogin,
                user_birthday = user_info.users_birthday
            )
            return user_models.UserUpdateInfoResponse(
                status=200,
                message="更新成功"
            )

        return user_models.UserUpdateInfoResponse(
            status=200,
            message="更新失败，用户不存在"
        )
    except Exception as e:
        return user_models.UserUpdateInfoResponse(
            status=4200,
            message="服务器发生错误"
        )

async def get_user_func(user_id: str):
    """
    获取用户信息
    """
    db_session = session.get_session()
    
    try:
        # 获取用户信息
        user = user_crud.get_user_by_id(db_session, user_id)
        if not user:
            return user_models.GetUserResponse(
                code=404,
                message="用户不存在"
            )
        
        # 构造响应数据
        user_data = user_models.UserDetailResponse(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            name=user.name,
            gender=user.gender,
            birthday=user.birthday.strftime("%Y-%m-%d") if user.birthday else None,
            address=user.address,
            avatar_url=user.avatar_url,
            bio=user.bio,
            pet_experience=user.pet_experience,
            occupation=user.occupation,
            living_condition=user.living_condition,
            family_members=user.family_members,
            has_other_pets=user.has_other_pets,
            user_type=user.user_type,
            status=user.status,
            created_at=user.created_at.isoformat() if user.created_at else None
        )
        
        return user_models.GetUserResponse(
            code=200,
            message="获取成功",
            data=user_data
        )
        
    except Exception as e:
        print(f"Get user error: {e}")
        return user_models.GetUserResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def update_user_func(user_id: str, data: user_models.UpdateUserRequest):
    """
    更新用户信息
    """
    db_session = session.get_session()
    
    try:
        # 检查用户是否存在
        user = user_crud.get_user_by_id(db_session, user_id)
        if not user:
            return user_models.UpdateUserResponse(
                code=404,
                message="用户不存在"
            )
        
        # 准备更新数据
        update_data = {}
        if data.name is not None:
            update_data['name'] = data.name
        if data.gender is not None:
            update_data['gender'] = data.gender
        if data.birthday is not None:
            update_data['birthday'] = data.birthday
        if data.address is not None:
            update_data['address'] = data.address
        if data.bio is not None:
            update_data['bio'] = data.bio
        if data.occupation is not None:
            update_data['occupation'] = data.occupation
        if data.living_condition is not None:
            update_data['living_condition'] = data.living_condition
        if data.family_members is not None:
            update_data['family_members'] = data.family_members
        if data.has_other_pets is not None:
            update_data['has_other_pets'] = data.has_other_pets
        
        # 更新用户信息
        updated_user = user_crud.update_user_info(db_session, user_id, update_data)
        if not updated_user:
            return user_models.UpdateUserResponse(
                code=400,
                message="更新失败"
            )
        
        # 构造响应数据
        user_data = user_models.UserDetailResponse(
            user_id=updated_user.user_id,
            username=updated_user.username,
            email=updated_user.email,
            phone=updated_user.phone,
            name=updated_user.name,
            gender=updated_user.gender,
            birthday=updated_user.birthday.strftime("%Y-%m-%d") if updated_user.birthday else None,
            address=updated_user.address,
            avatar_url=updated_user.avatar_url,
            bio=updated_user.bio,
            pet_experience=updated_user.pet_experience,
            occupation=updated_user.occupation,
            living_condition=updated_user.living_condition,
            family_members=updated_user.family_members,
            has_other_pets=updated_user.has_other_pets,
            user_type=updated_user.user_type,
            status=updated_user.status,
            created_at=updated_user.created_at.isoformat() if updated_user.created_at else None
        )
        
        return user_models.UpdateUserResponse(
            code=200,
            message="更新成功",
            data=user_data
        )
        
    except Exception as e:
        print(f"Update user error: {e}")
        return user_models.UpdateUserResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def upload_avatar_func(user_id: str, avatar: UploadFile):
    """
    上传用户头像
    """
    db_session = session.get_session()
    
    try:
        # 检查用户是否存在
        user = user_crud.get_user_by_id(db_session, user_id)
        if not user:
            return user_models.UploadAvatarResponse(
                code=404,
                message="用户不存在"
            )
        
        # 检查文件类型
        if not avatar.content_type.startswith('image/'):
            return user_models.UploadAvatarResponse(
                code=400,
                message="只能上传图片文件"
            )
        
        # 检查文件大小（限制5MB）
        if avatar.size > 5 * 1024 * 1024:
            return user_models.UploadAvatarResponse(
                code=400,
                message="文件大小不能超过5MB"
            )
        
        # 生成文件名
        file_extension = avatar.filename.split('.')[-1] if '.' in avatar.filename else 'jpg'
        filename = f"{user_id}_{uuid.uuid4().hex}.{file_extension}"
        
        # 创建上传目录
        upload_dir = "static/avatars"
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as buffer:
            content = await avatar.read()
            buffer.write(content)
        
        # 构造头像URL
        avatar_url = f"/static/avatars/{filename}"
        
        # 更新数据库
        user_crud.update_user_avatar(db_session, user_id, avatar_url)
        
        return user_models.UploadAvatarResponse(
            code=200,
            message="头像上传成功",
            data={"avatar_url": avatar_url}
        )
        
    except Exception as e:
        print(f"Upload avatar error: {e}")
        return user_models.UploadAvatarResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def get_user_statistics_func(user_id: str):
    """
    获取用户统计信息
    """
    db_session = session.get_session()
    
    try:
        # 获取统计信息
        statistics = user_crud.get_user_statistics(db_session, user_id)
        if statistics is None:
            return user_models.UserStatisticsResponse(
                code=404,
                message="用户不存在"
            )
        
        # 构造响应数据
        stats_data = user_models.UserStatisticsData(**statistics)
        
        return user_models.UserStatisticsResponse(
            code=200,
            message="获取成功",
            data=stats_data
        )
        
    except Exception as e:
        print(f"Get statistics error: {e}")
        return user_models.UserStatisticsResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()
