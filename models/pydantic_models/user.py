from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

if TYPE_CHECKING:
    from models import ReadEnvironment


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="email address")
    username: str = Field(
        default_factory=lambda data: data["email"], description="username", alias="name"
    )
    admin: bool = Field(False, description="admin status")


class CreateUser(UserBase):
    password: str = Field(..., min_length=8, max_length=64, description="password")


class UpdateUser(BaseModel):
    id: int
    email: Optional[EmailStr] = Field(None, description="email address")
    username: Optional[str] = Field(None, description="username", alias="name")
    admin: Optional[bool] = Field(None, description="admin status")
    password: Optional[str] = Field(
        None, min_length=8, max_length=64, description="new password"
    )


class ReadUser(UserBase):
    id: int = Field(..., description="user id in database")
    list_environments: List["ReadEnvironment"]

    model_config = ConfigDict(from_attributes=True)


class ResponseUser(UserBase):
    id: int = Field(..., description="user id in database")

    model_config = ConfigDict(from_attributes=True)
