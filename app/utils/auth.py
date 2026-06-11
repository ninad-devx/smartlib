from fastapi import Request
from fastapi import HTTPException

def require_login(request:Request):
    user_id=request.session.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="login required"
        )
    
    return user_id

def require_role(request:Request,allowed_roles:list):
    role=request.session.get("role")

    if role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )
    return role

