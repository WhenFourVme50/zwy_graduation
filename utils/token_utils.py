import base64
import json
import hmac
import hashlib
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os

# 配置
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here-change-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 30

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        **data,
        "exp": int(expire.timestamp()),
        "type": "access",
        "iat": int(datetime.utcnow().timestamp())
    }
    
    return _encode_token(payload)

def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建刷新令牌
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        **data,
        "exp": int(expire.timestamp()),
        "type": "refresh",
        "iat": int(datetime.utcnow().timestamp())
    }
    
    return _encode_token(payload)

def _encode_token(payload: Dict[str, Any]) -> str:
    """
    编码令牌
    """
    # 编码payload
    payload_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode().rstrip('=')
    
    # 创建签名
    signature = hmac.new(
        SECRET_KEY.encode(),
        payload_b64.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return f"{payload_b64}.{signature}"

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    验证令牌
    """
    try:
        if not token or '.' not in token:
            return None
            
        parts = token.split('.')
        if len(parts) != 2:
            return None
        
        payload_b64, signature = parts
        
        # 验证签名
        expected_signature = hmac.new(
            SECRET_KEY.encode(),
            payload_b64.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            print("Invalid token signature")
            return None
        
        # 解码payload
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += '=' * padding
        
        payload_json = base64.urlsafe_b64decode(payload_b64).decode()
        payload = json.loads(payload_json)
        
        # 检查过期时间
        current_time = int(datetime.utcnow().timestamp())
        if payload.get("exp", 0) < current_time:
            print("Token has expired")
            return None
        
        return payload
        
    except Exception as e:
        print(f"Token verification error: {e}")
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