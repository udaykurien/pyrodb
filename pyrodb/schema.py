class Field:
    def __init__(self, field_name:str, field_type:type) -> None:
        if not isinstance(field_name, str):
            raise TypeError(f"field_name expected str, got {type(field_name).__name__}")
        if not isinstance(field_type, type):
            raise TypeError(f"field_type expected type, got {type(field_type).__name__}")
        self.field_name = field_name
        self.field_type = field_type

class Foreign_Key(Field):
    def __init__(self, referenced_table=None):
        super().__init__(f"{referenced_table.row_type.__name__}_key",int )
        self.referenced_table = referenced_table

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
