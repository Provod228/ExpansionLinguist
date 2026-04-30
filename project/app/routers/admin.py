from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from models.user import User, UserRole
from service.auth import get_current_user, is_admin
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])

class RoleUpdate(BaseModel):
    new_role: UserRole


@router.get("/set_users", status_code=200)
async def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "nickname": u.nickname,
            "created_at": u.created_at,
            "role" : u.role
        }
        for u in users
    ]

@router.put("/users/{user_id}/role", status_code=204)
async def update_user_role(user_id: int, role_data: RoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
         raise HTTPException(status_code=404, detail="User not found")

    user.role = role_data.new_role.value
    db.commit()
    return {"message": f"User {user.username} role changed to {role_data.new_role.value}"}

@router.delete("/users/{user_id}/delete", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": f"User {user.username} deleted"}





