from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from models import ResponseUser


class EnvironmentBase(BaseModel):
    name: str = Field(..., description="The name of the environment.")
    api_key: str = Field(..., description="The Tinkoff access token.")
    account_api_id: str = Field(..., description="Id account in Tinkoff")
    user_id: int = Field(..., description="user ID of the environment host")


class CreateEnvironment(EnvironmentBase):
    pass


class UpdateEnvironment(BaseModel):
    id: int = Field(..., description="The id of the environment to update.")
    name: Optional[str] = Field(..., description="The name of the environment.")
    api_key: Optional[str] = Field(..., description="The Tinkoff access token.")
    account_api_id: Optional[str] = Field(..., description="Id account in Tinkoff")
    user_id: Optional[int] = Field(..., description="user ID of the environment host")


class ReadEnvironment(EnvironmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ResponseEnvironment(BaseModel):
    id: int
    user: "ResponseUser"

    model_config = ConfigDict(from_attributes=True)
