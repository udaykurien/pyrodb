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
                    raise TypeError(f"{key} expected {self.__class__.__dict__[key].field_type.__name__}, got {type(value).__name__}")
        self.__dict__.update(kwargs)
