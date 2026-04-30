from rows import Field, Row

if (False):
    field1 = Field("22", int)
    print(field1.field_name)

if (False):
    print(Field)

if (True):
    class User(Row):
        name = Field("name", str)
        age = Field("age", int)
        email = Field("email", str)

    u1 = User(name="Alice", age=30, email="alice@email.com")
