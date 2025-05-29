import uuid
import math
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, desc, asc, func, extract
from schemas.follow_up_record_schema import FollowUpRecord
from schemas.adoption_record_schema import AdoptionRecord
from schemas.animal_schema import Animal
from schemas.user_schema import User

def create_follow_up_record(db: Session, conducted_by: str, **record_data):
    """
    创建回访记录
    """
    follow_up_id = str(uuid.uuid4())
    
    # 验证领养记录是否存在
    adoption_record = db.query(AdoptionRecord).filter(
        AdoptionRecord.record_id == record_data['adoption_record_id']
    ).first()
    
    if not adoption_record:
        raise ValueError("领养记录不存在")
    
    db_record = FollowUpRecord(
        follow_up_id=follow_up_id,
        conducted_by=conducted_by,
        **record_data
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_follow_up_by_id(db: Session, follow_up_id: str):
    """
    根据ID获取回访记录
    """
    return db.query(FollowUpRecord).options(
        joinedload(FollowUpRecord.adoption_record).joinedload(AdoptionRecord.animal),
        joinedload(FollowUpRecord.adoption_record).joinedload(AdoptionRecord.adopter),
        joinedload(FollowUpRecord.conductor)
    ).filter(FollowUpRecord.follow_up_id == follow_up_id).first()

def get_follow_ups_with_pagination(db: Session,
                                 page: int = 1,
                                 size: int = 10,
                                 adoption_record_id: str = None,
                                 animal_id: str = None,
                                 adopter_id: str = None,
                                 conducted_by: str = None,
                                 follow_up_type: str = None,
                                 animal_condition: str = None,
                                 start_date: date = None,
                                 end_date: date = None,
                                 has_concerns: bool = None,
                                 satisfaction_min: int = None,
                                 satisfaction_max: int = None,
                                 keyword: str = None,
                                 sort_by: str = "follow_up_date",
                                 sort_order: str = "desc"):
    """
    获取回访记录列表（带分页和筛选）
    """
    query = db.query(FollowUpRecord).options(
        joinedload(FollowUpRecord.adoption_record).joinedload(AdoptionRecord.animal),
        joinedload(FollowUpRecord.adoption_record).joinedload(AdoptionRecord.adopter),
        joinedload(FollowUpRecord.conductor)
    )
    
    # 筛选条件
    if adoption_record_id:
        query = query.filter(FollowUpRecord.adoption_record_id == adoption_record_id)
    if animal_id:
        query = query.join(AdoptionRecord).filter(AdoptionRecord.animal_id == animal_id)
    if adopter_id:
        query = query.join(AdoptionRecord).filter(AdoptionRecord.adopter_id == adopter_id)
    if conducted_by:
        query = query.filter(FollowUpRecord.conducted_by == conducted_by)
    if follow_up_type:
        query = query.filter(FollowUpRecord.follow_up_type == follow_up_type)
    if animal_condition:
        query = query.filter(FollowUpRecord.animal_condition == animal_condition)
    if start_date:
        query = query.filter(FollowUpRecord.follow_up_date >= start_date)
    if end_date:
        query = query.filter(FollowUpRecord.follow_up_date <= end_date)
    if has_concerns is not None:
        if has_concerns:
            query = query.filter(FollowUpRecord.concerns.isnot(None))
            query = query.filter(FollowUpRecord.concerns != "")
        else:
            query = query.filter(
                or_(
                    FollowUpRecord.concerns.is_(None),
                    FollowUpRecord.concerns == ""
                )
            )
    if satisfaction_min is not None:
        query = query.filter(FollowUpRecord.satisfaction_score >= satisfaction_min)
    if satisfaction_max is not None:
        query = query.filter(FollowUpRecord.satisfaction_score <= satisfaction_max)
    if keyword:
        query = query.join(AdoptionRecord).join(Animal).join(User).filter(
            or_(
                Animal.name.contains(keyword),
                User.username.contains(keyword),
                User.name.contains(keyword),
                FollowUpRecord.living_condition.contains(keyword),
                FollowUpRecord.health_status.contains(keyword),
                FollowUpRecord.behavioral_notes.contains(keyword),
                FollowUpRecord.concerns.contains(keyword),
                FollowUpRecord.recommendations.contains(keyword)
            )
        )
    
    # 排序
    if sort_by == "animal_name":
        query = query.join(AdoptionRecord).join(Animal).order_by(
            asc(Animal.name) if sort_order == "asc" else desc(Animal.name)
        )
    elif sort_by == "adopter_name":
        query = query.join(AdoptionRecord).join(User).order_by(
            asc(User.name) if sort_order == "asc" else desc(User.name)
        )
    elif sort_by == "animal_condition":
        query = query.order_by(
            asc(FollowUpRecord.animal_condition) if sort_order == "asc" else desc(FollowUpRecord.animal_condition)
        )
    elif sort_by == "satisfaction_score":
        query = query.order_by(
            asc(FollowUpRecord.satisfaction_score) if sort_order == "asc" else desc(FollowUpRecord.satisfaction_score)
        )
    else:  # follow_up_date
        query = query.order_by(
            asc(FollowUpRecord.follow_up_date) if sort_order == "asc" else desc(FollowUpRecord.follow_up_date)
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

def update_follow_up_record(db: Session, follow_up_id: str, **update_data):
    """
    更新回访记录
    """
    db_record = db.query(FollowUpRecord).filter(
        FollowUpRecord.follow_up_id == follow_up_id
    ).first()
    
    if not db_record:
        return None
    
    # 更新字段
    for field, value in update_data.items():
        if hasattr(db_record, field) and value is not None:
            setattr(db_record, field, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_follow_up_record(db: Session, follow_up_id: str):
    """
    删除回访记录
    """
    db_record = db.query(FollowUpRecord).filter(
        FollowUpRecord.follow_up_id == follow_up_id
    ).first()
    
    if db_record:
        db.delete(db_record)
        db.commit()
    
    return db_record

def get_follow_up_statistics(db: Session, shelter_id: str = None, year: int = None):
    """
    获取回访统计信息
    """
    query = db.query(FollowUpRecord)
    
    if shelter_id:
        query = query.join(AdoptionRecord).filter(AdoptionRecord.shelter_id == shelter_id)
    
    if year:
        query = query.filter(extract('year', FollowUpRecord.follow_up_date) == year)
    
    records = query.all()
    
    # 基本统计
    total_follow_ups = len(records)
    
    # 本月回访数
    current_month = date.today().replace(day=1)
    this_month_follow_ups = len([
        r for r in records 
        if r.follow_up_date >= current_month
    ])
    
    # 本年回访数
    current_year = date.today().year
    this_year_follow_ups = len([
        r for r in records 
        if r.follow_up_date.year == current_year
    ])
    
    # 按回访方式统计
    by_type = {}
    for record in records:
        follow_up_type = record.follow_up_type.value if hasattr(record.follow_up_type, 'value') else str(record.follow_up_type)
        by_type[follow_up_type] = by_type.get(follow_up_type, 0) + 1
    
    # 按动物状况统计
    by_condition = {}
    for record in records:
        condition = record.animal_condition.value if hasattr(record.animal_condition, 'value') else str(record.animal_condition)
        by_condition[condition] = by_condition.get(condition, 0) + 1
    
    # 按回访人统计
    by_conductor = {}
    for record in records:
        if record.conductor:
            conductor_name = record.conductor.name or record.conductor.username
            by_conductor[conductor_name] = by_conductor.get(conductor_name, 0) + 1
    
    # 平均满意度
    satisfaction_scores = [r.satisfaction_score for r in records if r.satisfaction_score]
    average_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0.0
    
    # 关注案例数
    concerning_cases = len([r for r in records if r.animal_condition.value == 'concerning' or (r.concerns and r.concerns.strip())])
    
    # 逾期回访和即将到期回访
    today = date.today()
    
    # 获取所有领养记录的下次回访日期
    adoption_records_query = db.query(AdoptionRecord)
    if shelter_id:
        adoption_records_query = adoption_records_query.filter(AdoptionRecord.shelter_id == shelter_id)
    
    adoption_records = adoption_records_query.all()
    
    overdue_count = 0
    upcoming_count = 0
    total_scheduled = 0
    
    for adoption_record in adoption_records:
        # 获取最新的回访记录
        latest_follow_up = db.query(FollowUpRecord).filter(
            FollowUpRecord.adoption_record_id == adoption_record.record_id
        ).order_by(desc(FollowUpRecord.follow_up_date)).first()
        
        if latest_follow_up and latest_follow_up.next_follow_up_date:
            total_scheduled += 1
            if latest_follow_up.next_follow_up_date < today:
                overdue_count += 1
            elif latest_follow_up.next_follow_up_date <= today + timedelta(days=7):
                upcoming_count += 1
    
    # 完成率计算
    completion_rate = ((total_scheduled - overdue_count) / total_scheduled * 100) if total_scheduled > 0 else 100.0
    
    return {
        "total_follow_ups": total_follow_ups,
        "this_month_follow_ups": this_month_follow_ups,
        "this_year_follow_ups": this_year_follow_ups,
        "by_type": by_type,
        "by_condition": by_condition,
        "by_conductor": by_conductor,
        "average_satisfaction_score": average_satisfaction,
        "concerning_cases": concerning_cases,
        "overdue_follow_ups": overdue_count,
        "upcoming_follow_ups": upcoming_count,
        "completion_rate": completion_rate
    }

def get_animal_health_trends(db: Session, animal_ids: List[str] = None, limit: int = 50):
    """
    获取动物健康趋势
    """
    query = db.query(FollowUpRecord).options(
        joinedload(FollowUpRecord.adoption_record).joinedload(AdoptionRecord.animal)
    )
    
    if animal_ids:
        query = query.join(AdoptionRecord).filter(AdoptionRecord.animal_id.in_(animal_ids))
    
    records = query.order_by(FollowUpRecord.follow_up_date).all()
    
    # 按动物分组
    animals_data = {}
    for record in records:
        animal_id = record.adoption_record.animal_id
        animal_name = record.adoption_record.animal.name
        
        if animal_id not in animals_data:
            animals_data[animal_id] = {
                "animal_id": animal_id,
                "animal_name": animal_name,
                "follow_up_history": [],
                "conditions": [],
                "satisfaction_scores": [],
                "concerns_count": 0
            }
        
        # 添加回访历史
        animals_data[animal_id]["follow_up_history"].append({
            "date": record.follow_up_date.isoformat(),
            "condition": record.animal_condition.value,
            "satisfaction_score": record.satisfaction_score,
            "has_concerns": bool(record.concerns and record.concerns.strip())
        })
        
        animals_data[animal_id]["conditions"].append(record.animal_condition.value)
        if record.satisfaction_score:
            animals_data[animal_id]["satisfaction_scores"].append(record.satisfaction_score)
        if record.concerns and record.concerns.strip():
            animals_data[animal_id]["concerns_count"] += 1
    
    # 分析趋势
    result = []
    condition_values = {"excellent": 5, "good": 4, "fair": 3, "poor": 2, "concerning": 1}
    
    for animal_id, data in animals_data.items():
        if len(data["conditions"]) < 2:
            trend = "stable"
        else:
            # 计算条件趋势
            recent_conditions = data["conditions"][-3:]  # 最近3次回访
            condition_scores = [condition_values[c] for c in recent_conditions]
            
            if len(condition_scores) >= 2:
                if condition_scores[-1] > condition_scores[0]:
                    trend = "improving"
                elif condition_scores[-1] < condition_scores[0]:
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "stable"
        
        # 计算满意度趋势
        satisfaction_trend = 0.0
        if data["satisfaction_scores"]:
            satisfaction_trend = sum(data["satisfaction_scores"]) / len(data["satisfaction_scores"])
        
        result.append({
            "animal_id": animal_id,
            "animal_name": data["animal_name"],
            "follow_up_history": data["follow_up_history"],
            "condition_trend": trend,
            "latest_condition": data["conditions"][-1] if data["conditions"] else "unknown",
            "concerns_count": data["concerns_count"],
            "satisfaction_trend": satisfaction_trend
        })
    
    # 按关注度排序（有问题的动物优先）
    result.sort(key=lambda x: (
        x["condition_trend"] == "declining",
        x["latest_condition"] in ["concerning", "poor"],
        x["concerns_count"]
    ), reverse=True)
    
    return result[:limit]

def get_follow_up_reminders(db: Session, shelter_id: str = None, days_ahead: int = 7):
    """
    获取回访提醒
    """
    today = date.today()
    target_date = today + timedelta(days=days_ahead)
    
    # 查询需要回访的记录
    query = db.query(FollowUpRecord).options(
        joinedload(FollowUpRecord.adoption_record).joinedload(AdoptionRecord.animal),
        joinedload(FollowUpRecord.adoption_record).joinedload(AdoptionRecord.adopter)
    ).filter(
        FollowUpRecord.next_follow_up_date.isnot(None),
        FollowUpRecord.next_follow_up_date <= target_date
    )
    
    if shelter_id:
        query = query.join(AdoptionRecord).filter(AdoptionRecord.shelter_id == shelter_id)
    
    records = query.order_by(FollowUpRecord.next_follow_up_date).all()
    
    reminders = []
    for record in records:
        days_overdue = max(0, (today - record.next_follow_up_date).days)
        
        # 确定优先级
        if days_overdue > 0:
            priority = "high"
        elif record.next_follow_up_date <= today + timedelta(days=3):
            priority = "medium"
        else:
            priority = "low"
        
        reminders.append({
            "adoption_record_id": record.adoption_record_id,
            "animal_name": record.adoption_record.animal.name,
            "adopter_name": record.adoption_record.adopter.name or record.adoption_record.adopter.username,
            "last_follow_up_date": record.follow_up_date.isoformat(),
            "next_follow_up_date": record.next_follow_up_date.isoformat(),
            "days_overdue": days_overdue,
            "priority": priority
        })
    
    return reminders

def get_adoption_record_follow_ups(db: Session, adoption_record_id: str):
    """
    获取特定领养记录的所有回访记录
    """
    return db.query(FollowUpRecord).options(
        joinedload(FollowUpRecord.conductor)
    ).filter(
        FollowUpRecord.adoption_record_id == adoption_record_id
    ).order_by(FollowUpRecord.follow_up_date.desc()).all() 