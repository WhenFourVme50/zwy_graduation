from typing import Dict, Optional
from models import shelter_models
from db import session
from crud import shelter_crud

async def get_shelters_func(
    page: int = 1,
    size: int = 10,
    city: Optional[str] = None,
    province: Optional[str] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None
):
    """
    获取救助站列表
    """
    db_session = session.get_session()
    
    try:
        # 获取分页数据
        result = shelter_crud.get_shelters_with_pagination(
            db=db_session,
            page=page,
            size=size,
            city=city,
            province=province,
            status=status,
            keyword=keyword
        )
        
        # 构造响应数据
        items = []
        for shelter in result["items"]:
            item_data = shelter_crud.get_shelter_with_stats(db_session, shelter)
            items.append(shelter_models.ShelterListItem(**item_data))
        
        list_data = shelter_models.ShelterListData(
            items=items,
            total=result["total"],
            page=result["page"],
            size=result["size"],
            pages=result["pages"]
        )
        
        return shelter_models.ShelterListResponse(
            code=200,
            message="获取成功",
            data=list_data
        )
        
    except Exception as e:
        print(f"Get shelters error: {e}")
        return shelter_models.ShelterListResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def get_shelter_func(shelter_id: str):
    """
    获取救助站详情
    """
    db_session = session.get_session()
    
    try:
        # 获取救助站信息
        shelter = shelter_crud.get_shelter_by_id(db_session, shelter_id)
        if not shelter:
            return shelter_models.ShelterGetResponse(
                code=404,
                message="救助站不存在"
            )
        
        # 构造响应数据
        shelter_data = shelter_models.ShelterDetailResponse(
            shelter_id=shelter.shelter_id,
            name=shelter.name,
            description=shelter.description,
            address=shelter.address,
            city=shelter.city,
            province=shelter.province,
            postal_code=shelter.postal_code,
            phone=shelter.phone,
            email=shelter.email,
            website=shelter.website,
            license_number=shelter.license_number,
            capacity=shelter.capacity,
            current_animals=shelter.current_animals,
            established_date=shelter.established_date.strftime("%Y-%m-%d") if shelter.established_date else None,
            status=shelter.status,
            logo_url=shelter.logo_url,
            images=shelter.images or [],
            operating_hours=shelter.operating_hours or {},
            services=shelter.services or [],
            created_at=shelter.created_at.isoformat() if shelter.created_at else None
        )
        
        return shelter_models.ShelterGetResponse(
            code=200,
            message="获取成功",
            data=shelter_data
        )
        
    except Exception as e:
        print(f"Get shelter error: {e}")
        return shelter_models.ShelterGetResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def create_shelter_func(data: shelter_models.ShelterCreateRequest):
    """
    创建救助站
    """
    db_session = session.get_session()
    
    try:
        # 创建救助站
        new_shelter = shelter_crud.create_shelter(
            db=db_session,
            name=data.name,
            description=data.description,
            address=data.address,
            city=data.city,
            province=data.province,
            postal_code=data.postal_code,
            phone=data.phone,
            email=data.email,
            website=data.website,
            license_number=data.license_number,
            capacity=data.capacity or 0,
            established_date=data.established_date,
            operating_hours=data.operating_hours,
            services=data.services
        )
        
        # 构造响应数据
        shelter_data = shelter_models.ShelterDetailResponse(
            shelter_id=new_shelter.shelter_id,
            name=new_shelter.name,
            description=new_shelter.description,
            address=new_shelter.address,
            city=new_shelter.city,
            province=new_shelter.province,
            postal_code=new_shelter.postal_code,
            phone=new_shelter.phone,
            email=new_shelter.email,
            website=new_shelter.website,
            license_number=new_shelter.license_number,
            capacity=new_shelter.capacity,
            current_animals=new_shelter.current_animals,
            established_date=new_shelter.established_date.strftime("%Y-%m-%d") if new_shelter.established_date else None,
            status=new_shelter.status,
            logo_url=new_shelter.logo_url,
            images=new_shelter.images or [],
            operating_hours=new_shelter.operating_hours or {},
            services=new_shelter.services or [],
            created_at=new_shelter.created_at.isoformat() if new_shelter.created_at else None
        )
        
        return shelter_models.ShelterCreateResponse(
            code=200,
            message="创建成功",
            data=shelter_data
        )
        
    except Exception as e:
        print(f"Create shelter error: {e}")
        return shelter_models.ShelterCreateResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def update_shelter_func(shelter_id: str, data: shelter_models.ShelterUpdateRequest):
    """
    更新救助站信息
    """
    db_session = session.get_session()
    
    try:
        # 检查救助站是否存在
        shelter = shelter_crud.get_shelter_by_id(db_session, shelter_id)
        if not shelter:
            return shelter_models.ShelterUpdateResponse(
                code=404,
                message="救助站不存在"
            )
        
        # 准备更新数据
        update_data = {}
        for field, value in data.dict(exclude_unset=True).items():
            update_data[field] = value
        
        # 更新救助站信息
        updated_shelter = shelter_crud.update_shelter(db_session, shelter_id, update_data)
        if not updated_shelter:
            return shelter_models.ShelterUpdateResponse(
                code=400,
                message="更新失败"
            )
        
        # 构造响应数据
        shelter_data = shelter_models.ShelterDetailResponse(
            shelter_id=updated_shelter.shelter_id,
            name=updated_shelter.name,
            description=updated_shelter.description,
            address=updated_shelter.address,
            city=updated_shelter.city,
            province=updated_shelter.province,
            postal_code=updated_shelter.postal_code,
            phone=updated_shelter.phone,
            email=updated_shelter.email,
            website=updated_shelter.website,
            license_number=updated_shelter.license_number,
            capacity=updated_shelter.capacity,
            current_animals=updated_shelter.current_animals,
            established_date=updated_shelter.established_date.strftime("%Y-%m-%d") if updated_shelter.established_date else None,
            status=updated_shelter.status,
            logo_url=updated_shelter.logo_url,
            images=updated_shelter.images or [],
            operating_hours=updated_shelter.operating_hours or {},
            services=updated_shelter.services or [],
            created_at=updated_shelter.created_at.isoformat() if updated_shelter.created_at else None
        )
        
        return shelter_models.ShelterUpdateResponse(
            code=200,
            message="更新成功",
            data=shelter_data
        )
        
    except Exception as e:
        print(f"Update shelter error: {e}")
        return shelter_models.ShelterUpdateResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def get_shelter_statistics_func(shelter_id: str):
    """
    获取救助站统计信息
    """
    db_session = session.get_session()
    
    try:
        # 获取统计信息
        statistics = shelter_crud.get_shelter_statistics(db_session, shelter_id)
        if statistics is None:
            return shelter_models.ShelterStatisticsResponse(
                code=404,
                message="救助站不存在"
            )
        
        # 构造响应数据
        stats_data = shelter_models.ShelterStatisticsData(**statistics)
        
        return shelter_models.ShelterStatisticsResponse(
            code=200,
            message="获取成功",
            data=stats_data
        )
        
    except Exception as e:
        print(f"Get shelter statistics error: {e}")
        return shelter_models.ShelterStatisticsResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()
