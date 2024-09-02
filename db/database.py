from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from db.config import db_settings

engine = create_async_engine(
    url=db_settings.url,
    echo=False,
)
test_engine = create_async_engine(
    url=db_settings.test_url, 
    echo=False
)

session_factory = async_sessionmaker(engine)
test_session_factory = async_sessionmaker(test_engine)


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = ()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
