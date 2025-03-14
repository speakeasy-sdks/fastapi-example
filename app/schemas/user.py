from pydantic import BaseModel


class UserResponse(BaseModel):
    userId: str
