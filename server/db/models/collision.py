
from dataclasses import dataclass

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


@dataclass
class Collision(Base):
    __tablename__ = "collision"
    OBJECTID: Mapped[int] = mapped_column(primary_key=True)
    SE_ANNO_CAD_DATA: Mapped[str] = mapped_column()
    INCKEY: Mapped[int] = mapped_column()
    COLDETKEY: Mapped[int] = mapped_column()
    REPORTNO: Mapped[str] = mapped_column()
    STATUS: Mapped[str] = mapped_column()
    ADDRTYPE: Mapped[str] = mapped_column()
    INTKEY: Mapped[float] = mapped_column()
    LOCATION: Mapped[str] = mapped_column()
    EXCEPTRSNCODE: Mapped[str] = mapped_column()
    EXCEPTRSNDESC: Mapped[str] = mapped_column()
    SEVERITYCODE: Mapped[str] = mapped_column()
    SEVERITYDESC: Mapped[str] = mapped_column()
    COLLISIONTYPE: Mapped[str] = mapped_column()
    PERSONCOUNT: Mapped[int] = mapped_column()
    PEDCOUNT: Mapped[int] = mapped_column()
    PEDCYLCOUNT: Mapped[int] = mapped_column()
    VEHCOUNT: Mapped[int] = mapped_column()
    INJURIES: Mapped[int] = mapped_column()
    SERIOUSINJURIES: Mapped[int] = mapped_column()
    FATALITIES: Mapped[int] = mapped_column()
    INCDATE: Mapped[str] = mapped_column()
    INCDTTM: Mapped[str] = mapped_column()
    JUNCTIONTYPE: Mapped[str] = mapped_column()
    SDOT_COLCODE: Mapped[float] = mapped_column()
    SDOT_COLDESC: Mapped[str] = mapped_column()
    INATTENTIONIND: Mapped[str] = mapped_column()
    UNDERINFL: Mapped[str] = mapped_column()
    WEATHER: Mapped[str] = mapped_column()
    ROADCOND: Mapped[str] = mapped_column()
    LIGHTCOND: Mapped[str] = mapped_column()
    DIAGRAMLINK: Mapped[str] = mapped_column()
    REPORTLINK: Mapped[str] = mapped_column()
    PEDROWNOTGRNT: Mapped[str] = mapped_column()
    SDOTCOLNUM: Mapped[float] = mapped_column()
    SPEEDING: Mapped[str] = mapped_column()
    STCOLCODE: Mapped[float] = mapped_column()
    ST_COLDESC: Mapped[str] = mapped_column()
    SEGLANEKEY: Mapped[int] = mapped_column()
    CROSSWALKKEY: Mapped[int] = mapped_column()
    HITPARKEDCAR: Mapped[str] = mapped_column()
    SPDCASENO: Mapped[str] = mapped_column()
    Source_of_the_collision_report: Mapped[str] = mapped_column("Source of the collision report")
    Source_description: Mapped[str] = mapped_column("Source description")
    Added_by_User: Mapped[str] = mapped_column("Added by User")
    Added_date: Mapped[str] = mapped_column("Added date")
    Modified_by: Mapped[str] = mapped_column("Modified by")
    Modified_date: Mapped[str] = mapped_column("Modified date")
    x: Mapped[float] = mapped_column()
    y: Mapped[float] = mapped_column()
