from typing import TYPE_CHECKING, Any, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

if TYPE_CHECKING:
    from models import ReadEnvironment


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="email address")
    username: Optional[str] = Field(None, description="username", alias="name")
    admin: bool = Field(False, description="admin status")

    @model_validator(mode="before")
    @classmethod
    def set_username(cls, data: dict[str, Any]) -> dict[str, Any]:
        if "username" not in data:
            data["username"] = data["email"]
        return data


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


class ResponseUser(UserBase):
    id: int = Field(..., description="user id in database")
    environments: List["ReadEnvironment"] = Field(
        default_factory=list, alias="list_environments"
    )

    model_config = ConfigDict(from_attributes=True)


class ReadUser(UserBase):
    id: int = Field(..., description="user id in database")

    model_config = ConfigDict(from_attributes=True)
