from fastapi import HTTPException
from repositories.user_repository import user_repository
from schemas.user import CreateUser, UpdatedUser


class UserService:
    async def get_all(self):
        return await user_repository.get_all()

    async def get_by_id(self, user_id: str):
        return await user_repository.get_by_id(user_id)

    async def create(self, new_user: CreateUser):
        existing_user = await user_repository.get_by_email(new_user.email)
        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="User with that email already exists",
            )
        await user_repository.create(new_user.model_dump())
        return {"message": "User created"}

    async def update(self, user_id: str, data: UpdatedUser):
        user = await user_repository.get_by_id(user_id)
        if user is None:
            return None
        existing_email = await user_repository.get_by_email(data.email)
        if existing_email and str(existing_email["_id"]) != user_id:
            raise HTTPException(
                status_code=409,
                detail="Cannot use duplicate emails",
            )
        return await user_repository.update(user_id, data.model_dump())

    async def delete(self, user_id: str):
        if await user_repository.get_by_id(user_id) is None:
            return None
        return await user_repository.delete(user_id)


user_service = UserService()