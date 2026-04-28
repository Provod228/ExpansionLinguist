from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from models.user import User, UserRole
from models.word import Word
from models.note import Note
from app.auth import get_current_user
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/admin", tags=["admin"])

class RoleUpdate(BaseModel):
    new_role: UserRole

def is_admin(user: User):
    return hasattr(user, "role") and user.role == "admin"
 

@router.get("/set_users", status_code=200)
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
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
def update_role_user(user_id: int, role_data: RoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
         raise HTTPException(status_code=404, detail="User not found")

    user.role = role_data.new_role.value
    db.commit()
    return {"message": f"User {user.username} role changed to {role_data.new_role.value}"}

@router.delete("/users/{user_id}/delete", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": f"User {user.username} deleted"}




# Данный роутер возможно будет использоваться позже и , скорее всего, будет улучшен, так как сейчас
# он показывает ограниченные данные, а именно только количество: слов, пользователей и записей.


# @router.get("/users")
# def get_status(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     if not is_admin(current_user):
#         raise HTTPException(status_code=403, detail="Admin access required")
    
#     total_users = db.query(User).count()
#     total_words = db.query(Word).count()
#     total_notes = db.query(Note).count()
    
#     return {
#         "total_users": total_users,
#         "total_words": total_words,
#         "total_notes": total_notes
#     }
