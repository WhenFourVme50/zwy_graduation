import uuid
from datetime import datetime, date
from sqlalchemy.orm import Session
from schemas.user_schema import User

# 获取用户通过手机号
def get_user_by_phone(db: Session, user_phone: str = None):
    return db.query(User).filter(User.phone == user_phone).first()

# 获取用户通过邮箱
def get_user_by_email(db: Session, user_email: str = None):
    return db.query(User).filter(User.email == user_email).first()

# 获取用户通过用户名
def get_user_by_username(db: Session, username: str = None):
    return db.query(User).filter(User.username == username).first()

# 获取用户通过ID
def get_user_by_id(db: Session, user_id: str = None):
    return db.query(User).filter(User.user_id == user_id).first()

# 创建新用户
def create_user(db: Session,
                username: str,
                email: str,
                phone: str,
                password_hash: str,
                name: str = None,
                user_type: str = "user",
                gender: str = "other",
                birthday: date = None,
                address: str = None,
                occupation: str = None,
                pet_experience: str = "none"):
    
    user_id = str(uuid.uuid4())
    
    db_user = User(
        user_id=user_id,
        username=username,
        email=email,
        phone=phone,
        password_hash=password_hash,
        user_type=user_type,
        status="active",
        name=name,
        gender=gender,
        birthday=birthday,
        address=address,
        occupation=occupation,
        pet_experience=pet_experience,
        email_verified=False,
        phone_verified=False
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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
                user_avatar: bytes = None,
                user_gender: str = None,
                user_exp: str = None,
                user_job: str = None,
                user_intro: str = None,
                user_birthday: str = None):

    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        # 适配新字段名
        if user_name: db_user.name = user_name
        if user_email: db_user.email = user_email
        if user_phone: db_user.phone = user_phone
        if user_role: db_user.user_type = user_role
        if user_status: db_user.status = user_status
        if user_lastLogin: db_user.last_login_at = user_lastLogin
        if user_avatar: db_user.avatar_url = user_avatar
        if user_gender: db_user.gender = user_gender
        if user_exp: db_user.pet_experience = user_exp
        if user_job: db_user.occupation = user_job
        if user_intro: db_user.bio = user_intro
        if user_birthday: db_user.birthday = user_birthday
        
        db.commit()
        db.refresh(db_user)
    return db_user

# 保留原有的add_user函数以保持兼容性
def add_user(db: Session,
             user_id: str = None,
             user_name: str = None,
             user_email: str = None,
             user_phone: str = None,
             user_role: str = None,
             user_status: str = None,
             user_registeredAt: datetime = None,
             user_lastLogin: datetime = None,
             user_pwd: str = None,
             user_avatar: bytes = None,
             user_gender: str = "其他",
             user_exp: str = "暂无",
             user_job: str = "暂无",
             user_intro: str = " ",
             user_birthday: str = '2025-01-01'):

    # 映射到新的字段名
    db_user = User(
        user_id=user_id or str(uuid.uuid4()),
        username=user_name,
        email=user_email,
        phone=user_phone,
        password_hash=user_pwd,
        user_type=user_role,
        status=user_status,
        name=user_name,
        gender="other" if user_gender == "其他" else user_gender,
        birthday=user_birthday,
        occupation=user_job,
        pet_experience=user_exp,
        bio=user_intro,
        email_verified=False,
        phone_verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 删除用户
def delete_user(db: Session, user_id: str = None):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# 更新用户信息（新版本）
def update_user_info(db: Session, user_id: str, update_data: dict):
    """
    更新用户信息
    """
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        return None
    
    # 处理生日格式
    if 'birthday' in update_data and update_data['birthday']:
        try:
            update_data['birthday'] = datetime.strptime(update_data['birthday'], "%Y-%m-%d").date()
        except ValueError:
            # 如果日期格式错误，移除该字段
            del update_data['birthday']
    
    # 更新字段
    for field, value in update_data.items():
        if hasattr(db_user, field) and value is not None:
            setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# 更新用户头像URL
def update_user_avatar(db: Session, user_id: str, avatar_url: str):
    """
    更新用户头像URL
    """
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db_user.avatar_url = avatar_url
        db.commit()
        db.refresh(db_user)
    return db_user

# 获取用户统计信息（模拟数据，实际需要根据业务表计算）
def get_user_statistics(db: Session, user_id: str):
    """
    获取用户统计信息
    注意：这里返回模拟数据，实际应该从相关业务表中统计
    """
    # 检查用户是否存在
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    
    # 这里应该根据实际的业务表进行统计查询
    # 例如：adoption_applications, donations, activities, favorites 等表
    
    # 模拟统计数据
    statistics = {
        "total_applications": 5,
        "successful_adoptions": 2,
        "total_donations": 10,
        "total_donated_amount": 1500.00,
        "activities_participated": 8,
        "total_volunteer_hours": 24.5,
        "favorite_animals": 15
    }
    
    return statistics
