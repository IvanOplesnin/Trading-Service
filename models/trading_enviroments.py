from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base

if TYPE_CHECKING:
    from models import User


class TradingEnvironment(Base):
    __tablename__ = "trading_environments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    api_key: Mapped[str] = mapped_column(nullable=False)
    api_secret: Mapped[str] = mapped_column(nullable=False)
    account_api_id: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["User"] = relationship(back_populates="environments")

    def __repr__(self):
        return f"<TradEnv id={self.id} name={self.name}>"
