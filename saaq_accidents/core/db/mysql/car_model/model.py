from sqlalchemy import INTEGER
from sqlalchemy import TIMESTAMP
from sqlalchemy import TEXT
from sqlalchemy import VARCHAR
from sqlalchemy import DATETIME
from sqlalchemy import DATE

from core.contants.db_constant import CarModelDbConstant
from core.db.db_orm.base import BaseColumn
from core.db.db_orm.base import BaseModel


class CarModelModel(BaseModel):
    __tablename__ = CarModelDbConstant.name
    __table_constant__ = CarModelDbConstant
    
    # Relations
    EVENTS_RELATION_NAME = "events"

    id = BaseColumn(
        INTEGER,
        cls_attribute="id",
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    car_type = BaseColumn(
        TEXT(255),
        cls_attribute="car_type"
    )
    brand = BaseColumn(
        TEXT(255),
        cls_attribute="brand"
    )
    model = BaseColumn(
        TEXT(255),
        cls_attribute="model"
    )
    cylindrical = BaseColumn(
        INTEGER,
        cls_attribute="cylindrical"
    )
    year = BaseColumn(
        INTEGER,
        cls_attribute="year"
    )
    sequential_number = BaseColumn(
        INTEGER,
        cls_attribute="sequential_number"
    )
