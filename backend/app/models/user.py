from beanie import Document, Indexed


class User(Document):
    name: str
    email: str

    class Settings:
        name = "users"