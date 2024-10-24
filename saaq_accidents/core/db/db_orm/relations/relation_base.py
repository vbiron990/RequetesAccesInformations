
class BaseRelation(object):
    relations = dict()
    NO_ACTION_CASCADE = "expunge, refresh-expire"

    @classmethod
    def _connect_relation(cls):
        pass

    @classmethod
    def connect(cls):
        """
        :return:
        """
        if cls.__name__ not in cls.relations:
            cls.relations[cls.__name__] = True
            cls._connect_relation()
