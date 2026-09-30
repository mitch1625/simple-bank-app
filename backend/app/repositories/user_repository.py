from bson import ObjectId
from bson.errors import InvalidId
from database import user_collection


class UserRepository:
    async def get_all(self):
        return await user_collection.find().to_list(length=None)

    async def get_by_id(self, user_id: str):
        try:
            user_oid = ObjectId(user_id)
        except (InvalidId, TypeError):
            return None
        return await user_collection.find_one({"_id": user_oid})

    async def get_by_email(self, email: str):
        return await user_collection.find_one({"email": email})

    async def create(self, user: dict):
        return await user_collection.insert_one(user)

    async def update(self, user_id: str, data: dict):
        user = await self.get_by_id(user_id)
        if user is None:
            return None
        user_oid = user["_id"]
        await user_collection.update_one({"_id": user_oid}, {"$set": data})
        return await user_collection.find_one({"_id": user_oid})

    async def delete(self, user_id: str):
        user = await self.get_by_id(user_id)
        if user is None:
            return False
        result = await user_collection.delete_one({"_id": user["_id"]})
        return result.deleted_count == 1


user_repository = UserRepository()