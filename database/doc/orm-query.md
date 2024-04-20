# ORM quering

## Writing SELECT statements for ORM Mapped Classes

```py
from sqlalchemy import select

stmt = select(User).where(user.name == "spongebob")

result = session.execute(stmt)

for user_obj in result.scalars():
    print(f"{user_obj.name} {user_obj.fullname}")
```

SQL:

```sql
SELECT user_account.id,
    user_account.name,
    user_account.fullname
FROM user_account
WHERE user_account.name = ?
```

### Selecting ORM Entities and Attributes

`Result`返回`Row`列表：

```py
result.all()
```

每个Row元素是一个元组，这个元组中的元素包含数据库中一行的数据。如果只想要取出的数据，不要`Row`中包含的其他信息，使用`Session.scalars()`方法执行，返回`ScalarResult`对象，这是一个列表，每个元素只有数据库中一行的数据。

```py
session.scalars(select(User).order_by(User.id)).all()
session.scalars(select(User)).first()
```

相当于`result.scalars()`.

还可以选择表中的单独一列数据：

```py
rows = session.execute(select(User.name, User.fullname)).first()
```
