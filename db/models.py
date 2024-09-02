import datetime
from typing import Annotated

from sqlalchemy import Index, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime,
    mapped_column(
        default=datetime.datetime.now()  # datetime.UTC)
    ),
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        default=datetime.datetime.now(),  # datetime.UTC),
        onupdate=datetime.datetime.now(),  # datetime.UTC),
    ),
]


class User(Base):
    __tablename__ = "users"

    id: Mapped[pk]
    username: Mapped[str]

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="owner",
        cascade="all, delete",
        passive_deletes=True,
        order_by="Task.due.asc()",
    )

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    __table_args__ = (
        Index("username_index", "username"),
        UniqueConstraint("username", name="username_unique_constraint"),
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[pk]

    text: Mapped[str]
    due: Mapped[datetime.datetime]
    done: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["User"] = relationship(
        back_populates="tasks",
    )

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    __table_args__ = (Index("due_index", "due"),)
