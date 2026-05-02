class Field:
    def __init__(self, field_name:str, field_type:type) -> None:
        if not isinstance(field_name, str):
            raise TypeError(f"field_name expected str, got {type(field_name).__name__}")
        if not isinstance(field_type, type):
            raise TypeError(f"field_type expected type, got {type(field_type).__name__}")
        self.field_name = field_name
        self.field_type = field_type

class Row:
    @staticmethod
    def validate_kwargs(row_type, data:dict):
        for key, value in data.items():
            if (key in row_type.__dict__) and isinstance(value, row_type.__dict__[key].field_type):
                continue
            else:
                if key not in row_type.__dict__:
                    raise ValueError(f"Key: {key} not a valid field in {row_type.__name__}")
                if not isinstance(value, row_type.__dict__[key].field_type):
                    raise TypeError(f"Key: {key} expected {row_type.__dict__[key].field_type}, got {type(value)} ")

    def __init__(self, **kwargs) -> None:
        self.validate_kwargs(self.__class__, kwargs)
        self.__dict__.update(kwargs)

    def __repr__(self):
        row_string = f"Row Type: {self.__class__.__name__}, "
        for key, value in self.__dict__.items():
            row_string += f"{key}: {str(value)}, "
        row_string = row_string.rstrip(", ")
        return row_string

class Table:
    def __init__(self, row_type) -> None:
        self._index = 0
        self.row_type = row_type
        self.rows = {}

    def add_row(self, row):
        if not isinstance(row, self.row_type):
            raise TypeError(f"Expected row type {self.row_type.__name__}, got {type(row).__name__}.")
        self.rows[self._index]= row
        self._index += 1

    def find(self, **kwargs):
        results = {}
        Row.validate_kwargs(self.row_type, kwargs)
        for key_item, val_item in self.rows.items():
            match = []
            for key_search, val_search in kwargs.items():
                match.append(True) if val_search == getattr(val_item, key_search) else match.append(False)
            if(all(match)):
                results[key_item] = val_item
        return results

    def delete(self, **kwargs):
        results = self.find(**kwargs)
        if len(results) != 0:
            for key,val in results.items():
                self.rows.pop(key)

    def update(self, where:dict, set:dict):
        Row.validate_kwargs(self.row_type, where)
        Row.validate_kwargs(self.row_type, set)
        results = self.find(**where)
        for index, obj in results.items():
            for field, value in set.items():
                setattr(obj, field, value)

    def show(self, **kwargs):
        def print_each_line(rows):
            for index, row in rows.items():
                f=f"{index}. {row}"
                print(f)
        if len(kwargs) == 0:
            print_each_line(self.rows)
            return
        Row.validate_kwargs(self.row_type, kwargs)
        results = self.find(**kwargs)
        print_each_line(results)
