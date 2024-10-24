import sqlite3

from sqlalchemy import create_engine

from core.config.base import DatabaseAPIKeysConfig
from core.db.db_orm.base import DB_URL
from core.db.model_generator.base import TableGenerator

if __name__ == '__main__':
    """
    CASE 1: Show every table in this DB.
    CASE 2: Create model from table name.
    CASE 3: List every database tables and their columns
    """

    CASE = 2

    if CASE == 1:
        conn = sqlite3.connect(DB_URL.replace("sqlite:///", ""))
        cursor = conn.cursor()
        x = cursor.execute("SELECT * FROM sqlite_master where type='table'")

        for y in x.fetchall():
            print(y[1])

    elif CASE == 2:
        table_name = "events"
        TableGenerator.generate(DB_URL, table_name)
    elif CASE == 3:
        DB_URL = DatabaseAPIKeysConfig.get_config_by_name(DatabaseAPIKeysConfig.URL)
        from sqlalchemy import inspect

        engine = create_engine(DB_URL)

        inspector = inspect(engine)
        schemas = inspector.get_schema_names()

        for schema in schemas:
            print("schema: %s" % schema)
            for table_name in inspector.get_table_names(schema=schema):
                print("table: %s" % table_name)
                for column in inspector.get_columns(table_name, schema=schema):
                    print("Column: %s" % column)
