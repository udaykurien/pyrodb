from rows import Field, Row, Table

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

    class Furniture(Row):
        type = Field("type", str)
        length = Field("length", int)

    u1 = User(name="Alice", age=30, email="alice@email.com")
    u2 = User(name="Bob", age=22, email="bob@gmail.com")
    u3 = User(name="Alice", age=45, email="alice_two@gmail.com")
    u4 = User(name="Kira", age=30, email="kira@gmail.com")
    u5 = User(name="Bob", age=42, email="bobby@gmail.com")

    f1 = Furniture(type="Table", length=22)

    user_table = Table(User)

    furniture_table = Table(Furniture)

    user_table.add_row(u1)
    user_table.add_row(u2)
    user_table.add_row(u3)
    user_table.add_row(u4)
    user_table.add_row(u5)

    # user_table.update(where={"name":"Alice" ,"age":45},set={"name":"Jane"})
    user_table.update(where={"name":"Alice"},set={"name":"Jane"})


    user_table.find(name="Bob")
    user_table.delete(name="Alice")

    user_table.show()


    if(0):
        user_table.find(name="Alice")
        user_table.find(name="Alice", age=30)
        # user_table.find(name=123)
        user_table.find(nickname="Alice")
