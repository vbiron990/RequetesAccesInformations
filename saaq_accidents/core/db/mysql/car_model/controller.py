from core.db.mysql.car_model.model import CarModelModel


class CarModel(CarModelModel):

    def __init__(self):
        super(CarModel, self).__init__()

    @classmethod
    def _add_entry_data(
            cls,
            sequential_number=None,
            car_type=None,
            brand=None,
            model=None,
            cylindrical=None,
            year=None,
    ):
        """"""
        inst = cls()
        inst.sequential_number = sequential_number
        inst.car_type = car_type
        inst.brand = brand
        inst.model = model
        inst.cylindrical = cylindrical
        inst.year = year
        return inst
