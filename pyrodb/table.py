import json
import os

from pyrodb.schema import Row, Foreign_Key
from pyrodb.op import Op

class Table:
    def __init__(self, row_type) -> None:
        self._index = 0
        self.row_type = row_type
        self.rows = {}
        self.lookup_fields = {}
        self.parent_db = None

    def assign_parent_db(self, parent_db):
        self.parent_db = parent_db

    def _check_parent_db(self):
        if not (self.parent_db):
            raise RuntimeError("parent_db name unset. All tables need to be part of a db.")

    def set_lookup_fields(self, *args):
        for field_name in args:
            if field_name not in self.row_type.__dict__.keys():
                raise NameError(f"field: {field_name} not in {self.row_type.__name__}.")
            if field_name not in self.lookup_fields.keys():
                self.lookup_fields[field_name] = {}

    def index_rows(self, row_index):
        row = self.rows[row_index]
        for lookup_field in self.lookup_fields.keys():
            if row.__dict__[lookup_field] not in self.lookup_fields[lookup_field].keys():
                self.lookup_fields[lookup_field][row.__dict__[lookup_field]] = set()
            self.lookup_fields[lookup_field][row.__dict__[lookup_field]].add(row_index)

    def remove_old_index_entries(self, index):
        for field, value in self.rows[index].__dict__.items():
            if field in self.lookup_fields:
                self.lookup_fields[field][value].remove(index)

    def _check_does_foreign_key_exists(self, row):
        for field_name, field_object in row.__class__.__dict__.items():
           if (isinstance(field_object, Foreign_Key)):
               if row.__dict__[field_name] not in field_object.referenced_table.rows.keys():
                   raise ValueError(f"Index {row.__dict__[field_name]} not found in table {field_object.referenced_table.row_type.__name__}.")

    def add_row(self, row):
        if not isinstance(row, self.row_type):
            raise TypeError(f"Expected row type {self.row_type.__name__}, got {type(row).__name__}.")
        self._check_does_foreign_key_exists(row)
        self.rows[self._index]= row
        self.index_rows(self._index)
        self._index += 1

    def find(self, **kwargs):
        result_rows = {}
        result_indices = set(self.rows.keys()) # set result_indices to identity set (all table indices) for any set intersection
        for key, value in kwargs.items():
            if not isinstance(value, Op):
                Row.validate_kwargs(self.row_type, {key:value})
            elif isinstance(value, Op):
                Row.validate_kwargs(self.row_type, {key:value.value})
        indexed_fields = set(kwargs.keys()) & set(self.lookup_fields.keys()) #set intersection
        unindexed_fields = set(kwargs.keys()) - set(self.lookup_fields.keys())
        if (len(indexed_fields) != 0):
            for indexed_field in indexed_fields:
                if not isinstance(kwargs[indexed_field], Op):
                    result_indices = result_indices & self.lookup_fields[indexed_field].get(kwargs[indexed_field], set()) # Intersection with identity returns smaller set, subsequent intersections with last iteration results will whittle down results
                elif isinstance(kwargs[indexed_field], Op):
                    for index in result_indices.copy():
                        if not kwargs[indexed_field].op_function(self.rows[index].__dict__[indexed_field], kwargs[indexed_field].value):
                            result_indices.remove(index)
        if (len(unindexed_fields) != 0):
            for unindexed_field in unindexed_fields:
                if len(result_indices)== 0:
                    break
                for index in result_indices.copy(): # .copy to preven iterator chaining with base object as loop progresses
                    if not isinstance(kwargs[unindexed_field], Op):
                        if self.rows[index].__dict__[unindexed_field] != kwargs[unindexed_field]:
                            result_indices.remove(index)
                    elif isinstance(kwargs[unindexed_field], Op):
                        if not kwargs[unindexed_field].op_function(self.rows[index].__dict__[unindexed_field], kwargs[unindexed_field].value):
                            result_indices.remove(index)

        for result_index in result_indices:
            result_rows[result_index] = self.rows[result_index]
        return result_rows

    def delete(self, **kwargs):
        results = self.find(**kwargs)
        if len(results) != 0:
            for index,val in results.items():
                self.remove_old_index_entries(index)
                self.rows.pop(index)

    def update(self, where:dict, set_fields:dict):
        Row.validate_kwargs(self.row_type, set_fields)
        results = self.find(**where)
        if(len(results) == 0):
            print("No matches found.")
        for index, row in results.items():
            self.remove_old_index_entries(index)
            for field, value in set_fields.items():
                setattr(row, field, value)
            self.index_rows(index)

    def show(self, **kwargs):
        def print_each_line(rows):
            if len(rows) == 0:
                print("No matches found.")
                return
            for index, row in rows.items():
                f=f"{index}. {row}"
                print(f)
        if len(kwargs) == 0:
            print_each_line(self.rows)
            return
        results = self.find(**kwargs)
        print_each_line(results)

    def save(self):
        self._check_parent_db()
        file_path = os.path.join(self.parent_db.dir, f"{self.row_type.__name__}.json")
        table = {
            "metadata":{
                "lookup_fields":[],
                "foreign_keys":{}
            },
            "rows": {}
        }
        for index, row in self.rows.items():
            table["rows"][index] = row.__dict__
        for lookup_field in self.lookup_fields.keys():
            table["metadata"]["lookup_fields"].append(lookup_field)
        for field_name, field_object in self.row_type.__dict__.items():
            if isinstance(field_object, Foreign_Key):
                table["metadata"]["foreign_keys"][field_name] = field_object.referenced_table.row_type.__name__
        with open(file_path, 'w') as file:
            json.dump(table, file)

    def load(self):
        self._check_parent_db()
        file_path = os.path.join(self.parent_db.dir, f"{self.row_type.__name__}.json")
        # Empty old in-memory rows before loading new rows from file to prevent collisions and chaos.
        self.rows = {}
        # Empyty old indexed values as they beccome obsolete on loading rows from a file and can cause conflicts.
        for lookup_field, lookup_value in self.lookup_fields.items():
            self.lookup_fields[lookup_field] = {}
        with open(file_path, 'r') as file:
            data = json.load(file)
        for field in data["metadata"]["lookup_fields"]:
            self.lookup_fields[field] = {}
        for index, row in data["rows"].items():
            self.rows[int(index)]=self.row_type(**row)
            self._index = int(index)
            self.index_rows(self._index)
        self._index += 1
