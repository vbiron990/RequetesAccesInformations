import inspect
import sys

from core.db.db_orm.relations.relation_base import BaseRelation

# Relation imports go below this line. Do not remove
from core.db.mysql.events.relation import EventsRelation


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args)
        return cls._instances[cls]


class RelationConnector(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(RelationConnector, self).__init__()
        self.made_relation()

    @classmethod
    def made_relation(cls):
        """"""
        # Dynamic Imports
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj) and BaseRelation in inspect.getmro(obj):
                obj.connect()
