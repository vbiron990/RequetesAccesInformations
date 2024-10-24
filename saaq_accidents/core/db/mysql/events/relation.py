from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from core.db import Events
from core.db.db_orm.relations.relation_base import BaseRelation
from core.db.mysql.car_model.controller import CarModel


class EventsRelation(BaseRelation):

    @classmethod
    def _connect_relation(cls):
        """"""
        Events.car_model = relationship(
            CarModel,
            foreign_keys=Events.car_model_id,
            backref=backref(CarModel.EVENTS_RELATION_NAME)
        )
