import os
import uuid
from typing import Dict, Optional, List
from fastapi import UploadFile
from models import animal_models
from db import session
from crud import animal_crud, animal_image_crud

async def get_animals_func(
    page: int = 1,
    size: int = 10,
    species: Optional[str] = None,
    breed: Optional[str] = None,
    age_category: Optional[str] = None,
    gender: Optional[str] = None,
    size_filter: Optional[str] = None,
    status: Optional[str] = None,
    shelter_id: Optional[str] = None,
    city: Optional[str] = None,
    good_with_kids: Optional[bool] = None,
    good_with_pets: Optional[bool] = None,
    is_neutered: Optional[bool] = None,
    is_vaccinated: Optional[bool] = None,
    keyword: Optional[str] = None,
    sort: str = "created_at",
    order: str = "desc"
):
    """
    获取动物列表
    """
    db_session = session.get_session()
    
    try:
        # 获取分页数据
        result = animal_crud.get_animals_with_extended_info(
            db=db_session,
            page=page,
            size=size,
            species=species,
            breed=breed,
            age_category=age_category,
            gender=gender,
            size_filter=size_filter,
            status=status,
            shelter_id=shelter_id,
            city=city,
            good_with_kids=good_with_kids,
            good_with_pets=good_with_pets,
            is_neutered=is_neutered,
            is_vaccinated=is_vaccinated,
            keyword=keyword,
            sort_by=sort,
            sort_order=order
        )
        
        # 构造响应数据
        items = []
        for animal in result["items"]:
            # 获取动物图片（只取URL）
            images = animal_image_crud.get_animal_images(db_session, animal.animal_id)
            image_urls = [img.url for img in images] if images else []
            
            # 获取待处理申请数量
            pending_applications = animal_crud.get_pending_applications_count(db_session, animal.animal_id)
            
            item_data = animal_models.AnimalListItem(
                animal_id=animal.animal_id,
                name=animal.name,
                species=animal.species,
                breed=animal.breed,
                age=animal.age,
                age_category=animal.age_category,
                gender=animal.gender,
                size=animal.size,
                weight=float(animal.weight) if animal.weight else None,
                color=animal.color,
                description=animal.description,
                personality=animal.personality or [],
                health_status=animal.health_status,
                is_neutered=animal.is_neutered,
                is_vaccinated=animal.is_vaccinated,
                good_with_kids=animal.good_with_kids,
                good_with_pets=animal.good_with_pets,
                energy_level=animal.energy_level,
                training_level=animal.training_level,
                shelter_id=animal.shelter_id,
                shelter_name=animal.shelter.name if animal.shelter else None,
                shelter_city=animal.shelter.city if animal.shelter else None,
                status=animal.status,
                rescue_date=animal.rescue_date.strftime("%Y-%m-%d") if animal.rescue_date else None,
                adoption_fee=float(animal.adoption_fee),
                images=image_urls,
                videos=animal.videos or [],
                view_count=animal.view_count,
                favorite_count=animal.favorite_count,
                pending_applications=pending_applications,
                created_at=animal.created_at.isoformat() if animal.created_at else None
            )
            items.append(item_data)
        
        list_data = animal_models.AnimalListData(
            items=items,
            total=result["total"],
            page=result["page"],
            size=result["size"],
            pages=result["pages"]
        )
        
        return animal_models.AnimalListResponse(
            code=200,
            message="获取成功",
            data=list_data
        )
        
    except Exception as e:
        print(f"Get animals error: {e}")
        return animal_models.AnimalListResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def get_animal_func(animal_id: str):
    """
    获取动物详情
    """
    db_session = session.get_session()
    
    try:
        # 获取动物信息
        animal = animal_crud.get_animal_detail_with_images(db_session, animal_id)
        if not animal:
            return animal_models.AnimalGetResponse(
                code=404,
                message="动物不存在"
            )
        
        # 增加浏览次数
        animal_crud.increment_view_count(db_session, animal_id)
        
        # 获取图片信息
        images = []
        for img in animal.animal_images:
            images.append(animal_models.AnimalImageInfo(
                image_id=img.image_id,
                url=img.url,
                alt_text=img.alt_text,
                is_primary=img.is_primary,
                sort_order=img.sort_order
            ))
        
        # 获取待处理申请数量
        pending_applications = animal_crud.get_pending_applications_count(db_session, animal_id)
        
        # 构造救助站信息
        shelter_info = animal_models.ShelterInfo(
            shelter_id=animal.shelter.shelter_id,
            name=animal.shelter.name,
            city=animal.shelter.city,
            phone=animal.shelter.phone,
            address=animal.shelter.address
        ) if animal.shelter else None
        
        # 构造响应数据
        animal_data = animal_models.AnimalDetailResponse(
            animal_id=animal.animal_id,
            name=animal.name,
            species=animal.species,
            breed=animal.breed,
            age=animal.age,
            age_category=animal.age_category,
            gender=animal.gender,
            size=animal.size,
            weight=float(animal.weight) if animal.weight else None,
            color=animal.color,
            description=animal.description,
            personality=animal.personality or [],
            health_status=animal.health_status,
            medical_history=animal.medical_history or [],
            is_neutered=animal.is_neutered,
            is_vaccinated=animal.is_vaccinated,
            vaccination_records=animal.vaccination_records or [],
            special_needs=animal.special_needs,
            good_with_kids=animal.good_with_kids,
            good_with_pets=animal.good_with_pets,
            energy_level=animal.energy_level,
            training_level=animal.training_level,
            shelter=shelter_info,
            status=animal.status,
            location=animal.location,
            rescue_date=animal.rescue_date.strftime("%Y-%m-%d") if animal.rescue_date else None,
            rescue_story=animal.rescue_story,
            adoption_fee=float(animal.adoption_fee),
            images=images,
            videos=animal.videos or [],
            ai_features=animal.ai_features or {},
            view_count=animal.view_count,
            favorite_count=animal.favorite_count,
            pending_applications=pending_applications,
            created_at=animal.created_at.isoformat() if animal.created_at else None,
            updated_at=animal.updated_at.isoformat() if animal.updated_at else None
        )
        
        return animal_models.AnimalGetResponse(
            code=200,
            message="获取成功",
            data=animal_data
        )
        
    except Exception as e:
        print(f"Get animal error: {e}")
        return animal_models.AnimalGetResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def create_animal_func(data: animal_models.AnimalCreateRequest):
    """
    创建动物信息
    """
    db_session = session.get_session()
    
    try:
        # 创建动物
        new_animal = animal_crud.create_animal(
            db=db_session,
            name=data.name,
            species=data.species,
            breed=data.breed,
            age=data.age,
            age_category=data.age_category,
            gender=data.gender,
            size=data.size,
            weight=data.weight,
            color=data.color,
            description=data.description,
            personality=data.personality,
            health_status=data.health_status,
            medical_history=data.medical_history,
            is_neutered=data.is_neutered,
            is_vaccinated=data.is_vaccinated,
            vaccination_records=data.vaccination_records,
            special_needs=data.special_needs,
            good_with_kids=data.good_with_kids,
            good_with_pets=data.good_with_pets,
            energy_level=data.energy_level,
            training_level=data.training_level,
            shelter_id=data.shelter_id,
            location=data.location,
            rescue_date=data.rescue_date,
            rescue_story=data.rescue_story,
            adoption_fee=data.adoption_fee
        )
        
        # 重新获取完整信息用于响应
        animal = animal_crud.get_animal_detail_with_images(db_session, new_animal.animal_id)
        
        # 构造响应数据（简化版，没有图片）
        shelter_info = animal_models.ShelterInfo(
            shelter_id=animal.shelter.shelter_id,
            name=animal.shelter.name,
            city=animal.shelter.city,
            phone=animal.shelter.phone,
            address=animal.shelter.address
        ) if animal.shelter else None
        
        animal_data = animal_models.AnimalDetailResponse(
            animal_id=animal.animal_id,
            name=animal.name,
            species=animal.species,
            breed=animal.breed,
            age=animal.age,
            age_category=animal.age_category,
            gender=animal.gender,
            size=animal.size,
            weight=float(animal.weight) if animal.weight else None,
            color=animal.color,
            description=animal.description,
            personality=animal.personality or [],
            health_status=animal.health_status,
            medical_history=animal.medical_history or [],
            is_neutered=animal.is_neutered,
            is_vaccinated=animal.is_vaccinated,
            vaccination_records=animal.vaccination_records or [],
            special_needs=animal.special_needs,
            good_with_kids=animal.good_with_kids,
            good_with_pets=animal.good_with_pets,
            energy_level=animal.energy_level,
            training_level=animal.training_level,
            shelter=shelter_info,
            status=animal.status,
            location=animal.location,
            rescue_date=animal.rescue_date.strftime("%Y-%m-%d") if animal.rescue_date else None,
            rescue_story=animal.rescue_story,
            adoption_fee=float(animal.adoption_fee),
            images=[],
            videos=animal.videos or [],
            ai_features=animal.ai_features or {},
            view_count=animal.view_count,
            favorite_count=animal.favorite_count,
            pending_applications=0,
            created_at=animal.created_at.isoformat() if animal.created_at else None,
            updated_at=animal.updated_at.isoformat() if animal.updated_at else None
        )
        
        return animal_models.AnimalCreateResponse(
            code=200,
            message="创建成功",
            data=animal_data
        )
        
    except Exception as e:
        print(f"Create animal error: {e}")
        return animal_models.AnimalCreateResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def update_animal_func(animal_id: str, data: animal_models.AnimalUpdateRequest):
    """
    更新动物信息
    """
    db_session = session.get_session()
    
    try:
        # 检查动物是否存在
        animal = animal_crud.get_animal_by_id(db_session, animal_id)
        if not animal:
            return animal_models.AnimalUpdateResponse(
                code=404,
                message="动物不存在"
            )
        
        # 准备更新数据
        update_data = {}
        for field, value in data.dict(exclude_unset=True).items():
            update_data[field] = value
        
        # 更新动物信息
        updated_animal = animal_crud.update_animal(db_session, animal_id, update_data)
        if not updated_animal:
            return animal_models.AnimalUpdateResponse(
                code=400,
                message="更新失败"
            )
        
        # 重新获取完整信息
        animal = animal_crud.get_animal_detail_with_images(db_session, animal_id)
        
        # 构造响应数据
        shelter_info = animal_models.ShelterInfo(
            shelter_id=animal.shelter.shelter_id,
            name=animal.shelter.name,
            city=animal.shelter.city,
            phone=animal.shelter.phone,
            address=animal.shelter.address
        ) if animal.shelter else None
        
        images = []
        for img in animal.animal_images:
            images.append(animal_models.AnimalImageInfo(
                image_id=img.image_id,
                url=img.url,
                alt_text=img.alt_text,
                is_primary=img.is_primary,
                sort_order=img.sort_order
            ))
        
        animal_data = animal_models.AnimalDetailResponse(
            animal_id=animal.animal_id,
            name=animal.name,
            species=animal.species,
            breed=animal.breed,
            age=animal.age,
            age_category=animal.age_category,
            gender=animal.gender,
            size=animal.size,
            weight=float(animal.weight) if animal.weight else None,
            color=animal.color,
            description=animal.description,
            personality=animal.personality or [],
            health_status=animal.health_status,
            medical_history=animal.medical_history or [],
            is_neutered=animal.is_neutered,
            is_vaccinated=animal.is_vaccinated,
            vaccination_records=animal.vaccination_records or [],
            special_needs=animal.special_needs,
            good_with_kids=animal.good_with_kids,
            good_with_pets=animal.good_with_pets,
            energy_level=animal.energy_level,
            training_level=animal.training_level,
            shelter=shelter_info,
            status=animal.status,
            location=animal.location,
            rescue_date=animal.rescue_date.strftime("%Y-%m-%d") if animal.rescue_date else None,
            rescue_story=animal.rescue_story,
            adoption_fee=float(animal.adoption_fee),
            images=images,
            videos=animal.videos or [],
            ai_features=animal.ai_features or {},
            view_count=animal.view_count,
            favorite_count=animal.favorite_count,
            pending_applications=0,
            created_at=animal.created_at.isoformat() if animal.created_at else None,
            updated_at=animal.updated_at.isoformat() if animal.updated_at else None
        )
        
        return animal_models.AnimalUpdateResponse(
            code=200,
            message="更新成功",
            data=animal_data
        )
        
    except Exception as e:
        print(f"Update animal error: {e}")
        return animal_models.AnimalUpdateResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def delete_animal_func(animal_id: str):
    """
    删除动物信息
    """
    db_session = session.get_session()
    
    try:
        # 检查动物是否存在
        animal = animal_crud.get_animal_by_id(db_session, animal_id)
        if not animal:
            return animal_models.AnimalDeleteResponse(
                code=404,
                message="动物不存在"
            )
        
        # 删除动物（级联删除图片）
        animal_crud.delete_animal(db_session, animal_id)
        
        return animal_models.AnimalDeleteResponse(
            code=200,
            message="删除成功"
        )
        
    except Exception as e:
        print(f"Delete animal error: {e}")
        return animal_models.AnimalDeleteResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def upload_animal_images_func(animal_id: str, images: List[UploadFile], alt_texts: List[str] = None, is_primary_list: List[bool] = None):
    """
    上传动物图片
    """
    db_session = session.get_session()
    
    try:
        # 检查动物是否存在
        animal = animal_crud.get_animal_by_id(db_session, animal_id)
        if not animal:
            return animal_models.AnimalImageUploadResponse(
                code=404,
                message="动物不存在"
            )
        
        uploaded_images = []
        upload_dir = f"static/animals/{animal_id}"
        os.makedirs(upload_dir, exist_ok=True)
        
        for i, image in enumerate(images):
            # 检查文件类型
            if not image.content_type.startswith('image/'):
                continue
            
            # 生成文件名
            file_extension = image.filename.split('.')[-1] if '.' in image.filename else 'jpg'
            filename = f"{uuid.uuid4().hex}.{file_extension}"
            
            # 保存文件
            file_path = os.path.join(upload_dir, filename)
            with open(file_path, "wb") as buffer:
                content = await image.read()
                buffer.write(content)
            
            # 构造URL
            image_url = f"/static/animals/{animal_id}/{filename}"
            
            # 获取对应的参数
            alt_text = alt_texts[i] if alt_texts and i < len(alt_texts) else None
            is_primary = is_primary_list[i] if is_primary_list and i < len(is_primary_list) else False
            
            # 创建图片记录
            image_record = animal_image_crud.create_animal_image(
                db=db_session,
                animal_id=animal_id,
                url=image_url,
                alt_text=alt_text,
                is_primary=is_primary,
                sort_order=i
            )
            
            uploaded_images.append({
                "image_id": image_record.image_id,
                "url": image_record.url,
                "alt_text": image_record.alt_text,
                "is_primary": image_record.is_primary
            })
        
        return animal_models.AnimalImageUploadResponse(
            code=200,
            message="图片上传成功",
            data={"uploaded_images": uploaded_images}
        )
        
    except Exception as e:
        print(f"Upload images error: {e}")
        return animal_models.AnimalImageUploadResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def get_recommendations_func(user_id: Optional[str] = None, limit: int = 10):
    """
    获取推荐动物
    """
    db_session = session.get_session()
    
    try:
        # 获取推荐动物
        animals = animal_crud.get_recommended_animals(db_session, user_id, limit)
        
        # 构造响应数据
        items = []
        for animal in animals:
            # 获取动物图片
            images = animal_image_crud.get_animal_images(db_session, animal.animal_id)
            image_urls = [img.url for img in images] if images else []
            
            item_data = animal_models.AnimalListItem(
                animal_id=animal.animal_id,
                name=animal.name,
                species=animal.species,
                breed=animal.breed,
                age=animal.age,
                age_category=animal.age_category,
                gender=animal.gender,
                size=animal.size,
                weight=float(animal.weight) if animal.weight else None,
                color=animal.color,
                description=animal.description,
                personality=animal.personality or [],
                health_status=animal.health_status,
                is_neutered=animal.is_neutered,
                is_vaccinated=animal.is_vaccinated,
                good_with_kids=animal.good_with_kids,
                good_with_pets=animal.good_with_pets,
                energy_level=animal.energy_level,
                training_level=animal.training_level,
                shelter_id=animal.shelter_id,
                shelter_name=animal.shelter.name if animal.shelter else None,
                shelter_city=animal.shelter.city if animal.shelter else None,
                status=animal.status,
                rescue_date=animal.rescue_date.strftime("%Y-%m-%d") if animal.rescue_date else None,
                adoption_fee=float(animal.adoption_fee),
                images=image_urls,
                videos=animal.videos or [],
                view_count=animal.view_count,
                favorite_count=animal.favorite_count,
                pending_applications=0,
                created_at=animal.created_at.isoformat() if animal.created_at else None
            )
            items.append(item_data)
        
        return animal_models.AnimalRecommendationsResponse(
            code=200,
            message="获取成功",
            data=items
        )
        
    except Exception as e:
        print(f"Get recommendations error: {e}")
        return animal_models.AnimalRecommendationsResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()
