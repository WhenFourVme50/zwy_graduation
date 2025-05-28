from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import jwt_utils
from crud import user_crud
from db import session

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    获取当前用户（用于需要认证的接口）
    """
    token = credentials.credentials
    payload = jwt_utils.decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="无效的访问令牌")
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="令牌格式错误")
    
    # 获取用户信息
    db_session = session.get_session()
    try:
        user = user_crud.get_user_by_id(db_session, user_id)
        if not user or user.status != 'active':
            raise HTTPException(status_code=401, detail="用户不存在或已被禁用")
        return user
    finally:
        db_session.close()

async def get_current_active_user(current_user = Depends(get_current_user)):
    """
    获取当前活跃用户
    """
    if current_user.status != 'active':
        raise HTTPException(status_code=400, detail="用户账户已被禁用")
    return current_user

async def require_admin(current_user = Depends(get_current_user)):
    """
    要求管理员权限
    """
    if current_user.user_type not in ['system_admin', 'shelter_admin']:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user 