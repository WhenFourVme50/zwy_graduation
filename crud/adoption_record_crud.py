import uuid
import math
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, desc, asc, func, extract
from schemas.adoption_record_schema import AdoptionRecord
from schemas.adoption_application_schema import AdoptionApplication
from schemas.animal_schema import Animal
from schemas.user_schema import User
from schemas.shelter_schema import Shelter

def create_adoption_record(db: Session, **record_data):
    """
    创建领养记录
    """
    record_id = str(uuid.uuid4())
    
    # 获取申请信息以填充其他字段
    application = db.query(AdoptionApplication).filter(
        AdoptionApplication.application_id == record_data['application_id']
    ).first()
    
    if not application:
        raise ValueError("申请不存在")
    
    # 处理回访计划
    follow_up_schedule = record_data.get('follow_up_schedule')
    if follow_up_schedule:
        # 转换为JSON格式
        follow_up_json = []
        for item in follow_up_schedule:
            follow_up_json.append({
                "date": item.date.isoformat() if hasattr(item, 'date') else item['date'],
                "type": item.type if hasattr(item, 'type') else item['type'],
                "status": item.status if hasattr(item, 'status') else item.get('status', 'pending'),
                "notes": item.notes if hasattr(item, 'notes') else item.get('notes'),
                "completed_at": item.completed_at.isoformat() if hasattr(item, 'completed_at') and item.completed_at else item.get('completed_at')
            })
        record_data['follow_up_schedule'] = follow_up_json
    
    db_record = AdoptionRecord(
        record_id=record_id,
        animal_id=application.animal_id,
        adopter_id=application.user_id,
        shelter_id=application.animal.shelter_id,
        **record_data
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_record_by_id(db: Session, record_id: str):
    """
    根据ID获取领养记录
    """
    return db.query(AdoptionRecord).options(
        joinedload(AdoptionRecord.application),
        joinedload(AdoptionRecord.animal),
        joinedload(AdoptionRecord.adopter),
        joinedload(AdoptionRecord.shelter)
    ).filter(AdoptionRecord.record_id == record_id).first()

def get_record_by_application_id(db: Session, application_id: str):
    """
    根据申请ID获取领养记录
    """
    return db.query(AdoptionRecord).options(
        joinedload(AdoptionRecord.application),
        joinedload(AdoptionRecord.animal),
        joinedload(AdoptionRecord.adopter),
        joinedload(AdoptionRecord.shelter)
    ).filter(AdoptionRecord.application_id == application_id).first()

def get_records_with_pagination(db: Session,
                               page: int = 1,
                               size: int = 10,
                               animal_id: str = None,
                               adopter_id: str = None,
                               shelter_id: str = None,
                               species: str = None,
                               start_date: date = None,
                               end_date: date = None,
                               contract_signed: bool = None,
                               keyword: str = None,
                               sort_by: str = "adoption_date",
                               sort_order: str = "desc"):
    """
    获取领养记录列表（带分页和筛选）
    """
    query = db.query(AdoptionRecord).options(
        joinedload(AdoptionRecord.animal),
        joinedload(AdoptionRecord.adopter),
        joinedload(AdoptionRecord.shelter)
    )
    
    # 筛选条件
    if animal_id:
        query = query.filter(AdoptionRecord.animal_id == animal_id)
    if adopter_id:
        query = query.filter(AdoptionRecord.adopter_id == adopter_id)
    if shelter_id:
        query = query.filter(AdoptionRecord.shelter_id == shelter_id)
    if species:
        query = query.join(Animal).filter(Animal.species == species)
    if start_date:
        query = query.filter(AdoptionRecord.adoption_date >= start_date)
    if end_date:
        query = query.filter(AdoptionRecord.adoption_date <= end_date)
    if contract_signed is not None:
        query = query.filter(AdoptionRecord.contract_signed == contract_signed)
    if keyword:
        query = query.join(Animal).join(User).join(Shelter).filter(
            or_(
                Animal.name.contains(keyword),
                User.username.contains(keyword),
                User.name.contains(keyword),
                Shelter.name.contains(keyword),
                AdoptionRecord.microchip_id.contains(keyword),
                AdoptionRecord.notes.contains(keyword)
            )
        )
    
    # 排序
    if sort_by == "animal_name":
        query = query.join(Animal).order_by(
            asc(Animal.name) if sort_order == "asc" else desc(Animal.name)
        )
    elif sort_by == "adopter_name":
        query = query.join(User).order_by(
            asc(User.name) if sort_order == "asc" else desc(User.name)
        )
    elif sort_by == "shelter_name":
        query = query.join(Shelter).order_by(
            asc(Shelter.name) if sort_order == "asc" else desc(Shelter.name)
        )
    elif sort_by == "adoption_fee":
        query = query.order_by(
            asc(AdoptionRecord.adoption_fee) if sort_order == "asc" else desc(AdoptionRecord.adoption_fee)
        )
    else:  # adoption_date
        query = query.order_by(
            asc(AdoptionRecord.adoption_date) if sort_order == "asc" else desc(AdoptionRecord.adoption_date)
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

def update_record(db: Session, record_id: str, **update_data):
    """
    更新领养记录
    """
    db_record = db.query(AdoptionRecord).filter(
        AdoptionRecord.record_id == record_id
    ).first()
    
    if not db_record:
        return None
    
    # 处理回访计划更新
    if 'follow_up_schedule' in update_data and update_data['follow_up_schedule']:
        follow_up_json = []
        for item in update_data['follow_up_schedule']:
            follow_up_json.append({
                "date": item.date.isoformat() if hasattr(item, 'date') else item['date'],
                "type": item.type if hasattr(item, 'type') else item['type'],
                "status": item.status if hasattr(item, 'status') else item.get('status', 'pending'),
                "notes": item.notes if hasattr(item, 'notes') else item.get('notes'),
                "completed_at": item.completed_at.isoformat() if hasattr(item, 'completed_at') and item.completed_at else item.get('completed_at')
            })
        update_data['follow_up_schedule'] = follow_up_json
    
    # 更新字段
    for field, value in update_data.items():
        if hasattr(db_record, field) and value is not None:
            setattr(db_record, field, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: str):
    """
    删除领养记录
    """
    db_record = db.query(AdoptionRecord).filter(
        AdoptionRecord.record_id == record_id
    ).first()
    
    if db_record:
        db.delete(db_record)
        db.commit()
    
    return db_record

def get_adoption_statistics(db: Session, shelter_id: str = None, year: int = None):
    """
    获取领养统计信息
    """
    query = db.query(AdoptionRecord)
    
    if shelter_id:
        query = query.filter(AdoptionRecord.shelter_id == shelter_id)
    
    if year:
        query = query.filter(extract('year', AdoptionRecord.adoption_date) == year)
    
    records = query.all()
    
    # 基本统计
    total_adoptions = len(records)
    
    # 本月领养数
    current_month = date.today().replace(day=1)
    this_month_adoptions = len([
        r for r in records 
        if r.adoption_date >= current_month
    ])
    
    # 本年领养数
    current_year = date.today().year
    this_year_adoptions = len([
        r for r in records 
        if r.adoption_date.year == current_year
    ])
    
    # 费用统计
    total_fees = sum([float(r.adoption_fee) for r in records])
    average_fee = total_fees / total_adoptions if total_adoptions > 0 else 0.0
    
    # 按物种统计
    by_species = {}
    for record in records:
        if record.animal:
            species = record.animal.species
            by_species[species] = by_species.get(species, 0) + 1
    
    # 按救助站统计
    by_shelter = {}
    for record in records:
        if record.shelter:
            shelter_name = record.shelter.name
            by_shelter[shelter_name] = by_shelter.get(shelter_name, 0) + 1
    
    # 按月份统计（最近12个月）
    by_month = {}
    for i in range(12):
        month_date = date.today().replace(day=1) - timedelta(days=30*i)
        month_key = month_date.strftime("%Y-%m")
        month_count = len([
            r for r in records 
            if r.adoption_date.strftime("%Y-%m") == month_key
        ])
        by_month[month_key] = month_count
    
    # 合同签署率
    contract_signed_count = len([r for r in records if r.contract_signed])
    contract_signed_rate = (contract_signed_count / total_adoptions * 100) if total_adoptions > 0 else 0.0
    
    # 芯片植入率
    microchip_count = len([r for r in records if r.microchip_id])
    microchip_rate = (microchip_count / total_adoptions * 100) if total_adoptions > 0 else 0.0
    
    return {
        "total_adoptions": total_adoptions,
        "this_month_adoptions": this_month_adoptions,
        "this_year_adoptions": this_year_adoptions,
        "total_fees_collected": total_fees,
        "average_adoption_fee": average_fee,
        "by_species": by_species,
        "by_shelter": by_shelter,
        "by_month": by_month,
        "contract_signed_rate": contract_signed_rate,
        "microchip_rate": microchip_rate
    }

def get_follow_up_statistics(db: Session, shelter_id: str = None):
    """
    获取回访统计信息
    """
    query = db.query(AdoptionRecord)
    
    if shelter_id:
        query = query.filter(AdoptionRecord.shelter_id == shelter_id)
    
    records = query.filter(AdoptionRecord.follow_up_schedule.isnot(None)).all()
    
    total_follow_ups = 0
    pending_follow_ups = 0
    completed_follow_ups = 0
    overdue_follow_ups = 0
    upcoming_follow_ups = 0
    
    today = date.today()
    
    for record in records:
        if record.follow_up_schedule:
            for follow_up in record.follow_up_schedule:
                total_follow_ups += 1
                status = follow_up.get('status', 'pending')
                follow_up_date = datetime.strptime(follow_up['date'], '%Y-%m-%d').date()
                
                if status == 'completed':
                    completed_follow_ups += 1
                elif status == 'pending':
                    pending_follow_ups += 1
                    if follow_up_date < today:
                        overdue_follow_ups += 1
                    elif follow_up_date <= today + timedelta(days=7):
                        upcoming_follow_ups += 1
    
    completion_rate = (completed_follow_ups / total_follow_ups * 100) if total_follow_ups > 0 else 0.0
    
    return {
        "total_follow_ups": total_follow_ups,
        "pending_follow_ups": pending_follow_ups,
        "completed_follow_ups": completed_follow_ups,
        "overdue_follow_ups": overdue_follow_ups,
        "upcoming_follow_ups": upcoming_follow_ups,
        "completion_rate": completion_rate
    }

def get_user_adoption_records(db: Session, user_id: str, page: int = 1, size: int = 10):
    """
    获取用户的领养记录
    """
    return get_records_with_pagination(
        db=db,
        page=page,
        size=size,
        adopter_id=user_id
    )

def update_follow_up_status(db: Session, record_id: str, follow_up_index: int, status: str, notes: str = None):
    """
    更新回访状态
    """
    db_record = db.query(AdoptionRecord).filter(
        AdoptionRecord.record_id == record_id
    ).first()
    
    if not db_record or not db_record.follow_up_schedule:
        return None
    
    if follow_up_index >= len(db_record.follow_up_schedule):
        return None
    
    # 更新回访状态
    follow_up_schedule = db_record.follow_up_schedule.copy()
    follow_up_schedule[follow_up_index]['status'] = status
    if notes:
        follow_up_schedule[follow_up_index]['notes'] = notes
    if status == 'completed':
        follow_up_schedule[follow_up_index]['completed_at'] = datetime.utcnow().isoformat()
    
    db_record.follow_up_schedule = follow_up_schedule
    db.commit()
    db.refresh(db_record)
    
    return db_record 