from fastapi import APIRouter, HTTPException
from schemas.user import CreateUser, UpdatedUser, User
from services.user_service import user_service


router = APIRouter(prefix="/api")


@router.get("/users", response_model=list[User], status_code=200)
async def get_all_users():
    return await user_service.get_all()


@router.get("/users/{user_id}", response_model=User, status_code=200)
async def get_user_by_id(user_id: str):
    user = await user_service.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users", status_code=201)
async def create_user(new_user: CreateUser):
    return await user_service.create(new_user)


@router.put("/users/{user_id}", response_model=User, status_code=200)
async def update_user(user_id: str, user: UpdatedUser):
    updated = await user_service.update(user_id, user)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: str):
    if not await user_service.delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")