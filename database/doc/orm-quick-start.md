# ORM Quick Start

## Using ORM declarative forms to define table metadata

Delcaring Table metadata is usually combined with mappled classes.

## 声明模型

声明式映射同时定义了Python对象和数据库元数据，元数据描述了SQL表。

```py
from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import select

class Base(DeclarativeBase):
    pass


class User(Base):
    """
    CREATE TABLE user_account (
        id INTEGER NOT NULL AUTO_INCREMENT,
        name VARCHAR(30) NOT NULL,
        fullname VARCHAR(60),
        PRIMARY KEY (id)
    )
    """
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(60))
    nickname: Mapped[Optional[str]] = mapped_column(String(64))
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    

class Address(Base):
    """
    CREATE TABLE address (
        id INTEGER NOT NULL AUTO_INCREMENT,
        email_address VARCHAR(30) NOT NULL,
        user_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES user_account (id)
    )
    """
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    email_address: Mapped[str] = mapped_column(String(30))
    
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
```

映射从一个基类开始，这个基类继承`DeclarativeBase`.

`Base`引用一个自动创建的`MetaData`集合，这个`MetaData`集合通过`DeclarativeBase.metadata`
类属性访问.

通过继承`Base`类来创建其他映射子类。一个映射类通常对应某个特定的数据库表，类属性`__tablename__`设置表明。
类创建后，生成的表可以通过`Declarative.__table__`访问。

接下来，生命表中的列。添加属性，属性包含特殊的类型注释，称为`Mapped`. 每一个属性名对应表中的一个列. 列的数据类型首先从`Mapped`注释中获得：

* `int` -> INTEGER
* `str` -> VARCHAR
* `Optional` -> NULL

更具体的类型信息可以在右侧用`mapped_column()`表明。

Python数据类型和SQL类型之间的关系可以用“类型注释map”定制。

所有ORM映射类要求至少有一个列被声明为主键, 使用`primary_key`参数.

`Mapped`还有其他变体, 最常见的是`relationship()`. `relationship`表示两个RM类之间的关联.

The classes are automativally given an `__init__()` method if we don't declare one of our own.

## Emit CREATE TABLE DDL

```py
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
```

## Create Objects and Persist

要插入数据，首先创建类的实例. 然后使用`Session`对象传递给数据库.

`Session.add_all()`插入多个对象。

`Session.commit()`把数据写入数据库，提交事务。

```py
with Session(engine) as session:
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[
            Address(email_address="spongebob@sqlalchemy.rog"),
        ]
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(
        name="patrick",
        fullname="Patrick Star"
    )

    session.add_all([spongebob, sandy, patrick])
    session.commit()
```

生成的SQL如下：

```sql
INSERT INTO user_account (name, fullname) 
VALUES (%(name)s, %(fullname)s)
{'name': 'spongebob', 'fullname': 'Spongebob Squarepants'}

INSERT INTO user_account (name, fullname) 
VALUES (%(name)s, %(fullname)s)
{'name': 'sandy', 'fullname': 'Sandy Cheeks'}

INSERT INTO user_account (name, fullname)
VALUES (%(name)s, %(fullname)s)
{'name': 'patrick', 'fullname': 'Patrick Star'}
```

See more:

* Executing with an ORM Session
* Basics of Using a Session
* Inserting Rows using the ORM Unit of Work pattern

## SELECT

使用`select()`函数创建一个新`Select`对象来生成`SELECT`表达式，然后传递给`Session`.

`Session.scalars()`返回一个`ScalarResult`对象，用它可以遍历选择的ORM对象列表.

```py
with Session(engine) as session:
    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

    for user in session.scalars(stmt):
        print(user)
```

生成SQL：

```sql
SELECT user_account.id, user_account.name, user_account.fullname
FROM user_account
WHERE user_account.name IN (%(name_1_1)s, %(name_1_2)s)
{'name_1_1': 'spongebob', 'name_1_2': 'sandy'}
```

See more:

* Selecting ORM Entities and Columns

## SELECT with JOIN

The `Select` construct creates joins using the `Select.join()` method.

See more:

* The WHERE clause
* Explicit FROM clauses and JOINs

```py
def select_with_joins():
    print_separator("selct with joins")
    stmt = (
        select(Address)
        .join(Address.user)
        # Multiple WHERE criteria are automatically chained together using AND.
        # Use column-like objects to create "equality" comparion.
        .where(User.name == "sandy")
        .where(Address.email_address == "sandy@sqlalchemy.org")
    )
    """
    SELECT address.id, address.email_address, address.user_id
    FROM address INNER JOIN user_account
    ON user_account.id = address.user_id
    WHERE user_account.name = %(name_1)s AND address.email_address = %(email_address_1)s
    {'name_1': 'sandy', 'email_address_1': 'sandy@sqlalchemy.org'}
    """
    with Session(engine) as session:
        sandy_address = session.scalars(stmt).one()
        # Address(id=2, email_address='sandy@sqlalchemy.org')
        print(sandy_address)


def load_address_of(name: str, email: str) -> Address:
    stmt = (
        select(Address)
        .join(Address.user)
        .where(User.name == name)
        .where(Address.email_address == email)
    )
    with Session(engine) as session:
        sandy_address = session.scalars(
            select(Address)
            .join(Address.user)
            .where(User.name == name)
            .where(Address.email_address == email)
        ).one()
        session.commit()
        return sandy_address

```

## Make Changes

THe Session object, together with ORM-mapped classes, automatically track
changes to the objects as they are made, which results in SQL statements
that will be emitted the next time the Session flushes.

See more:

* Loader Strategies
* Data Manipulation with the ORM

```py
def make_changes():
    print_separator("make changes")

    # sandy_address = load_address_of("sandy", "sandy@sqlalchemy.org")
    """
    SELECT user_account.id, user_account.name, user_account.fullname
    FROM user_account
    WHERE user_account.name = ?
    """
    with Session(engine) as session:
        stmt = select(User).where(User.name == "patrick")

        # Retrieve patrick
        patrick = session.scalars(stmt).one()
        print(patrick)
        # Add a new email address to patrick.
        # When we access patrick.addresses, a SELECT was emitted:
        # 
        # SELECT address.id, address.email_address, address.user_id
        # FROM address
        # WHERE ? = address.user_id
        patrick.addresses.append(
            Address(email_address="patrickstar@sqlalchemy.org")
        )
        
        sandy_address = session.scalars(
            select(Address)
            .join(Address.user)
            .where(User.name == "sandy")
            .where(Address.email_address == "sandy@sqlalchemy.org")
        ).one()
        # This won't work if sandy_address is retrieved in another session.
        sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"
        """
        UPDATE address
        SET email_address=?
        WHERE address.id = ?

        INSERT INTO address (email_address, user_id)
        VALUES (?, ?)
        """
        session.commit()


def load_user_by_name(name: str) -> User:
    stmt = select(User).where(User.name == name)
    with Session(engine) as session:
        user = session.scalars(stmt).one()
        session.commit()
        return user
```

## Some Deletes

Two different forms of deletion.

```py
def some_deletes():
    print_separator("some deletes")

    patrick = load_user_by_name("patrick")

    with Session(engine) as session:
        sandy_address = session.scalars(
            select(Address)
            .join(Address.user)
            .where(User.name == "sandy")
            .where(Address.email_address == "sandy_cheeks@sqlalchemy.org")
        ).one()

        """
        SELECT user_account.id, user_account, user_account.fullname
        FROM user_account
        WHERE user_account.id = ?
        """
        sandy = session.get(User, 2)

        """
        SELECT address.id, address.email_address, address.user_id
        FROM address
        WHERE ? = address.user_id

        This is the lazy loading operation proceeding so that the `sandy.addresses` collection
        could be loaded, so that we could remove the `sandy_address` member.

        sandy_address must be in this session.
        """
        sandy.addresses.remove(sandy_address)

        """
        We can choose to emit the DELETE SQL for what's set to be changed so far,
        without commiting the transaction, using the Session.flush():
        """
        session.flush()

        """
        For a top-level delete of an object by itself, use the `Session.delete()` method;
        this method dosn't actually perform the deletion, but sets up the object to be
        deleted on the next flush. The operation will also cascade to related objects
        based on the cascade options.

        The Session.delete() method in this particular case emitted two SELECT statements.
        When delete went to inspect the object, it turns out the patrick object was expired
        in memory, so new SQL was emitted to re-load the rows form the new transaction.
        """
        session.delete(patrick)
        """
        DELETE FROM address WHERE address.id = ?
        """
        session.commit()
```
