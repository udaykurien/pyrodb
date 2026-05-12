from pyrodb.pyrodb import Field, Foreign_Key, Row, Table, Database

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

    store = Database('clients')
    store.add_table(user_table)

    # clients.tables["User"].show()
    store.User.show()

    print("-"*10)
    u1 = User(name="Alice", age=30, email="alice@email.com")
    u2 = User(name="Bob", age=22, email="bob@gmail.com")
    u3 = User(name="Alice", age=45, email="alice_two@gmail.com")
    u4 = User(name="Kira", age=30, email="kira@gmail.com")
    u5 = User(name="Bob", age=42, email="bobby@gmail.com")
    u6 = User(name = "John", age =55, email="john@hotmail.com")

    store.User.add_row(u1)
    store.User.add_row(u2)
    store.User.add_row(u3)
    store.User.add_row(u4)
    store.User.add_row(u5)
    store.User.add_row(u6)

    # user_table.save()
    # clients.User.save()
    # clients.User.show()
    # clients.User.delete(name='John', age=55)
    # clients.User.save()
    #
    store.User.lookup_index("name", "email")
    store.User.show()


    # clients.tables["User"].show()
    #
if (False):
    class User(Row):
        name = Field("name", str)
        age = Field("age", int)
        email = Field("email", str)

    user_table = Table(User)
    store = Database('clients')
    store.add_table(user_table)
    store.User.set_lookup_fields("name", "email")
    # clients.User.set_lookup_fields()
    store.User.load()
    # clients.User.show()

    u1 = User(name="Archie", age=27, email="archie@riverdale.com")
    store.User.add_row(u1)
    # clients.User.show()
    # clients.User.show()
    print("---")
    # print(clients.User.lookup_fields)
    print("---")
    # clients.User.update(where={"name":"Alice", "email":"alice@email.com"},set_fields={"name":"Jane", "email":"jane@email.com"})

    # clients.User.delete(name="John", email='john@hotmail.com')

    # clients.User.show()

    store.User.show(age=30)#, email="alice@email.com")
    print("---")
    store.User.show()

    print("---")
    # clients.User.show()

    # print()

    # clients.User.show(name="Alice9")

if (True):
    class User(Row):
        name = Field("name", str)
        age = Field("age", int)
        email = Field("email", str)

    user = Table(User)

    class Cat(Row):
        name = Field("product", str)
        age = Field("age", int)

    cat = Table(Cat)

    class Order(Row):
        product = Field("product", str)
        cost = Field("cost", float)
        fk = Foreign_Key(user)

    store = Database('store')

    store.add_table(user)
    store.User.set_lookup_fields("name", "email")
    store.User.load()

    order = Table(Order)
    store.add_table(order)

    o1 = Order(product="Table", cost=25.5, fk=1)
    store.Order.add_row(o1)

    o2 = Order(product="Paint", cost=7.2, fk=99)
    store.Order.add_row(o2)

    store.User.show()
    store.Order.show()
