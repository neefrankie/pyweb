# 使用SELECT语句

`select()`函数生成`Select`构造，用于所有的`SELECT`查询，传递给：

* `Connection.execute()` in core
* `Session.execute()` in ORM

返回的`Result`包含取出的行。

## `select()`SQL表达式构造

```py
from sqlalchemy import select
stmt = select(user_table)where(user_table.c.name == "spongebob")
print(stmt)
```
