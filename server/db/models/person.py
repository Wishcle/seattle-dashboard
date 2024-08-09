
from dataclasses import dataclass

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


@dataclass
class Person(Base):
    __tablename__ = "person"
    OBJECTID: Mapped[int] = mapped_column(primary_key=True)
    COLLISIONPSNDETKEY: Mapped[int] = mapped_column()
    COLDETKEY: Mapped[int] = mapped_column()
    Added_date: Mapped[str] = mapped_column("Added date")
    ST_AGE: Mapped[float] = mapped_column()
    ST_ARBG_STAT: Mapped[float] = mapped_column()
    ST_ARBG_STAT_DESC: Mapped[str] = mapped_column()
    ST_ALCHL_TST_RSLTS: Mapped[float] = mapped_column()
    ST_ALCHL_TST_RSLTS_DESC: Mapped[float] = mapped_column()
    ST_CITED: Mapped[str] = mapped_column()
    ST_CLTHNG_VSBLTY: Mapped[float] = mapped_column()
    ST_CLTHNG_VSBLTY_DESC: Mapped[str] = mapped_column()
    ST_CONTRBCIR_CD1: Mapped[float] = mapped_column()
    ST_CONTRBCIR1_DESC: Mapped[str] = mapped_column()
    ST_CONTRBCIR_CD2: Mapped[float] = mapped_column()
    ST_CONTRBCIR2_DESC: Mapped[str] = mapped_column()
    ST_CONTRBCIR_CD3: Mapped[float] = mapped_column()
    ST_CONTRBCIR3_DESC: Mapped[str] = mapped_column()
    ST_DIR_FM: Mapped[float] = mapped_column()
    ST_DIR_FM_DESC: Mapped[str] = mapped_column()
    ST_DIR_TO: Mapped[float] = mapped_column()
    ST_DIR_TO_DESC: Mapped[str] = mapped_column()
    ST_DRE1: Mapped[float] = mapped_column()
    ST_DRE1_DESC: Mapped[str] = mapped_column()
    ST_DRE2: Mapped[float] = mapped_column()
    ST_DRE2_DESC: Mapped[str] = mapped_column()
    ST_DRIVER_MISC_ACT_CD1: Mapped[str] = mapped_column()
    ST_DRIVER_MISC_ACT1_DESC: Mapped[str] = mapped_column()
    ST_DRIVER_MISC_ACT_CD2: Mapped[str] = mapped_column()
    ST_DRIVER_MISC_ACT2_DESC: Mapped[str] = mapped_column()
    ST_DRVR_ACTNS3: Mapped[str] = mapped_column()
    ST_DRVR_ACTNS3_DESC: Mapped[str] = mapped_column()
    ST_EJCTN: Mapped[float] = mapped_column()
    ST_EJCTN_DESC: Mapped[str] = mapped_column()
    ST_GENDER: Mapped[str] = mapped_column()
    ST_GENDER_DESC: Mapped[str] = mapped_column()
    ST_HZMT_IND: Mapped[float] = mapped_column()
    ST_HZMT_IND_DESC: Mapped[str] = mapped_column()
    ST_HELMET: Mapped[float] = mapped_column()
    ST_HELMET_DESC: Mapped[str] = mapped_column()
    ST_INJRY_CLSS: Mapped[float] = mapped_column()
    ST_INJRY_CLSS_DESC: Mapped[str] = mapped_column()
    ST_PARTCPNT_TYPE: Mapped[int] = mapped_column()
    ST_PARTCPNT_TYPE_DESC: Mapped[str] = mapped_column()
    ST_PED_ACT_CD: Mapped[float] = mapped_column()
    ST_PED_ACT_DESC: Mapped[str] = mapped_column()
    ST_PED_TYPE: Mapped[float] = mapped_column()
    ST_PED_TYPE_DESC: Mapped[str] = mapped_column()
    ST_PED_WAS_USING_CD: Mapped[float] = mapped_column()
    ST_PED_WAS_USING_DESC: Mapped[str] = mapped_column()
    ST_RESTRAINT: Mapped[float] = mapped_column()
    ST_RESTRAINT_DESC: Mapped[str] = mapped_column()
    ST_SOBRIETY_CD: Mapped[float] = mapped_column()
    ST_SOBRIETY_DESC: Mapped[str] = mapped_column()
    ST_ST_PSTON: Mapped[float] = mapped_column()
    ST_ST_PSTON_DESC: Mapped[str] = mapped_column()
    ST_UNIT: Mapped[int] = mapped_column()
    SE_ANNO_CAD_DATA: Mapped[str] = mapped_column()
    Source_of_the_collision_report: Mapped[str] = mapped_column("Source of the collision report")
    Source_description: Mapped[str] = mapped_column("Source description")
    Incident_Date: Mapped[str] = mapped_column("Incident Date")
    Incident_Date_Time: Mapped[str] = mapped_column("Incident Date Time")
    Report_Number: Mapped[str] = mapped_column("Report Number")
    Added_by_User: Mapped[str] = mapped_column("Added by User")
    Modified_by: Mapped[float] = mapped_column("Modified by")
    Modified_date: Mapped[float] = mapped_column("Modified date")
    x: Mapped[float] = mapped_column()
    y: Mapped[float] = mapped_column()
