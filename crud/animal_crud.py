import uuid
import math
from datetime import datetime, date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc
from schemas.animal_schema import Animal
from schemas.shelter_schema import Shelter

# 创建动物
def create_animal(db: Session, **animal_data):
    """
    创建新动物
    """
    animal_id = str(uuid.uuid4())
    
    # 处理救助日期
    if animal_data.get('rescue_date'):
        try:
            animal_data['rescue_date'] = datetime.strptime(
                animal_data['rescue_date'], "%Y-%m-%d"
            ).date()
        except ValueError:
            animal_data['rescue_date'] = None
    
    db_animal = Animal(
        animal_id=animal_id,
        **animal_data
    )
    
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

# 根据ID获取动物
def get_animal_by_id(db: Session, animal_id: str):
    """
    根据ID获取动物（包含救助站信息）
    """
    return db.query(Animal).options(
        joinedload(Animal.shelter)
    ).filter(Animal.animal_id == animal_id).first()

# 获取动物列表（带分页和筛选）
def get_animals_with_pagination(db: Session,
                               page: int = 1,
                               size: int = 10,
                               species: str = None,
                               age_category: str = None,
                               gender: str = None,
                               size_filter: str = None,
                               good_with_kids: bool = None,
                               good_with_pets: bool = None,
                               energy_level: str = None,
                               is_neutered: bool = None,
                               is_vaccinated: bool = None,
                               shelter_id: str = None,
                               status: str = None,
                               min_fee: float = None,
                               max_fee: float = None,
                               keyword: str = None,
                               sort_by: str = "created_at",
                               sort_order: str = "desc"):
    """
    获取动物列表（带分页和筛选）
    """
    query = db.query(Animal).options(joinedload(Animal.shelter))
    
    # 筛选条件
    if species:
        query = query.filter(Animal.species == species)
    if age_category:
        query = query.filter(Animal.age_category == age_category)
    if gender:
        query = query.filter(Animal.gender == gender)
    if size_filter:
        query = query.filter(Animal.size == size_filter)
    if good_with_kids is not None:
        query = query.filter(Animal.good_with_kids == good_with_kids)
    if good_with_pets is not None:
        query = query.filter(Animal.good_with_pets == good_with_pets)
    if energy_level:
        query = query.filter(Animal.energy_level == energy_level)
    if is_neutered is not None:
        query = query.filter(Animal.is_neutered == is_neutered)
    if is_vaccinated is not None:
        query = query.filter(Animal.is_vaccinated == is_vaccinated)
    if shelter_id:
        query = query.filter(Animal.shelter_id == shelter_id)
    if status:
        query = query.filter(Animal.status == status)
    if min_fee is not None:
        query = query.filter(Animal.adoption_fee >= min_fee)
    if max_fee is not None:
        query = query.filter(Animal.adoption_fee <= max_fee)
    if keyword:
        query = query.filter(
            or_(
                Animal.name.contains(keyword),
                Animal.description.contains(keyword),
                Animal.breed.contains(keyword),
                Animal.color.contains(keyword)
            )
        )
    
    # 排序
    if sort_by == "name":
        query = query.order_by(asc(Animal.name) if sort_order == "asc" else desc(Animal.name))
    elif sort_by == "age":
        query = query.order_by(asc(Animal.age) if sort_order == "asc" else desc(Animal.age))
    elif sort_by == "adoption_fee":
        query = query.order_by(asc(Animal.adoption_fee) if sort_order == "asc" else desc(Animal.adoption_fee))
    elif sort_by == "view_count":
        query = query.order_by(asc(Animal.view_count) if sort_order == "asc" else desc(Animal.view_count))
    else:  # created_at
        query = query.order_by(asc(Animal.created_at) if sort_order == "asc" else desc(Animal.created_at))
    
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

# 更新动物信息
def update_animal(db: Session, animal_id: str, update_data: dict):
    """
    更新动物信息
    """
    db_animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if not db_animal:
        return None
    
    # 处理救助日期
    if 'rescue_date' in update_data and update_data['rescue_date']:
        try:
            update_data['rescue_date'] = datetime.strptime(
                update_data['rescue_date'], "%Y-%m-%d"
            ).date()
        except ValueError:
            del update_data['rescue_date']
    
    # 更新字段
    for field, value in update_data.items():
        if hasattr(db_animal, field) and value is not None:
            setattr(db_animal, field, value)
    
    db.commit()
    db.refresh(db_animal)
    return db_animal

# 删除动物
def delete_animal(db: Session, animal_id: str):
    """
    删除动物
    """
    db_animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if db_animal:
        db.delete(db_animal)
        db.commit()
    return db_animal

# 增加浏览次数
def increment_view_count(db: Session, animal_id: str):
    """
    增加浏览次数
    """
    db_animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if db_animal:
        db_animal.view_count += 1
        db.commit()
        db.refresh(db_animal)
    return db_animal

# 更新收藏次数
def update_favorite_count(db: Session, animal_id: str, increment: bool = True):
    """
    更新收藏次数
    """
    db_animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if db_animal:
        if increment:
            db_animal.favorite_count += 1
        else:
            db_animal.favorite_count = max(0, db_animal.favorite_count - 1)
        db.commit()
        db.refresh(db_animal)
    return db_animal

# 更新动物图片
def update_animal_images(db: Session, animal_id: str, images: list):
    """
    更新动物图片
    """
    db_animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if db_animal:
        db_animal.images = images
        db.commit()
        db.refresh(db_animal)
    return db_animal

# 更新动物视频
def update_animal_videos(db: Session, animal_id: str, videos: list):
    """
    更新动物视频
    """
    db_animal = db.query(Animal).filter(Animal.animal_id == animal_id).first()
    if db_animal:
        db_animal.videos = videos
        db.commit()
        db.refresh(db_animal)
    return db_animal

# 获取动物统计信息
def get_animal_statistics(db: Session, shelter_id: str = None):
    """
    获取动物统计信息
    """
    query = db.query(Animal)
    if shelter_id:
        query = query.filter(Animal.shelter_id == shelter_id)
    
    total_animals = query.count()
    available_animals = query.filter(Animal.status == 'available').count()
    adopted_animals = query.filter(Animal.status == 'adopted').count()
    pending_animals = query.filter(Animal.status == 'pending').count()
    
    # 按物种统计
    species_stats = db.query(
        Animal.species, func.count(Animal.animal_id)
    ).group_by(Animal.species)
    
    if shelter_id:
        species_stats = species_stats.filter(Animal.shelter_id == shelter_id)
    
    by_species = {species: count for species, count in species_stats.all()}
    
    # 按年龄段统计
    age_stats = db.query(
        Animal.age_category, func.count(Animal.animal_id)
    ).group_by(Animal.age_category)
    
    if shelter_id:
        age_stats = age_stats.filter(Animal.shelter_id == shelter_id)
    
    by_age_category = {age: count for age, count in age_stats.all()}
    
    # 按体型统计
    size_stats = db.query(
        Animal.size, func.count(Animal.animal_id)
    ).group_by(Animal.size)
    
    if shelter_id:
        size_stats = size_stats.filter(Animal.shelter_id == shelter_id)
    
    by_size = {size: count for size, count in size_stats.all()}
    
    # 平均领养费用
    avg_fee_query = query.filter(Animal.adoption_fee > 0)
    avg_fee = avg_fee_query.with_entities(func.avg(Animal.adoption_fee)).scalar() or 0.0
    
    # 总浏览数和收藏数
    total_views = query.with_entities(func.sum(Animal.view_count)).scalar() or 0
    total_favorites = query.with_entities(func.sum(Animal.favorite_count)).scalar() or 0
    
    return {
        "total_animals": total_animals,
        "available_animals": available_animals,
        "adopted_animals": adopted_animals,
        "pending_animals": pending_animals,
        "by_species": by_species,
        "by_age_category": by_age_category,
        "by_size": by_size,
        "average_adoption_fee": float(avg_fee),
        "total_views": total_views,
        "total_favorites": total_favorites
    }

# 获取推荐动物
def get_recommended_animals(db: Session, user_id: str = None, limit: int = 10):
    """
    获取推荐动物（简单推荐算法）
    """
    query = db.query(Animal).options(joinedload(Animal.shelter))
    
    # 只推荐可领养的动物
    query = query.filter(Animal.status == 'available')
    
    if user_id:
        # 这里可以根据用户的偏好历史、浏览记录等进行个性化推荐
        # 目前使用简单的推荐策略：浏览量和收藏量高的动物
        query = query.order_by(
            desc(Animal.view_count + Animal.favorite_count * 2),
            desc(Animal.created_at)
        )
    else:
        # 访客用户：推荐最新和最受欢迎的动物
        query = query.order_by(
            desc(Animal.view_count),
            desc(Animal.created_at)
        )
    
    return query.limit(limit).all()

# 获取动物的待处理申请数量（模拟）
def get_pending_applications_count(db: Session, animal_id: str):
    """
    获取动物的待处理申请数量
    注意：这里返回模拟数据，实际应该从申请表中统计
    """
    # 模拟数据
    import random
    return random.randint(0, 5)

# 更新扩展的动物列表查询
def get_animals_with_extended_info(db: Session,
                                  page: int = 1,
                                  size: int = 10,
                                  species: str = None,
                                  breed: str = None,
                                  age_category: str = None,
                                  gender: str = None,
                                  size_filter: str = None,
                                  status: str = None,
                                  shelter_id: str = None,
                                  city: str = None,
                                  good_with_kids: bool = None,
                                  good_with_pets: bool = None,
                                  is_neutered: bool = None,
                                  is_vaccinated: bool = None,
                                  keyword: str = None,
                                  sort_by: str = "created_at",
                                  sort_order: str = "desc"):
    """
    获取动物列表（带扩展信息）
    """
    query = db.query(Animal).options(joinedload(Animal.shelter))
    
    # 筛选条件
    if species:
        query = query.filter(Animal.species == species)
    if breed:
        query = query.filter(Animal.breed.contains(breed))
    if age_category:
        query = query.filter(Animal.age_category == age_category)
    if gender:
        query = query.filter(Animal.gender == gender)
    if size_filter:
        query = query.filter(Animal.size == size_filter)
    if status:
        query = query.filter(Animal.status == status)
    if shelter_id:
        query = query.filter(Animal.shelter_id == shelter_id)
    if city:
        # 通过救助站的城市筛选
        query = query.join(Animal.shelter).filter(Shelter.city == city)
    if good_with_kids is not None:
        query = query.filter(Animal.good_with_kids == good_with_kids)
    if good_with_pets is not None:
        query = query.filter(Animal.good_with_pets == good_with_pets)
    if is_neutered is not None:
        query = query.filter(Animal.is_neutered == is_neutered)
    if is_vaccinated is not None:
        query = query.filter(Animal.is_vaccinated == is_vaccinated)
    if keyword:
        query = query.filter(
            or_(
                Animal.name.contains(keyword),
                Animal.description.contains(keyword),
                Animal.breed.contains(keyword),
                Animal.color.contains(keyword)
            )
        )
    
    # 排序
    if sort_by == "name":
        query = query.order_by(asc(Animal.name) if sort_order == "asc" else desc(Animal.name))
    elif sort_by == "age":
        query = query.order_by(asc(Animal.age) if sort_order == "asc" else desc(Animal.age))
    elif sort_by == "view_count":
        query = query.order_by(asc(Animal.view_count) if sort_order == "asc" else desc(Animal.view_count))
    else:  # created_at
        query = query.order_by(asc(Animal.created_at) if sort_order == "asc" else desc(Animal.created_at))
    
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

# 获取动物详情（包含图片信息）
def get_animal_detail_with_images(db: Session, animal_id: str):
    """
    获取动物详情（包含图片信息）
    """
    animal = db.query(Animal).options(
        joinedload(Animal.shelter),
        joinedload(Animal.animal_images)
    ).filter(Animal.animal_id == animal_id).first()
    
    return animal
