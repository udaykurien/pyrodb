import unittest
from unittest.mock import patch
from pyrodb.pyrodb import Field, Row, Table, Database

class TestTable(unittest.TestCase):
    def setUp(self):
        class User(Row):
            name = Field("name", str)
            age = Field("age", int)
            email = Field("email", str)

        self.user_table = Table(User)

        self.clients_test = Database('clients')
        self.clients_test.add_table(self.user_table)
        self.clients_test.User.set_lookup_fields("name", "age")

        u1 = User(name="Alice", age=30, email="alice@email.com")
        u2 = User(name="Bob", age=22, email="bob@gmail.com")
        u3 = User(name="Alice", age=45, email="alice_two@gmail.com")
        u4 = User(name="Kira", age=30, email="kira@gmail.com")
        u5 = User(name="Bob", age=42, email="bobby@gmail.com")
        u6 = User(name = "John", age =55, email="john@hotmail.com")

        self.clients_test.User.add_row(u1)
        self.clients_test.User.add_row(u2)
        self.clients_test.User.add_row(u3)
        self.clients_test.User.add_row(u4)
        self.clients_test.User.add_row(u5)
        self.clients_test.User.add_row(u6)

    def test_add_correct_row(self):
        User = self.user_table.row_type
        u7 = User(name = "Jake", age =62, email="jake@hotmail.com")
        self.clients_test.User.add_row(u7)
        self.assertEqual(len(self.clients_test.User.rows), 7)

    def test_add_incorrect_field_name(self):
        User = self.user_table.row_type
        with self.assertRaises(ValueError):
            u7 = User(name_wrong = "Rhea", age =30, email="rhea@hotmail.com")

    def test_add_incorrect_field_type(self):
        User = self.user_table.row_type
        with self.assertRaises(TypeError):
            u7 = User(name = "Rhea", age ="30", email="rhea@hotmail.com")

    def test_find_correct_row_via_indexed_fields(self):
        User = self.user_table.row_type
        u_test = User(name="Alice", age=45, email="alice_two@gmail.com")
        results = self.clients_test.User.find(name=u_test.name, age=u_test.age)
        self.assertEqual(results[2].name, u_test.name)
        self.assertEqual(results[2].age, u_test.age)

    def test_find_correct_row_via_mixed_fields(self):
        User = self.user_table.row_type
        u_test = User(name="Alice", age=45, email="alice_two@gmail.com")
        results = self.clients_test.User.find(name=u_test.name, email=u_test.email)
        self.assertEqual(results[2].name, u_test.name)
        self.assertEqual(results[2].email, u_test.email)

    def test_find_wrong_key(self):
        User = self.user_table.row_type
        u_test = User(name="Alice", age=45, email="alice_two@gmail.com")
        with self.assertRaises(ValueError):
            results = self.clients_test.User.find(name_wrong=u_test.name, email=u_test.email)

    def test_find_wrong_type(self):
        User = self.user_table.row_type
        u_test = User(name="Alice", age=45, email="alice_two@gmail.com")
        with self.assertRaises(TypeError):
            results = self.clients_test.User.find(name=u_test.age, email=u_test.email)

    def test_del_happy_path(self):
         User = self.user_table.row_type
         u_test_1 = User(name="Alice", age=30, email="alice@email.com")
         self.clients_test.User.delete(name=u_test_1.name)
         self.assertEqual(len(self.user_table.rows), 4)

    def test_update_happy_path(self):
        User = self.user_table.row_type
        u_test_1 = User(name="Alice", age=30, email="alice@email.com")
        self.clients_test.User.update(where={"name":u_test_1.name, "email":u_test_1.email},\
            set_fields={"name":"Jane", "email":"jane@email.com", "age":52})
        result = self.clients_test.User.find(name="Jane")
        self.assertEqual(result[0].name, "Jane")
        self.assertEqual(result[0].email, "jane@email.com")
        self.assertEqual(result[0].age, 52)

    def test_print_happy_path(self):
        User = self.user_table.row_type
        name = "Alice"
        with patch('builtins.print') as mock_print:
            self.clients_test.User.show(name=name)
            mock_print.assert_called()
        self.assertEqual(len(mock_print.call_args_list), 2)
        for arg in mock_print.call_args_list:
            self.assertIn(name, arg[0][0])


if __name__ == "__main__":
    unittest.main()
