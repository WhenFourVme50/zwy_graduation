from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from sqlalchemy.orm import Session
from utils.jwt_utils import decode_access_token
from schemas.user_schema import User
from db import session

# HTTP Bearer 安全方案
security = HTTPBearer()

class CurrentUser:
    """当前用户信息"""
    def __init__(self, user_id: str, username: str, email: str, user_type: str, name: str = None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.user_type = user_type
        self.name = name

def get_current_user_from_token(token: str, db: Session) -> Optional[CurrentUser]:
    """
    从令牌获取当前用户信息
    """
    try:
        # 解码令牌
        payload = decode_access_token(token)
        if not payload:
            return None
        
        user_id = payload.get("user_id")
        if not user_id:
            return None
        
        # 从数据库获取用户信息
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None
        
        # 检查用户状态
        if user.status != 'active':
            return None
        
        return CurrentUser(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            user_type=user.user_type.value if hasattr(user.user_type, 'value') else str(user.user_type),
            name=user.name
        )
        
    except Exception as e:
        print(f"Get current user error: {e}")
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> CurrentUser:
    """
    获取当前用户（FastAPI依赖项）
    """
    token = credentials.credentials
    db = session.get_session()
    
    try:
        current_user = get_current_user_from_token(token, db)
        if not current_user:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return current_user
    finally:
        db.close()

def get_optional_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[CurrentUser]:
    """
    获取可选的当前用户（不要求必须登录）
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    db = session.get_session()
    
    try:
        return get_current_user_from_token(token, db)
    finally:
        db.close()

def require_admin(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """
    要求管理员权限
    """
    if current_user.user_type not in ['shelter_admin', 'system_admin']:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions"
        )
    return current_user

def require_system_admin(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """
    要求系统管理员权限
    """
    if current_user.user_type != 'system_admin':
        raise HTTPException(
            status_code=403,
            detail="System admin permissions required"
        )
    return current_user

def require_shelter_admin(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """
    要求救助站管理员权限
    """
    if current_user.user_type not in ['shelter_admin', 'system_admin']:
        raise HTTPException(
            status_code=403,
            detail="Shelter admin permissions required"
        )
    return current_user

def check_user_access(user_id: str, current_user: CurrentUser) -> bool:
    """
    检查用户是否有权限访问指定用户的数据
    """
    # 用户自己或管理员可以访问
    return (current_user.user_id == user_id or 
            current_user.user_type in ['shelter_admin', 'system_admin'])

def check_shelter_access(shelter_id: str, current_user: CurrentUser, db: Session) -> bool:
    """
    检查用户是否有权限访问指定救助站的数据
    """
    # 系统管理员可以访问所有救助站
    if current_user.user_type == 'system_admin':
        return True
    
    # 救助站管理员只能访问自己管理的救助站
    if current_user.user_type == 'shelter_admin':
        # 这里需要查询救助站管理员关联表
        # 暂时简化处理，实际应该查询 shelter_admins 表
        return True  # TODO: 实现实际的权限检查
    
    return False

def extract_token_from_header(authorization: str) -> Optional[str]:
    """
    从Authorization头部提取令牌
    """
    if not authorization:
        return None
    
    if not authorization.startswith("Bearer "):
        return None
    
    return authorization[7:]  # 移除 "Bearer " 前缀 