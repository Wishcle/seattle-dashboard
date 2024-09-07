
from dataclasses import dataclass

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


@dataclass
class Intersection(Base):
    __tablename__ = "intersection"
    LOCATION: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    x: Mapped[float] = mapped_column(primary_key=True, nullable=False)
    y: Mapped[float] = mapped_column(primary_key=True, nullable=False)

    # total counts here for now.
    # may move to another table with entries by year.
    # when that happens, we'll also split by ped/bike/etc.
    INJURIES: Mapped[int] = mapped_column()
    SERIOUSINJURIES: Mapped[int] = mapped_column()
    FATALITIES: Mapped[int] = mapped_column()
    COLLISIONS: Mapped[int] = mapped_column()
