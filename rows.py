class Field:
    '''
    Names and data types of each attribute in a table.
    '''
    def __init__(self, field_name:str, field_type:type) -> None:
        if not isinstance(field_name, str):
            raise TypeError(f"field_name expected str, got {type(field_name).__name__}")
        if not isinstance(field_type, type):
            raise TypeError(f"field_type expected type, got {type(field_type).__name__}")
        self.field_name = field_name
        self.field_type = field_type

class Row:
    def __init__(self, **kwargs) -> None:
        '''Validate and update fields and values'''
        for key, value in kwargs.items():
            if (key in self.__class__.__dict__ and
                isinstance(value, self.__class__.__dict__[key].field_type)):
                    continue
            else:
                if key not in self.__class__.__dict__:
                    raise ValueError(f"{key} not a valid field.")
                if not isinstance(value, self.__class__.__dict__[key].field_type):
                    raise TypeError(f"{key} expected {self.__class__.__dict__[key].field_type.__value__}, got {type(value).__name__}")
        self.__dict__.update(kwargs)
    def __repr__(self):
        row_string = f"Row Type: {self.__class__.__name__}, "
        for key, value in self.__dict__.items():
            row_string += f"{key}: {str(value)}, "
        row_string = row_string.rstrip(", ")
        return row_string

class Table:
    def __init__(self, row_type) -> None:
        # Make indices
        self._index = 0
        # Save row type
        self.row_type = row_type
        # Save rows into a dictionary
        self.rows = {}

    def add_row(self, row):
        if not isinstance(row, self.row_type):
            raise TypeError(f"Expected row type {self.row_type.__name__}, got {type(row).__name__}.")
        self.rows[self._index]= row
        self._index += 1

    def find(self, **kwargs):
        results = []
        for key, value in kwargs.items():
            if key not in self.row_type.__dict__:
                raise ValueError(f"Key {key} not in {self.row_type.__name__}")
            if not isinstance(value, getattr(self.row_type.__dict__[key],'field_type')):
                raise TypeError(f"Expected type of key: {key} is {getattr(self.row_type.__dict__[key],'field_type')}, got {type(value)} ")
        for key_item, val_item in self.rows.items():
            match = []
            for key_search, val_search in kwargs.items():
                match.append(True) if val_search == getattr(val_item, key_search) else match.append(False)
            if(all(match)):
                results.append(val_item)
        if len(results) == 0:
            return None
        return results
