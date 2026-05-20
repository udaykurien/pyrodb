import os
import warnings
from copy import deepcopy

from pyrodb.schema import Foreign_Key
from pyrodb.table import Table

class Database:
    DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

    def __init__(self, db_name:str):
        self.db_name = db_name
        self.tables = {}
        self.dir = os.path.join(Database.DATA_DIR, self.db_name)
        self.table_snapshots = {}
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)

    def does_foreign_key_table_exist(self, table):
        for field_name, field_object in table.row_type.__dict__.items():
            if isinstance(field_object, Foreign_Key):
                if field_object.referenced_table not in self.tables.values():
                    raise NameError(f"Table {field_object.referenced_table.row_type.__name__} not found in {self.db_name}")

    def add_table(self, table:Table):
        self.does_foreign_key_table_exist(table)
        # Make registry of tables associated with db
        self.tables[table.row_type.__name__] = table
        # Give client direct (dot) access to table from db
        self.__dict__.update({table.row_type.__name__ : table})
        table.assign_parent_db(self)

    def begin(self):
        for key, value in self.__dict__.items():
            if isinstance(value, Table):
                self.table_snapshots[key] ={
                    "rows": deepcopy(value.rows),
                    "lookup_fields": deepcopy(value.lookup_fields),
                    "index": value._index
                }

    def _does_snapshot_exist(self):
        if len(self.table_snapshots) == 0:
            warnings.warn("No snapshots found.")
            return False
        return True

    def rollback(self):
        if (self._does_snapshot_exist()):
            for key, value in self.__dict__.items():
                if isinstance(value, Table):
                    value.rows = deepcopy(self.table_snapshots[key]["rows"])
                    value.lookup_fields = deepcopy(self.table_snapshots[key]["lookup_fields"])
                    value._index = self.table_snapshots[key]["index"]
            self.table_snapshots = {}

    def commit(self):
        if (self._does_snapshot_exist()):
            self.table_snapshots = {}
