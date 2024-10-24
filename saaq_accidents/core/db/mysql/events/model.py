from sqlalchemy import ForeignKey
from sqlalchemy import INTEGER
from sqlalchemy import TIMESTAMP
from sqlalchemy import TEXT
from sqlalchemy import VARCHAR
from sqlalchemy import DATETIME
from sqlalchemy import DATE

from core.contants.db_constant import EventsDbConstant
from core.db.db_orm.base import BaseColumn
from core.db.db_orm.base import BaseModel


class EventsModel(BaseModel):
    __tablename__ = EventsDbConstant.name
    __table_constant__ = EventsDbConstant
    
    # Relations
    
    id = BaseColumn(
        INTEGER,
        cls_attribute="id",
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    sequential_number = BaseColumn(
        INTEGER,
        cls_attribute="sequential_number"
    )
    gravity = BaseColumn(
        TEXT(255),
        cls_attribute="gravity"
    )
    user_type = BaseColumn(
        TEXT(255),
        cls_attribute="user_type"
    )
    car_model_id = BaseColumn(
        "car_model_id",
        INTEGER,
        ForeignKey("car_model.id")
    )
