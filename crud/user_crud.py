import datetime

from sqlalchemy.orm import Session

from schemas.user_schema import User


# 获取用户通过ID
def get_user_by_phone(db: Session, user_phone: str = None):
    return db.query(User).filter(User.users_phone == user_phone).first()


# 获取用户通过邮箱
def get_user_by_email(db: Session, user_email: str = None):
    return db.query(User).filter(User.users_email == user_email).first()


# 更新用户信息
def update_user(db: Session,
                user_id: str = None,
                user_name: str = None,
                user_email: str = None,
                user_phone: str = None,
                user_role: str = None,
                user_status: str = None,
                user_registeredAt: str = None,
                user_lastLogin: str = None,
                user_pwd: str = None,
                user_avatar: bytes  = None,
                user_gender: str = None,
                user_exp: str = None,
                user_job: str = None,
                user_intro: str = None,
                user_birthday: str = None):

    db_user = db.query(User).filter(User.users_id == user_id).first()
    if db_user:
        db_user.users_name = user_name
        db_user.users_email = user_email
        db_user.users_phone = user_phone
        db_user.users_role = user_role
        db_user.users_status = user_status
        db_user.users_registeredAt = user_registeredAt
        db_user.users_lastLogin = user_lastLogin
        db_user.users_avatar = user_avatar
        db_user.users_gender = user_gender
        db_user.users_exp = user_exp
        db_user.users_job = user_job
        db_user.users_intro = user_intro
        db_user.users_pwd = user_pwd
        db_user.users_birthday = user_birthday
        db.commit()
        db.refresh(db_user)
    return db_user

def add_user(db: Session,
             user_id: str = None,
            user_name: str = None,
            user_email: str = None,
            user_phone: str = None,
            user_role: str = None,
            user_status: str = None,
            user_registeredAt: datetime.datetime = None,
            user_lastLogin: datetime.datetime = None,
            user_pwd: str = None,
            user_avatar: bytes = None,
            user_gender: str = "其他",
            user_exp: str = "暂无",
            user_job: str = "暂无",
            user_intro: str = " ",
            user_birthday: str = '2025-01-01'):

    db_user = User(
        users_id = user_id,
        users_name = user_name,
        users_email = user_email,
        users_phone = user_phone,
        users_role = user_role,
        users_status = user_status,
        users_registeredAt = user_registeredAt,
        users_lastLogin = user_lastLogin,
        users_pwd = user_pwd,
        users_avatar = user_avatar,
        users_gender = user_gender,
        users_exp = user_exp,
        users_job = user_job,
        users_intro = user_intro,
        users_birthday = user_birthday
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 删除用户
def delete_user(db: Session, user_id: str = None):
    db_user = db.query(User).filter(User.users_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
