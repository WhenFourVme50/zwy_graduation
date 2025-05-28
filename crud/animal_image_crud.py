import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from schemas.animal_image_schema import AnimalImage
from schemas.animal_schema import Animal

# 创建动物图片
def create_animal_image(db: Session, **image_data):
    """
    创建动物图片
    """
    image_id = str(uuid.uuid4())
    
    db_image = AnimalImage(
        image_id=image_id,
        **image_data
    )
    
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

# 批量创建动物图片
def create_animal_images_batch(db: Session, animal_id: str, images_data: list):
    """
    批量创建动物图片
    """
    created_images = []
    
    for image_data in images_data:
        image_id = str(uuid.uuid4())
        db_image = AnimalImage(
            image_id=image_id,
            animal_id=animal_id,
            **image_data
        )
        db.add(db_image)
        created_images.append(db_image)
    
    db.commit()
    
    # 刷新所有对象
    for image in created_images:
        db.refresh(image)
    
    return created_images

# 根据ID获取图片
def get_animal_image_by_id(db: Session, image_id: str):
    """
    根据ID获取动物图片
    """
    return db.query(AnimalImage).filter(AnimalImage.image_id == image_id).first()

# 获取动物的所有图片
def get_animal_images(db: Session, animal_id: str, include_ai_analysis: bool = False):
    """
    获取动物的所有图片（按排序排列）
    """
    query = db.query(AnimalImage).filter(AnimalImage.animal_id == animal_id)
    
    if not include_ai_analysis:
        # 如果不需要AI分析，可以优化查询
        pass
    
    return query.order_by(AnimalImage.sort_order.asc(), AnimalImage.created_at.asc()).all()

# 获取动物的主图
def get_animal_primary_image(db: Session, animal_id: str):
    """
    获取动物的主图
    """
    return db.query(AnimalImage).filter(
        and_(
            AnimalImage.animal_id == animal_id,
            AnimalImage.is_primary == True
        )
    ).first()

# 设置主图
def set_primary_image(db: Session, animal_id: str, image_id: str):
    """
    设置主图（先清除其他主图，再设置新主图）
    """
    # 清除该动物的所有主图标记
    db.query(AnimalImage).filter(
        and_(
            AnimalImage.animal_id == animal_id,
            AnimalImage.is_primary == True
        )
    ).update({"is_primary": False})
    
    # 设置新的主图
    result = db.query(AnimalImage).filter(
        AnimalImage.image_id == image_id
    ).update({"is_primary": True})
    
    db.commit()
    
    if result > 0:
        return db.query(AnimalImage).filter(AnimalImage.image_id == image_id).first()
    return None

# 更新图片信息
def update_animal_image(db: Session, image_id: str, update_data: dict):
    """
    更新动物图片信息
    """
    db_image = db.query(AnimalImage).filter(AnimalImage.image_id == image_id).first()
    if not db_image:
        return None
    
    # 如果要设置为主图，先清除其他主图
    if update_data.get('is_primary') == True:
        db.query(AnimalImage).filter(
            and_(
                AnimalImage.animal_id == db_image.animal_id,
                AnimalImage.is_primary == True,
                AnimalImage.image_id != image_id
            )
        ).update({"is_primary": False})
    
    # 更新字段
    for field, value in update_data.items():
        if hasattr(db_image, field) and value is not None:
            setattr(db_image, field, value)
    
    db.commit()
    db.refresh(db_image)
    return db_image

# 重新排序图片
def reorder_animal_images(db: Session, animal_id: str, image_orders: list):
    """
    重新排序动物图片
    image_orders: [{"image_id": "xxx", "sort_order": 1}, ...]
    """
    updated_count = 0
    
    for order_item in image_orders:
        image_id = order_item.get("image_id")
        sort_order = order_item.get("sort_order")
        
        if image_id and sort_order is not None:
            result = db.query(AnimalImage).filter(
                and_(
                    AnimalImage.image_id == image_id,
                    AnimalImage.animal_id == animal_id
                )
            ).update({"sort_order": sort_order})
            updated_count += result
    
    db.commit()
    return updated_count

# 删除图片
def delete_animal_image(db: Session, image_id: str):
    """
    删除动物图片
    """
    db_image = db.query(AnimalImage).filter(AnimalImage.image_id == image_id).first()
    if db_image:
        db.delete(db_image)
        db.commit()
    return db_image

# 批量删除图片
def delete_animal_images_batch(db: Session, image_ids: list):
    """
    批量删除动物图片
    """
    deleted_count = db.query(AnimalImage).filter(
        AnimalImage.image_id.in_(image_ids)
    ).delete(synchronize_session=False)
    
    db.commit()
    return deleted_count

# 删除动物的所有图片
def delete_all_animal_images(db: Session, animal_id: str):
    """
    删除动物的所有图片
    """
    deleted_count = db.query(AnimalImage).filter(
        AnimalImage.animal_id == animal_id
    ).delete(synchronize_session=False)
    
    db.commit()
    return deleted_count

# 更新AI分析结果
def update_ai_analysis(db: Session, image_id: str, ai_analysis: dict):
    """
    更新图片的AI分析结果
    """
    result = db.query(AnimalImage).filter(
        AnimalImage.image_id == image_id
    ).update({"ai_analysis": ai_analysis})
    
    db.commit()
    
    if result > 0:
        return db.query(AnimalImage).filter(AnimalImage.image_id == image_id).first()
    return None

# 获取图片统计信息
def get_animal_images_statistics(db: Session, animal_id: str = None):
    """
    获取动物图片统计信息
    """
    query = db.query(AnimalImage)
    
    if animal_id:
        query = query.filter(AnimalImage.animal_id == animal_id)
    
    total_images = query.count()
    images_with_ai = query.filter(AnimalImage.ai_analysis.isnot(None)).count()
    primary_images = query.filter(AnimalImage.is_primary == True).count()
    
    # 有图片的动物数量
    animals_with_images_query = db.query(AnimalImage.animal_id).distinct()
    if animal_id:
        animals_with_images_query = animals_with_images_query.filter(AnimalImage.animal_id == animal_id)
    
    animals_with_images = animals_with_images_query.count()
    
    # 平均每只动物的图片数量
    if animals_with_images > 0:
        average_images_per_animal = total_images / animals_with_images
    else:
        average_images_per_animal = 0.0
    
    return {
        "total_images": total_images,
        "images_with_ai": images_with_ai,
        "primary_images": primary_images,
        "animals_with_images": animals_with_images,
        "average_images_per_animal": round(average_images_per_animal, 2)
    }

# 搜索图片
def search_animal_images(db: Session, 
                        keyword: str = None,
                        has_ai_analysis: bool = None,
                        is_primary: bool = None,
                        animal_ids: list = None,
                        page: int = 1,
                        size: int = 20):
    """
    搜索动物图片
    """
    query = db.query(AnimalImage)
    
    # 筛选条件
    if keyword:
        query = query.filter(
            or_(
                AnimalImage.alt_text.contains(keyword),
                AnimalImage.url.contains(keyword)
            )
        )
    
    if has_ai_analysis is not None:
        if has_ai_analysis:
            query = query.filter(AnimalImage.ai_analysis.isnot(None))
        else:
            query = query.filter(AnimalImage.ai_analysis.is_(None))
    
    if is_primary is not None:
        query = query.filter(AnimalImage.is_primary == is_primary)
    
    if animal_ids:
        query = query.filter(AnimalImage.animal_id.in_(animal_ids))
    
    # 分页
    total = query.count()
    skip = (page - 1) * size
    items = query.order_by(AnimalImage.created_at.desc()).offset(skip).limit(size).all()
    
    pages = (total + size - 1) // size if total > 0 else 1
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    } 