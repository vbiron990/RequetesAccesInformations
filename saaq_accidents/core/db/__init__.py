import inspect
import sys

from core.db.db_orm.base import CoolBase
# Controller imports go below this line
from core.db.mysql.events.controller import Events
from core.db.mysql.car_model.controller import CarModel


from core.db.db_orm.relations.base import RelationConnector
RelationConnector()


# Fill Constant With Real Db Class
def map_constant():
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and CoolBase in inspect.getmro(obj):
            if obj.__table_constant__:
                obj.__table_constant__.value = obj


map_constant()
