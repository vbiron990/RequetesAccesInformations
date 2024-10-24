CONTROLLER_IMPORT_LINE_MARKER = """# Controller imports go below this line\n"""

CONTROLLER_TEMPLATE = """from core.db.mysql.{table_name}.model import {cls_name}Model


class {cls_name}({cls_name}Model):

    def __init__(self):
        super({cls_name}, self).__init__()
"""

MODEL_TEMPLATE = """{sqlalchemy_imports}
{db_constant_imports}
{orm_base_imports}

class {table_name}Model(BaseModel):
    __tablename__ = {table_name}DbConstant.name
    __table_constant__ = {table_name}DbConstant
    {relation_var_names}
    # Relations
    {relation_var_lists}
    {columns}    
"""

DB_CONSTANT_IMPORTS = """from core.contants.db_constant import {table_name}DbConstant"""

ORM_BASE_IMPORTS = """from core.db.db_orm.base import BaseColumn
from core.db.db_orm.base import BaseModel
"""

SQLALCHEMY_IMPORTS = """from sqlalchemy import INTEGER
from sqlalchemy import TIMESTAMP
from sqlalchemy import TEXT
from sqlalchemy import VARCHAR
from sqlalchemy import DATETIME
from sqlalchemy import DATE
"""

COLUMN_TEMPLATE = """{var_name} = BaseColumn(
        {col_type},
        {args}
    )"""

DB_CONSTANT_TEMPLATE = """{cls_name}DbConstant = DbClassConstant("{constant_name}")
"""
RELATION_TEMPLATE = """from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

{controller_imports}
from core.db.db_orm.relations.relation_base import BaseRelation


class {cls_name}Relation(BaseRelation):

    @classmethod
    def _connect_relation(cls):
        """"""
        {cls_name}.{relation_name} = relationship(
            {relation_cls_name},
            foreign_keys={cls_name}.{relation_name}_id,
            backref=backref({relation_cls_name}.COUNTERS_RELATION_NAME)
        )
"""
