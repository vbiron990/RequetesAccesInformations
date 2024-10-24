import os
from pathlib import Path

from sqlalchemy import create_engine

from core.db.db_orm.base import DB_NAME
from core.db.db_orm.base import DB_URL
from sqlalchemy import inspect

from core.db.model_generator.templates import COLUMN_TEMPLATE
from core.db.model_generator.templates import CONTROLLER_IMPORT_LINE_MARKER
from core.db.model_generator.templates import CONTROLLER_TEMPLATE
from core.db.model_generator.templates import DB_CONSTANT_IMPORTS
from core.db.model_generator.templates import DB_CONSTANT_TEMPLATE
from core.db.model_generator.templates import MODEL_TEMPLATE
from core.db.model_generator.templates import ORM_BASE_IMPORTS
from core.db.model_generator.templates import RELATION_TEMPLATE
from core.db.model_generator.templates import SQLALCHEMY_IMPORTS
from core.logger.base import logger


class TableGenerator:
    DB_URL = None
    DB_NAME = None
    MODEL_FILENAME = "model.py"
    CONTROLLER_FILENAME = "controller.py"
    RELATION_FILENAME = "relation.py"

    CORE_BASE_DIR = Path(__file__).resolve().parent.parent.parent
    RELATION_BASE_MODULE = os.path.join(
        CORE_BASE_DIR,
        "db/db_orm/relations/base.py"
    )
    MYSQL_MODULE = os.path.join(
        CORE_BASE_DIR,
        "db/mysql/{table_name}"
    )
    DB_CONSTANT_MODULE = os.path.join(
        CORE_BASE_DIR,
        "contants/db_constant.py"
    )
    CONTROLLER_IMPORTS_INIT_MODULE = os.path.join(
        CORE_BASE_DIR,
        "db/__init__.py"
    )

    @classmethod
    def _get_output_file(cls, table_name):
        """"""
        table_dir = cls.MYSQL_MODULE.format(table_name=table_name)

        if not os.path.exists(table_dir):
            os.makedirs(table_dir)

        return table_dir

    @classmethod
    def get_file(cls, table_name, file_name):
        """"""
        outfile = os.path.join(
            cls._get_output_file(table_name),
            file_name
        )

        if os.path.exists(outfile):
            logger.error(
                f"{file_name} already exists. Aborting to prevent overwriting it."
            )
            return outfile
        else:
            fp = open(outfile, "w")
            fp.close()

        return outfile

    @classmethod
    def build_model(cls, table_name):
        """"""
        model_data = MODEL_TEMPLATE.format(
            sqlalchemy_imports=SQLALCHEMY_IMPORTS,
            db_constant_imports=DB_CONSTANT_IMPORTS.format(table_name=table_name.title().replace("_", "")),
            orm_base_imports=ORM_BASE_IMPORTS,
            table_name=table_name.title().replace("_", ""),
            # relation_var_names='\nCOUNTERS_RELATION_NAME = "counters"\n',
            relation_var_names='',
            # relation_var_lists='counters = []\n',
            relation_var_lists='',
            columns="\n    ".join(cls.get_table_columns(table_name)),
        )
        filename = cls.get_file(table_name, cls.MODEL_FILENAME)
        if not filename:
            return

        with open(filename, "w") as fp:
            fp.writelines(model_data)

    @classmethod
    def build_relation(cls, table_name):
        """"""
        relation_data = RELATION_TEMPLATE.format(
            controller_imports="",
            cls_name="",
            relation_name="",
            relation_cls_name="",

        )
        filename = cls.get_file(table_name, cls.CONTROLLER_FILENAME)
        if not filename:
            return

        with open(filename, "w") as fp:
            fp.writelines(relation_data)


    @classmethod
    def build_controller(cls, table_name):
        """"""
        controller_data = CONTROLLER_TEMPLATE.format(
            table_name=table_name,
            cls_name=table_name.title().replace("_", ""),
        )
        filename = cls.get_file(table_name, cls.CONTROLLER_FILENAME)
        if not filename:
            return

        with open(filename, "w") as fp:
            fp.writelines(controller_data)

    @classmethod
    def build_db_constant(cls, table_name):
        """"""
        constant_cls_name = table_name.title().replace("_", "")
        constant_data = DB_CONSTANT_TEMPLATE.format(
            cls_name=constant_cls_name,
            constant_name=table_name
        )

        with open(cls.DB_CONSTANT_MODULE, "r") as fp:
            readlines = fp.readlines()

        if constant_data in readlines:
            logger.error(f"{constant_cls_name}Constant constant already exists.")
            return

        readlines.append(constant_data)

        with open(cls.DB_CONSTANT_MODULE, "w") as fp:
            fp.writelines(readlines)

    @classmethod
    def get_table_columns(cls, table_name):
        """"""
        engine = create_engine(cls.DB_URL)
        inspector = inspect(engine)
        schemas = inspector.get_schema_names()
        columns = list()

        schema = None
        if "sqlite" in cls.DB_URL:
            schema = "main"
        else:
            for schema_ in schemas:
                if schema_ == cls.DB_NAME:
                    schema = schema_

        if not schema:
            return logger.error("No schema found. Aborting")

        for column in inspector.get_columns(table_name, schema=schema):
            col_var = COLUMN_TEMPLATE.format(
                var_name=column.get("name"),
                col_type=column.get("type"),
                args=cls.get_column_args(column)
            )
            columns.append(col_var)
        return columns

    @classmethod
    def get_column_args(cls, column):
        """"""
        args = [f'cls_attribute="{column.get("name")}"']
        column_args_mapping = {
            "id": [
                "        primary_key=True",
                "        autoincrement=True",
                "        unique=True"
            ],
        }
        return ",\n".join(args + column_args_mapping.get(column.get("name"), []))

    @classmethod
    def build_controller_import(cls, table_name):
        """"""
        controller_cls_name = table_name.title().replace('_', '')
        controller_import_str = f"from core.db.mysql.{table_name}.controller import {controller_cls_name}\n"

        with open(cls.CONTROLLER_IMPORTS_INIT_MODULE, "r") as fp:
            readlines = fp.readlines()

        if controller_import_str in readlines:
            logger.error(
                f"{controller_cls_name} controller import already exists."
            )
            return

        index = readlines.index(CONTROLLER_IMPORT_LINE_MARKER)
        readlines.insert(
            index + 1,
            controller_import_str
        )

        with open(cls.CONTROLLER_IMPORTS_INIT_MODULE, "w") as fp:
            fp.writelines(readlines)

    @classmethod
    def generate(cls, db_url, table_name, db_name=None):
        """"""
        cls.DB_URL = db_url
        cls.DB_NAME = db_name or DB_NAME
        cls.build_model(table_name)
        cls.build_controller(table_name)
        # cls.build_relation(table_name)
        cls.build_db_constant(table_name)
        cls.build_controller_import(table_name)


if __name__ == '__main__':
    TableGenerator.generate(DB_URL, "contact")
