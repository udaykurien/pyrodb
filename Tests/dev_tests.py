from rows import Field, Row, Table, Database

if (False):
    field1 = Field("22", int)
    print(field1.field_name)

if (False):
    print(Field)

if (False):
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
    print(f1.__dict__)
    print(f1)

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
    user_table.save()


    if(0):
        user_table.find(name="Alice")
        user_table.find(name="Alice", age=30)
        # user_table.find(name=123)
        user_table.find(nickname="Alice")

if (False):
    class User(Row):
        name = Field("name", str)
        age = Field("age", int)
        email = Field("email", str)

    user_table = Table(User)
    # user_table.load()
    # user_table.show()

    clients = Database('clients')
    clients.add_table(user_table)

    # clients.tables["User"].show()
    clients.User.show()

    print("-"*10)
    u1 = User(name="Alice", age=30, email="alice@email.com")
    u2 = User(name="Bob", age=22, email="bob@gmail.com")
    u3 = User(name="Alice", age=45, email="alice_two@gmail.com")
    u4 = User(name="Kira", age=30, email="kira@gmail.com")
    u5 = User(name="Bob", age=42, email="bobby@gmail.com")
    u6 = User(name = "John", age =55, email="john@hotmail.com")

    clients.User.add_row(u1)
    clients.User.add_row(u2)
    clients.User.add_row(u3)
    clients.User.add_row(u4)
    clients.User.add_row(u5)
    clients.User.add_row(u6)

    # user_table.save()
    # clients.User.save()
    # clients.User.show()
    # clients.User.delete(name='John', age=55)
    # clients.User.save()
    #
    clients.User.lookup_index("name", "email")
    clients.User.show()


    # clients.tables["User"].show()
    #
if (True):
    class User(Row):
        name = Field("name", str)
        age = Field("age", int)
        email = Field("email", str)

    user_table = Table(User)
    clients = Database('clients')
    clients.add_table(user_table)
    clients.User.set_lookup_fields("name", "email")
    # clients.User.set_lookup_fields()
    clients.User.load()
    # clients.User.show()

    u1 = User(name="Archie", age=27, email="archie@riverdale.com")
    clients.User.add_row(u1)
    # clients.User.show()
    print("calling update now..")
    clients.User.update(where={"name":"Alice", "email":"alice@email.com"},set_fields={"name":"Jane", "email":"jane@email.com"})

    clients.User.show()

    # print()

    # clients.User.show(name="Alice9")
