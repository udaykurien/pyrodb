# Introduction

## pyrodb

A lightweight in-memory database built in Python, designed around class-based table and row definitions.

---

## Concepts

- **Field** — defines a column name and its expected type
- **Row** — a base class your data models inherit from; enforces field types on instantiation
- **Table** — holds rows of a given type; supports add, find, update, delete, show, save, and load
- **Database** — groups tables together and manages persistence paths

---

## Defining a Schema

```python
from rows import Field, Row, Table, Database

class User(Row):
    name  = Field("name",  str)
    age   = Field("age",   int)
    email = Field("email", str)
```

---

# Usage

## Creating a Database and Table

```python
user_table = Table(User)

clients = Database("clients")
clients.add_table(user_table)
```

Once added, the table is accessible as an attribute:

```python
clients.User  # same as user_table
```

---

## Adding Rows

```python
u1 = User(name="Alice", age=30, email="alice@email.com")
u2 = User(name="Bob",   age=22, email="bob@gmail.com")

clients.User.add_row(u1)
clients.User.add_row(u2)
```

Type mismatches raise errors at instantiation:

```python
User(name="Alice", age="thirty", email="alice@email.com")
# TypeError: Key: age expected <class 'int'>, got <class 'str'>
```

---

## Displaying Rows

```python
# Show all rows
clients.User.show()

# Show rows matching conditions
clients.User.show(name="Alice")
clients.User.show(age=30)
```

---

## Finding Rows

`find` returns a dict of `{index: row}` for use in code:

```python
results = clients.User.find(name="Bob")
results = clients.User.find(name="Alice", age=30)
```

---

## Updating Rows

```python
clients.User.update(
    where={"name": "Alice"},
    set_fields={"name": "Jane", "email": "jane@email.com"}
)
```

---

## Deleting Rows

```python
clients.User.delete(name="Bob")
clients.User.delete(name="Alice", age=30)
```

---

## Indexes

Set lookup fields to speed up `find`, `update`, and `delete` on large tables:

```python
clients.User.set_lookup_fields("name", "email")
```

Indexes are maintained automatically on add, update, and delete. Fields without an index fall back to a linear scan.

---

## Persistence

```python
# Save table to ./Data/clients/User.json
clients.User.save()

# Load from disk (set lookup fields first if using indexes)
clients.User.set_lookup_fields("name", "email")
clients.User.load()
```

---

## Multiple Tables

```python
class Furniture(Row):
    type   = Field("type",   str)
    length = Field("length", int)

furniture_table = Table(Furniture)
clients.add_table(furniture_table)

clients.Furniture.add_row(Furniture(type="Table", length=22))
clients.Furniture.show()
```

---

# System Call Graphs

## Table

### add_row
```mermaid
graph TD
    A["add_row(row)"] --> B{"isinstance(row, row_type)?"}
    B -- No --> C["raise TypeError"]
    B -- Yes --> D["_check_does_foreign_key_exists(row)"]
    D --> E["rows[self._index] = row"]
    E --> F["index_rows(self._index)"]
    F --> G["self._index += 1"]
```

---

### find
```mermaid
graph TD
    A["find(**kwargs)"] --> B["Row.validate_kwargs"]
    B --> C["result_indices = all row keys"]
    C --> D["split kwargs into indexed and unindexed fields"]
    D --> E{"indexed fields?"}
    E -- Yes --> F["intersect result_indices with lookup per field"]
    E -- No --> G{"unindexed fields?"}
    F --> G
    G -- Yes --> H["loop: remove non-matching indices"]
    G -- No --> I["build result_rows from result_indices"]
    H --> I
    I --> J["return result_rows"]
  
```

---

### delete
```mermaid
graph TD
  A["delete(**kwargs)"] --> B["find(**kwargs)"]
  B --> C{"results empty?"}
  C -- Yes --> D["return"]
  C -- No --> E["loop over results"]
  E --> F["remove_old_index_entries(index)"]
  F --> G["rows.pop(index)"]
  G --> E
```

---

### update
```mermaid
graph TD
    A["update(where, set_fields)"] --> B["Row.validate_kwargs"]
    B --> C["find(**where)"]
    C --> D{"results empty?"}
    D -- Yes --> E["print no matches found"]
    D -- No --> F["loop over results"]
    E --> F
    F --> G["remove_old_index_entries(index)"]
    G --> H["loop over set_fields"]
    H --> I["setattr row field to new value"]
    I --> H
    H --> J["index_rows(index)"]
    J --> F
```

---

### show
```mermaid
graph TD
    A["show(**kwargs)"] --> B{"kwargs empty?"}
    B -- Yes --> C["print_each_line(self.rows)"]
    B -- No --> D["find(**kwargs)"]
    D --> E["print_each_line(results)"]
    C --> F{"rows empty?"}
    E --> F
    F -- Yes --> G["print no matches found"]
    F -- No --> H["loop: print index and row"]
```

---

### save
```mermaid
graph TD
    A["save()"] --> B["_check_parent_db()"]
    B --> C["set file_path"]
    C --> D["initialise table dict structure"]
    D --> E["loop over rows"]
    E --> F["add row.__dict__ to table['rows']"]
    F --> E
    E --> G["loop over lookup_fields"]
    G --> H["append field to table['metadata']['lookup_fields']"]
    H --> G
    G --> I["loop over row_type schema fields"]
    I --> J{"isinstance(field_object, Foreign_Key)?"}
    J -- Yes --> K["add field to table['metadata']['foreign_keys']"]
    K --> I
    J -- No --> I
    I --> L["json.dump table to file"]
  
```

---

### load
```mermaid
graph TD
    A["load()"] --> B["_check_parent_db()"]
    B --> C["set file_path"]
    C --> D["clear self.rows"]
    D --> E["clear all lookup_field index dicts"]
    E --> F["open and parse json file"]
    F --> G["loop over metadata lookup_fields"]
    G --> H["initialise lookup_fields[field] to empty dict"]
    H --> G
    G --> I["loop over index, row in file rows"]
    I --> J["add row to self.rows"]
    J --> K["set _index to current index"]
    K --> L["index_rows(_index)"]
    L --> I
    I --> M["increment _index by 1"]
```

---

## Database

### add_table
```mermaid
graph TD
    A["add_table(table)"] --> B{"does_foreign_key_table_exist(table)?"}
    B -- foreign key table missing --> C["raise NameError"]
    B -- OK --> D["add table to self.tables dict"]
    D --> E["add table reference to self.__dict__"]
    E --> F["table.assign_parent_db(self)"]
```
