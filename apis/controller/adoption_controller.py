import uuid
from typing import Optional
from models import adoption_models
from db import session
from crud import adoption_application_crud, animal_crud

async def submit_adoption_application_func(data: adoption_models.AdoptionApplicationSubmitRequest, user_id: str):
    """
    提交领养申请
    """
    print("==================================================")
    print("submit_adoption_application_func data", data)
    print("==================================================")
    print("submit_adoption_application_func user_id", user_id)
    print("==================================================")
    db_session = session.get_session()
    
    try:
        # 验证动物是否存在且可领养
        animal = animal_crud.get_animal_by_id(db_session, data.animal_id)
        if not animal:
            return adoption_models.AdoptionApplicationSubmitResponse(
                code=404,
                message="动物不存在"
            )
        
        if animal.status != 'available':
            return adoption_models.AdoptionApplicationSubmitResponse(
                code=400,
                message="该动物当前不可领养"
            )
        
        # 检查用户是否已经申请过该动物
        existing_application = adoption_application_crud.get_user_animal_application(
            db_session, user_id, data.animal_id
        )
        if existing_application:
            return adoption_models.AdoptionApplicationSubmitResponse(
                code=400,
                message="您已经申请过该动物"
            )
        
        # 构建申请数据
        application_data = {
            'animal_id': data.animal_id,
            'reason': data.reason,
            'previous_experience': data.previous_experience,
            'living_situation': data.living_situation.dict(),
            'family_info': data.family_info.dict(),
            'veterinarian_info': data.veterinarian_info.dict() if data.veterinarian_info else None,
            'references': [ref.dict() for ref in data.references] if data.references else None
        }
        
        print("构建申请完成")
        
        # 创建申请
        application = adoption_application_crud.create_adoption_application(
            db_session, user_id, **application_data
        )
        
        print("创建申请完成")
        
        # 构造响应数据
        response_data = adoption_models.ApplicationSubmitData(
            application_id=application.application_id,
            animal_id=application.animal_id,
            user_id=application.user_id,
            status=application.status.value if hasattr(application.status, 'value') else str(application.status),
            created_at=application.created_at.isoformat()
        )
        
        print("构造响应数据完成")
        
        return adoption_models.AdoptionApplicationSubmitResponse(
            code=200,
            message="申请提交成功",
            data=response_data
        )
        
    except Exception as e:
        print(f"Submit application error: {e}")
        return adoption_models.AdoptionApplicationSubmitResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def get_adoption_application_func(application_id: str):
    """
    获取领养申请详情
    """
    db_session = session.get_session()
    
    try:
        application = adoption_application_crud.get_application_by_id(db_session, application_id)
        if not application:
            return adoption_models.AdoptionApplicationDetailGetResponse(
                code=404,
                message="申请不存在"
            )
        
        # 构造动物信息
        animal_info = adoption_models.SimpleAnimalInfo(
            animal_id=application.animal.animal_id,
            name=application.animal.name,
            species=application.animal.species,
            breed=application.animal.breed,
            age=application.animal.age,
            size=application.animal.size,
            images=application.animal.images or []
        )
        
        # 构造申请人信息
        applicant_info = adoption_models.SimpleUserInfo(
            user_id=application.user.user_id,
            username=application.user.username,
            name=application.user.name,
            email=application.user.email,
            phone=application.user.phone
        )
        
        # 构造审核人信息
        reviewer_info = None
        if application.reviewer:
            reviewer_info = adoption_models.SimpleUserInfo(
                user_id=application.reviewer.user_id,
                username=application.reviewer.username,
                name=application.reviewer.name,
                email=application.reviewer.email,
                phone=application.reviewer.phone
            )
        
        # 构造响应数据
        detail_data = adoption_models.AdoptionApplicationDetailResponse(
            application_id=application.application_id,
            animal=animal_info,
            applicant=applicant_info,
            status=application.status.value if hasattr(application.status, 'value') else str(application.status),
            reason=application.reason,
            previous_experience=application.previous_experience,
            living_situation=application.living_situation or {},
            family_info=application.family_info or {},
            veterinarian_info=application.veterinarian_info,
            references=application.references,
            home_visit_required=application.home_visit_required,
            home_visit_date=application.home_visit_date.isoformat() if application.home_visit_date else None,
            home_visit_notes=application.home_visit_notes,
            interview_date=application.interview_date.isoformat() if application.interview_date else None,
            interview_notes=application.interview_notes,
            approval_notes=application.approval_notes,
            rejection_reason=application.rejection_reason,
            reviewer=reviewer_info,
            reviewed_at=application.reviewed_at.isoformat() if application.reviewed_at else None,
            created_at=application.created_at.isoformat(),
            updated_at=application.updated_at.isoformat()
        )
        
        return adoption_models.AdoptionApplicationDetailGetResponse(
            code=200,
            message="获取成功",
            data=detail_data
        )
        
    except Exception as e:
        print(f"Get application error: {e}")
        return adoption_models.AdoptionApplicationDetailGetResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def get_adoption_applications_func(
    page: int = 1,
    size: int = 10,
    status: Optional[str] = None,
    animal_id: Optional[str] = None,
    user_id: Optional[str] = None,
    species: Optional[str] = None,
    keyword: Optional[str] = None,
    sort: str = "created_at",
    order: str = "desc"
):
    """
    获取领养申请列表
    """
    db_session = session.get_session()
    
    try:
        result = adoption_application_crud.get_applications_with_pagination(
            db=db_session,
            page=page,
            size=size,
            status=status,
            animal_id=animal_id,
            user_id=user_id,
            species=species,
            keyword=keyword,
            sort_by=sort,
            sort_order=order
        )
        
        # 构造响应数据
        items = []
        for application in result["items"]:
            item_data = adoption_models.AdoptionApplicationListItem(
                application_id=application.application_id,
                animal_name=application.animal.name,
                animal_id=application.animal.animal_id,
                animal_species=application.animal.species,
                applicant_name=application.user.name or application.user.username,
                applicant_id=application.user.user_id,
                status=application.status.value if hasattr(application.status, 'value') else str(application.status),
                reason=application.reason[:100] + "..." if len(application.reason) > 100 else application.reason,
                home_visit_required=application.home_visit_required,
                home_visit_date=application.home_visit_date.isoformat() if application.home_visit_date else None,
                interview_date=application.interview_date.isoformat() if application.interview_date else None,
                created_at=application.created_at.isoformat()
            )
            items.append(item_data)
        
        list_data = adoption_models.AdoptionApplicationListData(
            items=items,
            total=result["total"],
            page=result["page"],
            size=result["size"],
            pages=result["pages"]
        )
        
        return adoption_models.AdoptionApplicationListResponse(
            code=200,
            message="获取成功",
            data=list_data
        )
        
    except Exception as e:
        print(f"Get applications error: {e}")
        return adoption_models.AdoptionApplicationListResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def review_adoption_application_func(
    application_id: str, 
    data: adoption_models.AdoptionApplicationReviewRequest,
    reviewer_id: str
):
    """
    审核领养申请
    """
    db_session = session.get_session()
    
    try:
        # 获取申请
        application = adoption_application_crud.get_application_by_id(db_session, application_id)
        if not application:
            return adoption_models.AdoptionApplicationReviewResponse(
                code=404,
                message="申请不存在"
            )
        
        # 更新申请状态
        update_data = {
            'status': data.status,
            'approval_notes': data.approval_notes,
            'rejection_reason': data.rejection_reason,
            'home_visit_required': data.home_visit_required,
            'interview_date': data.interview_date
        }
        
        updated_application = adoption_application_crud.update_application(
            db_session, application_id, reviewer_id, **update_data
        )
        
        # 如果申请被批准，更新动物状态
        if data.status == 'approved':
            animal_crud.update_animal(db_session, application.animal_id, {'status': 'pending'})
        elif data.status == 'rejected':
            # 如果拒绝，释放动物状态
            animal_crud.update_animal(db_session, application.animal_id, {'status': 'available'})
        
        # 构造响应数据（重用获取详情的逻辑）
        detail_response = await get_adoption_application_func(application_id)
        
        return adoption_models.AdoptionApplicationReviewResponse(
            code=200,
            message="审核完成",
            data=detail_response.data
        )
        
    except Exception as e:
        print(f"Review application error: {e}")
        return adoption_models.AdoptionApplicationReviewResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close()

async def cancel_adoption_application_func(application_id: str, user_id: str):
    """
    取消领养申请
    """
    db_session = session.get_session()
    
    try:
        # 获取申请
        application = adoption_application_crud.get_application_by_id(db_session, application_id)
        if not application:
            return adoption_models.AdoptionApplicationReviewResponse(
                code=404,
                message="申请不存在"
            )
        
        # 验证申请人
        if application.user_id != user_id:
            return adoption_models.AdoptionApplicationReviewResponse(
                code=403,
                message="无权限操作"
            )
        
        # 只能取消待处理或审核中的申请
        if application.status.value not in ['pending', 'under_review']:
            return adoption_models.AdoptionApplicationReviewResponse(
                code=400,
                message="该申请状态无法取消"
            )
        
        # 更新申请状态为已取消
        adoption_application_crud.update_application(
            db_session, application_id, None, status='cancelled'
        )
        
        # 释放动物状态
        animal_crud.update_animal(db_session, application.animal_id, {'status': 'available'})
        
        return adoption_models.AdoptionApplicationReviewResponse(
            code=200,
            message="申请已取消"
        )
        
    except Exception as e:
        print(f"Cancel application error: {e}")
        return adoption_models.AdoptionApplicationReviewResponse(
            code=500,
            message="服务器内部错误"
        )
    finally:
        db_session.close() 