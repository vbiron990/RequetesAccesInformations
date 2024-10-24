import pickle
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import or_
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.elements import UnaryExpression, BinaryExpression
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config.base import DatabaseAPIKeysConfig
from core.logger.base import logger

DB_NAME = DatabaseAPIKeysConfig.get_config_by_name(DatabaseAPIKeysConfig.DB_NAME)
DB_URL = DatabaseAPIKeysConfig.get_config_by_name(DatabaseAPIKeysConfig.URL)

engine = create_engine(DB_URL)
connection = engine.connect()


class CoolBase(object):
    __tablename__ = None
    __table_constant__ = None
    _session = None

    def __init__(self, *args, **kwargs):
        super(CoolBase, self).__init__(*args, **kwargs)

    def __str__(self):
        return u"\n{}: \n{}".format(
            self.__class__.__name__,
            self._info()
        )

    def _info(self):
        """"""
        data = list()
        for _ in sorted(self.__table__.columns, key=lambda x: x.get_cls_attribute_name()):
            result = getattr(self, _.get_cls_attribute_name())
            data.append(u"\t{} = {}".format(_.get_cls_attribute_name(), result))
        return "\t\n".join(data)

    @classmethod
    def query(
            cls,
            query_with=None,
            limit_keys=None
    ):
        """"""
        session = cls.get_session()

        if query_with is None:
            query_with = list()

        if not isinstance(limit_keys, UnaryExpression):
            limit_keys = [cls] if not limit_keys else limit_keys
        else:
            limit_keys = limit_keys if isinstance(limit_keys, list) else [limit_keys]

        if isinstance(query_with, BinaryExpression):
            return session.query(*limit_keys).filter(query_with)
        elif isinstance(query_with, (list, tuple)):
            return session.query(*limit_keys).filter(*query_with)

    @classmethod
    def get(cls, *args, **kwargs):
        """"""
        cursor = cls.query(*args, **kwargs)
        return cls.assign_options_to_cursor(cursor)

    @classmethod
    def assign_options_to_cursor(cls, cursor):
        """"""
        return cursor.options()

    @classmethod
    def get_one(cls, *args, **kwargs):
        cursor = cls.query(*args, **kwargs)
        data = cls.assign_options_to_cursor(cursor)

        if data:
            return data.first()

    @classmethod
    def search(cls, word):
        """"""
        id_column = getattr(cls, "id")
        item = cls.get_one(
            or_(
                id_column == word
            )
        )
        if item:
            return item

    def add(self, auto_commit=True):
        session = self.get_session()
        item = session.merge(self)
        session.add(item)

        if auto_commit:
            self.commit()

        return self

    def delete(self, auto_commit=True):
        """"""
        session = self.get_session()
        session.delete(self)

        if auto_commit:
            self.commit()

    @classmethod
    def commit(cls):
        """"""
        session = cls.get_session()
        session.commit()
        # cls._session = None

    @classmethod
    def flush(cls):
        """"""
        session = cls.get_session()
        session.flush()

    @classmethod
    def get_session(cls):
        """"""
        if not cls._session:
            Session = sessionmaker(
                bind=engine,
            )
            cls._session = Session()
        return cls._session

    @classmethod
    def bulk_insert_mappings(cls, data_set, auto_commit=True):
        """"""
        if not data_set:
            return

        logger.info("Committing new {} {}...".format(len(data_set), cls.__tablename__.title()))
        session = cls.get_session()
        session.bulk_insert_mappings(
            cls,
            data_set
        )
        if auto_commit:
            cls.commit()

    @classmethod
    def bulk_update_mappings(cls, data_set, auto_commit=True):
        """"""
        if not data_set:
            return

        logger.info("Committing existing {} {}...".format(len(data_set), cls.__tablename__.title()))
        session = cls.get_session()
        session.bulk_update_mappings(
            cls,
            data_set
        )
        if auto_commit:
            cls.commit()

    @classmethod
    def _add_entry_data(cls, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        logger.error("_add_entry_data Need to be re-implemented")

    @classmethod
    def add_entry(cls, *args, **kwargs):
        """
        For args, kwargs, need to check for each class what function need to create entry
        :param args:
        :param kwargs:
        :return:
        """
        auto_commit = kwargs.pop("auto_commit", True)
        auto_add = kwargs.pop("auto_add", True)

        inst = cls._add_entry_data(*args, **kwargs)
        if not inst:
            return None

        if auto_add:
            inst.add(auto_commit=auto_commit)
        return inst

    @classmethod
    def from_json(cls, json_file, inst=None):
        """"""
        if inst is None:
            inst = cls()

        for k, v in json_file.items():
            column = cls.__table__.columns.get(k)
            if column is None:
                continue

            db_cls_attribute = column.get_cls_attribute_name()
            if db_cls_attribute is not None and v is not None:
                try:
                    v = datetime.strptime(v, '%d/%m/%Y')
                except:
                    v = v
                if isinstance(v, (list, tuple)):
                    v = pickle.dumps(v)
                setattr(inst, db_cls_attribute, v)

        return inst


class BaseColumn(Column):
    inherit_cache = True

    def __init__(
            self,
            *args, **kwargs
    ):
        self._cls_attribute = kwargs.pop("cls_attribute", None)
        super(BaseColumn, self).__init__(*args, **kwargs)

    def get_cls_attribute_name(self):
        if self.cls_attribute is None:
            return self.name
        return self.cls_attribute

    @property
    def cls_attribute(self):
        return self._cls_attribute

    @cls_attribute.setter
    def cls_attribute(self, value):
        self._cls_attribute = value

    @classmethod
    def create_table_from_model(cls):
        """"""
        cls.__table__.create(engine)


BaseModel = declarative_base(cls=CoolBase)


def init_db():
    """"""
    BaseModel.metadata.create_all(engine)
    #
    # for cls in BaseModel.registry._class_registry.values():
    #      if hasattr(cls, 'create_default_data'):
    #         cls.create_default_data()
