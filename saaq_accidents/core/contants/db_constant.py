from core.contants.base import BaseConstant


class DbClassConstant(BaseConstant):
    def __init__(self, name):
        super(DbClassConstant, self).__init__(name)

    @property
    def db_class(self):
        return self._value


EventsDbConstant = DbClassConstant("events")
CarModelDbConstant = DbClassConstant("car_model")
