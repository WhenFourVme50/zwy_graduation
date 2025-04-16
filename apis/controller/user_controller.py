from typing import Dict
from models import user_models
from db import session
from crud import user_crud

from utils import random_utils,time_utils

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
            user_info_response=user_info_response  # 返回空的用户信息
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
            user_intro = " "
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
                user_lastLogin=user_info.users_lastLogin
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
