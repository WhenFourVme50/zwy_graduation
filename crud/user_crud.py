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
                user_pwd: str = None):
    db_user = db.query(User).filter(User.users_id == user_id).first()
    if db_user:
        db_user.users_name = user_name
        db_user.users_email = user_email
        db_user.users_phone = user_phone
        db_user.users_role = user_role
        db_user.users_status = user_status
        db_user.users_registeredAt = user_registeredAt
        db_user.users_lastLogin = user_lastLogin
        if user_pwd:
            db_user.users_pwd = user_pwd
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
            user_pwd: str = None):
    db_user = User(
        users_id = user_id,
        users_name = user_name,
        users_email = user_email,
        users_phone = user_phone,
        users_role = user_role,
        users_status = user_status,
        users_registeredAt = user_registeredAt,
        users_lastLogin = user_lastLogin,
        users_pwd = user_pwd
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
