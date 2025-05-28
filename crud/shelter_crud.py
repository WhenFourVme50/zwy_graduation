import uuid
import math
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from schemas.shelter_schema import Shelter, ShelterAdmin
from schemas.user_schema import User

# 获取救助站列表（带分页和筛选）
def get_shelters_with_pagination(db: Session, 
                                page: int = 1,
                                size: int = 10,
                                city: str = None, 
                                province: str = None, 
                                status: str = None,
                                keyword: str = None):
    """
    获取救助站列表（带分页和筛选）
    """
    query = db.query(Shelter)
    
    # 筛选条件
    if city:
        query = query.filter(Shelter.city == city)
    if province:
        query = query.filter(Shelter.province == province)
    if status:
        query = query.filter(Shelter.status == status)
    if keyword:
        query = query.filter(
            or_(
                Shelter.name.contains(keyword),
                Shelter.description.contains(keyword),
                Shelter.address.contains(keyword)
            )
        )
    
    # 获取总数
    total = query.count()
    
    # 计算分页
    skip = (page - 1) * size
    pages = math.ceil(total / size) if total > 0 else 1
    
    # 获取分页数据
    items = query.offset(skip).limit(size).all()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }

# 创建救助站
def create_shelter(db: Session, **shelter_data):
    """
    创建新救助站
    """
    shelter_id = str(uuid.uuid4())
    
    # 处理成立日期
    if shelter_data.get('established_date'):
        try:
            shelter_data['established_date'] = datetime.strptime(
                shelter_data['established_date'], "%Y-%m-%d"
            ).date()
        except ValueError:
            shelter_data['established_date'] = None
    
    db_shelter = Shelter(
        shelter_id=shelter_id,
        **shelter_data
    )
    
    db.add(db_shelter)
    db.commit()
    db.refresh(db_shelter)
    return db_shelter

# 根据ID获取救助站
def get_shelter_by_id(db: Session, shelter_id: str):
    """
    根据ID获取救助站
    """
    return db.query(Shelter).filter(Shelter.shelter_id == shelter_id).first()

# 获取救助站列表
def get_shelters(db: Session, 
                city: str = None, 
                province: str = None, 
                status: str = None,
                skip: int = 0, 
                limit: int = 100):
    """
    获取救助站列表
    """
    query = db.query(Shelter)
    
    if city:
        query = query.filter(Shelter.city == city)
    if province:
        query = query.filter(Shelter.province == province)
    if status:
        query = query.filter(Shelter.status == status)
    
    return query.offset(skip).limit(limit).all()

# 搜索救助站
def search_shelters(db: Session, 
                   keyword: str = None,
                   city: str = None,
                   province: str = None,
                   skip: int = 0,
                   limit: int = 100):
    """
    搜索救助站
    """
    query = db.query(Shelter)
    
    if keyword:
        query = query.filter(
            or_(
                Shelter.name.contains(keyword),
                Shelter.description.contains(keyword),
                Shelter.address.contains(keyword)
            )
        )
    
    if city:
        query = query.filter(Shelter.city == city)
    if province:
        query = query.filter(Shelter.province == province)
    
    return query.offset(skip).limit(limit).all()

# 更新救助站信息
def update_shelter(db: Session, shelter_id: str, update_data: dict):
    """
    更新救助站信息
    """
    db_shelter = db.query(Shelter).filter(Shelter.shelter_id == shelter_id).first()
    if not db_shelter:
        return None
    
    # 处理成立日期
    if 'established_date' in update_data and update_data['established_date']:
        try:
            update_data['established_date'] = datetime.strptime(
                update_data['established_date'], "%Y-%m-%d"
            ).date()
        except ValueError:
            del update_data['established_date']
    
    # 更新字段
    for field, value in update_data.items():
        if hasattr(db_shelter, field) and value is not None:
            setattr(db_shelter, field, value)
    
    db.commit()
    db.refresh(db_shelter)
    return db_shelter

# 删除救助站
def delete_shelter(db: Session, shelter_id: str):
    """
    删除救助站
    """
    db_shelter = db.query(Shelter).filter(Shelter.shelter_id == shelter_id).first()
    if db_shelter:
        db.delete(db_shelter)
        db.commit()
    return db_shelter

# 获取救助站统计信息
def get_shelter_statistics(db: Session, shelter_id: str):
    """
    获取救助站统计信息
    注意：这里返回模拟数据，实际应该从相关业务表中统计
    """
    # 检查救助站是否存在
    shelter = db.query(Shelter).filter(Shelter.shelter_id == shelter_id).first()
    if not shelter:
        return None
    
    # 这里应该根据实际的业务表进行统计查询
    # 例如：animals, adoption_applications, donations 等表
    
    # 模拟统计数据
    statistics = {
        "total_animals": shelter.current_animals + 65,  # 总动物数量
        "available_animals": shelter.current_animals,    # 可领养动物数量
        "adopted_animals": 65,                          # 已领养动物数量
        "pending_applications": 12,                     # 待处理申请
        "successful_adoptions": 65,                     # 成功领养数
        "total_donations": 45,                          # 总捐赠次数
        "total_donated_amount": 15800.50,               # 总捐赠金额
        "volunteer_count": 25,                          # 志愿者数量
        "monthly_expenses": 8500.00,                    # 月度支出
        "rescue_count": 89                              # 救助数量
    }
    
    return statistics

# 获取救助站扩展信息（包含统计数据）
def get_shelter_with_stats(db: Session, shelter):
    """
    获取救助站扩展信息（包含统计数据）
    """
    # 这里应该查询实际的动物表来获取真实统计
    # 目前使用模拟数据
    total_animals = shelter.current_animals + 65
    available_animals = shelter.current_animals
    adopted_animals = 65
    
    return {
        "shelter_id": shelter.shelter_id,
        "name": shelter.name,
        "description": shelter.description,
        "address": shelter.address,
        "city": shelter.city,
        "province": shelter.province,
        "phone": shelter.phone,
        "email": shelter.email,
        "website": shelter.website,
        "capacity": shelter.capacity,
        "current_animals": shelter.current_animals,
        "status": shelter.status,
        "logo_url": shelter.logo_url,
        "images": shelter.images or [],
        "operating_hours": shelter.operating_hours or {},
        "services": shelter.services or [],
        "total_animals": total_animals,
        "available_animals": available_animals,
        "adopted_animals": adopted_animals
    }

# 更新救助站logo
def update_shelter_logo(db: Session, shelter_id: str, logo_url: str):
    """
    更新救助站logo
    """
    db_shelter = db.query(Shelter).filter(Shelter.shelter_id == shelter_id).first()
    if db_shelter:
        db_shelter.logo_url = logo_url
        db.commit()
        db.refresh(db_shelter)
    return db_shelter

# 更新救助站图片
def update_shelter_images(db: Session, shelter_id: str, images: list):
    """
    更新救助站图片
    """
    db_shelter = db.query(Shelter).filter(Shelter.shelter_id == shelter_id).first()
    if db_shelter:
        db_shelter.images = images
        db.commit()
        db.refresh(db_shelter)
    return db_shelter

# 添加救助站管理员
def add_shelter_admin(db: Session, shelter_id: str, user_id: str, role: str = "staff", permissions: dict = None):
    """
    添加救助站管理员
    """
    # 检查是否已经是管理员
    existing = db.query(ShelterAdmin).filter(
        and_(ShelterAdmin.shelter_id == shelter_id, ShelterAdmin.user_id == user_id)
    ).first()
    
    if existing:
        return None  # 已经是管理员
    
    admin_id = str(uuid.uuid4())
    db_admin = ShelterAdmin(
        id=admin_id,
        shelter_id=shelter_id,
        user_id=user_id,
        role=role,
        permissions=permissions,
        status="active"
    )
    
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

# 获取救助站管理员列表
def get_shelter_admins(db: Session, shelter_id: str):
    """
    获取救助站管理员列表
    """
    return db.query(ShelterAdmin, User).join(
        User, ShelterAdmin.user_id == User.user_id
    ).filter(ShelterAdmin.shelter_id == shelter_id).all()

# 更新管理员信息
def update_shelter_admin(db: Session, admin_id: str, update_data: dict):
    """
    更新救助站管理员信息
    """
    db_admin = db.query(ShelterAdmin).filter(ShelterAdmin.id == admin_id).first()
    if not db_admin:
        return None
    
    for field, value in update_data.items():
        if hasattr(db_admin, field) and value is not None:
            setattr(db_admin, field, value)
    
    db.commit()
    db.refresh(db_admin)
    return db_admin

# 移除救助站管理员
def remove_shelter_admin(db: Session, admin_id: str):
    """
    移除救助站管理员
    """
    db_admin = db.query(ShelterAdmin).filter(ShelterAdmin.id == admin_id).first()
    if db_admin:
        db.delete(db_admin)
        db.commit()
    return db_admin

# 检查用户是否是救助站管理员
def check_shelter_admin(db: Session, shelter_id: str, user_id: str):
    """
    检查用户是否是救助站管理员
    """
    return db.query(ShelterAdmin).filter(
        and_(
            ShelterAdmin.shelter_id == shelter_id,
            ShelterAdmin.user_id == user_id,
            ShelterAdmin.status == "active"
        )
    ).first()
