import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os

# JWT配置
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1小时
REFRESH_TOKEN_EXPIRE_DAYS = 30    # 30天

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        # 在某些版本的PyJWT中，encode返回bytes，需要转换为string
        if isinstance(encoded_jwt, bytes):
            encoded_jwt = encoded_jwt.decode('utf-8')
        return encoded_jwt
    except Exception as e:
        print(f"JWT encode error: {e}")
        raise e

def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建刷新令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        # 在某些版本的PyJWT中，encode返回bytes，需要转换为string
        if isinstance(encoded_jwt, bytes):
            encoded_jwt = encoded_jwt.decode('utf-8')
        return encoded_jwt
    except Exception as e:
        print(f"JWT encode error: {e}")
        raise e

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    验证令牌
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None  # 令牌已过期
    except jwt.InvalidTokenError:  # 使用 InvalidTokenError 替代 JWTError
        print("Invalid token")
        return None  # 令牌无效
    except jwt.DecodeError:  # 添加 DecodeError 处理
        print("Token decode error")
        return None
    except jwt.InvalidSignatureError:  # 添加签名错误处理
        print("Invalid token signature")
        return None
    except Exception as e:
        print(f"JWT decode error: {e}")
        return None

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    解码访问令牌
    """
    payload = verify_token(token)
    if payload and payload.get("type") == "access":
        return payload
    return None

def decode_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """
    解码刷新令牌
    """
    payload = verify_token(token)
    if payload and payload.get("type") == "refresh":
        return payload
    return None

def get_user_id_from_token(token: str) -> Optional[str]:
    """
    从令牌中获取用户ID
    """
    payload = decode_access_token(token)
    if payload:
        return payload.get("user_id")
    return None 