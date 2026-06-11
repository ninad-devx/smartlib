from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import RegisterSchema
from app.utils.security import hash_password
from app.schemas.auth import LoginSchema
from app.utils.security import verify_password
from fastapi import Request
from fastapi.responses import JSONResponse

router=APIRouter()

@router.post("/register")
def register(payload:RegisterSchema,db:Session=Depends(get_db)):
    existing_email=(db.query(User).filter(User.email==payload.email).first())

    if existing_email:
        return{
            "success":False,
            "message":"Email Already Exists"
        }
    

    user=User(
        university_id=payload.university_id,
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        department=payload.department
    )

    db.add(user)
    db.commit()
    return{
        "success":True,
        "message":"Registration Successful"
    }



#login
@router.post('/login')
def login(payload:LoginSchema,request:Request,db:Session=Depends(get_db)):
    user=(db.query(User).filter(User.email==payload.email).first())

    if not user:
        return {
            "success":False,
            "message":"Invalid Credentials"
        }
    
    if not verify_password(payload.password,user.password_hash):
        return {
            "success":False,
            "message":"Invalid Credentials"
        }
    request.session["user_id"]=user.id
    request.session["role"]=user.role
    request.session["name"]=user.name

    if user.role == "student":
     redirect_url = "/student"

    elif user.role == "teacher":
     redirect_url = "/teacher"

    else:
     redirect_url = "/librarian"

    return {
    "success": True,
    "redirect": redirect_url
}


#logout
@router.post("/logout")
def logout(request:Request):
    request.session.clear()

    return {
        "success":True,
        "message":"logged out"
    }

#current user
@router.get("/me")
def me(request:Request):
    user_id=request.session.get("user_id")

    if not user_id:
        return {
            "success":False,
            "message":"not logged in"
        }
    
    return {
        "success":True,
        "user_id":request.session.get("user_id"),
        "role":request.session.get("role"),
        "name":request.session.get("name")
    }