from uuid import UUID

from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

db=[]

class UserCreate(BaseModel):
    username: str
    email: str 

class User(UserCreate):
    id: UUID    

@router.get("/")
def get_users():
    return db #TODO: Implement database retrieval logic

@router.post("/", status_code=201)
def create_user(user: UserCreate):
    new_user = User(id=UUID(int=0), username=user.username, email=user.email) #TODO: Implement UUID generation logic
    db.append(new_user)
    return new_user

@router.get("/{user_id}")
def get_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


    
