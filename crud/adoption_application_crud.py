import uuid
import math
from datetime import datetime, date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, desc, asc
from schemas.adoption_application_schema import AdoptionApplication
from schemas.animal_schema import Animal
from schemas.user_schema import User

def create_adoption_application(db: Session, user_id: str, **application_data):
    """
    创建领养申请
    """
    application_id = str(uuid.uuid4())
    
    # 构建申请数据
    application_json = {
        "living_situation": application_data.get('living_situation'),
        "family_info": application_data.get('family_info'),
        "veterinarian_info": application_data.get('veterinarian_info'),
        "references": application_data.get('references'),
        "additional_info": application_data.get('additional_info', {})
    }
    
    db_application = AdoptionApplication(
        application_id=application_id,
        animal_id=application_data['animal_id'],
        user_id=user_id,
        application_data=application_json,
        reason=application_data.get('reason'),
        previous_experience=application_data.get('previous_experience'),
        living_situation=application_data.get('living_situation'),
        family_info=application_data.get('family_info'),
        veterinarian_info=application_data.get('veterinarian_info'),
        references=application_data.get('references')
    )
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_application_by_id(db: Session, application_id: str):
    """
    根据ID获取申请详情
    """
    return db.query(AdoptionApplication).options(
        joinedload(AdoptionApplication.animal),
        joinedload(AdoptionApplication.user),
        joinedload(AdoptionApplication.reviewer)
    ).filter(AdoptionApplication.application_id == application_id).first()

def get_applications_with_pagination(db: Session,
                                   page: int = 1,
                                   size: int = 10,
                                   status: str = None,
                                   animal_id: str = None,
                                   user_id: str = None,
                                   species: str = None,
                                   keyword: str = None,
                                   sort_by: str = "created_at",
                                   sort_order: str = "desc"):
    """
    获取申请列表（带分页和筛选）
    """
    query = db.query(AdoptionApplication).options(
        joinedload(AdoptionApplication.animal),
        joinedload(AdoptionApplication.user)
    )
    
    # 筛选条件
    if status:
        query = query.filter(AdoptionApplication.status == status)
    if animal_id:
        query = query.filter(AdoptionApplication.animal_id == animal_id)
    if user_id:
        query = query.filter(AdoptionApplication.user_id == user_id)
    if species:
        query = query.join(Animal).filter(Animal.species == species)
    if keyword:
        query = query.join(Animal).join(User).filter(
            or_(
                Animal.name.contains(keyword),
                User.username.contains(keyword),
                User.name.contains(keyword),
                AdoptionApplication.reason.contains(keyword)
            )
        )
    
    # 排序
    if sort_by == "animal_name":
        query = query.join(Animal).order_by(
            asc(Animal.name) if sort_order == "asc" else desc(Animal.name)
        )
    elif sort_by == "applicant_name":
        query = query.join(User).order_by(
            asc(User.name) if sort_order == "asc" else desc(User.name)
        )
    elif sort_by == "status":
        query = query.order_by(
            asc(AdoptionApplication.status) if sort_order == "asc" else desc(AdoptionApplication.status)
        )
    else:  # created_at
        query = query.order_by(
            asc(AdoptionApplication.created_at) if sort_order == "asc" else desc(AdoptionApplication.created_at)
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

def update_application(db: Session, application_id: str, reviewer_id: str = None, **update_data):
    """
    更新申请信息
    """
    db_application = db.query(AdoptionApplication).filter(
        AdoptionApplication.application_id == application_id
    ).first()
    
    if not db_application:
        return None
    
    # 更新字段
    for field, value in update_data.items():
        if hasattr(db_application, field) and value is not None:
            setattr(db_application, field, value)
    
    # 如果状态发生变化，记录审核信息
    if 'status' in update_data and reviewer_id:
        db_application.reviewed_by = reviewer_id
        db_application.reviewed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_application)
    return db_application

def delete_application(db: Session, application_id: str):
    """
    删除申请
    """
    db_application = db.query(AdoptionApplication).filter(
        AdoptionApplication.application_id == application_id
    ).first()
    
    if db_application:
        db.delete(db_application)
        db.commit()
    
    return db_application

def get_user_applications(db: Session, user_id: str, page: int = 1, size: int = 10):
    """
    获取用户的申请列表
    """
    return get_applications_with_pagination(
        db=db,
        page=page,
        size=size,
        user_id=user_id
    )

def get_animal_applications(db: Session, animal_id: str, page: int = 1, size: int = 10):
    """
    获取动物的申请列表
    """
    return get_applications_with_pagination(
        db=db,
        page=page,
        size=size,
        animal_id=animal_id
    )

def get_application_statistics(db: Session, shelter_id: str = None):
    """
    获取申请统计信息
    """
    query = db.query(AdoptionApplication)
    
    if shelter_id:
        query = query.join(Animal).filter(Animal.shelter_id == shelter_id)
    
    applications = query.all()
    
    total_applications = len(applications)
    pending_applications = len([app for app in applications if app.status == 'pending'])
    approved_applications = len([app for app in applications if app.status == 'approved'])
    rejected_applications = len([app for app in applications if app.status == 'rejected'])
    completed_adoptions = len([app for app in applications if app.status == 'completed'])
    
    # 按状态统计
    by_status = {}
    for app in applications:
        status = app.status.value if hasattr(app.status, 'value') else str(app.status)
        by_status[status] = by_status.get(status, 0) + 1
    
    # 按动物种类统计
    by_animal_species = {}
    for app in applications:
        if app.animal:
            species = app.animal.species
            by_animal_species[species] = by_animal_species.get(species, 0) + 1
    
    # 计算平均处理天数
    processed_apps = [app for app in applications if app.reviewed_at]
    avg_days = 0.0
    if processed_apps:
        total_days = sum([
            (app.reviewed_at - app.created_at).days 
            for app in processed_apps
        ])
        avg_days = total_days / len(processed_apps)
    
    # 计算总收费
    total_fees = sum([
        float(app.adoption_fee_paid) 
        for app in applications 
        if app.adoption_fee_paid
    ])
    
    return {
        "total_applications": total_applications,
        "pending_applications": pending_applications,
        "approved_applications": approved_applications,
        "rejected_applications": rejected_applications,
        "completed_adoptions": completed_adoptions,
        "by_status": by_status,
        "by_animal_species": by_animal_species,
        "average_processing_days": avg_days,
        "total_fees_collected": total_fees
    }

def get_user_animal_application(db: Session, user_id: str, animal_id: str):
    """
    获取用户对特定动物的申请
    """
    return db.query(AdoptionApplication).filter(
        AdoptionApplication.user_id == user_id,
        AdoptionApplication.animal_id == animal_id,
        AdoptionApplication.status.in_(['pending', 'under_review', 'approved'])
    ).first() 