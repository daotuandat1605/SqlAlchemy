# /from sqlalchemy import create_engine, text
# from sqlalchemy.orm import Session
# engine = create_engine(
#     "postgresql+psycopg://postgres:160507@localhost:5432/people",
#     echo=True
# )


# with engine.begin() as conn:
#     conn.execute(text("TRUNCATE TABLE people RESTART IDENTITY"))

# with engine.begin() as conn:
#     conn.execute(
#         text("INSERT INTO people(name,age) VALUES (:name,:age)"),
#         [
#             {"name":"An", "age":20},
#             {"name":"Binh","age":21},
#             {"name":"Bao", "age":22}
#         ]
#     )
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT id, name, age FROM people ORDER BY id"))

#     for row in result:
#         print(row.id,row.name,row.age)

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT id, name, age FROM people WHERE age >= :min_age"), {"min_age":21})

#     for row in result:
#         print(row[0],row[1],row[2])

# with engine.connect() as conn:
#     conn.execute(
#         text("INSERT INTO people(name,age) VALUES (:name, :age)"),
#         [
#             {"name":"Hoa", "age":25}
#         ]
#     )
#     conn.commit()
#     conn.execute(
#         text("INSERT INTO people(name,age) VALUES(:name, :age)"),
#         [
#             {"name":"Binh", "age":30}
#         ]   
#     )
#     conn.rollback()

#     result = conn.execute(text("SELECT * FROM people"))

#     print(result.all())

# with Session(engine) as session:
#     session.execute(
#         text("UPDATE people SET age = 40 WHERE id = 1"),
#     )
#     session.commit()
# with Session(engine) as session:
#     result = session.execute(
#         text("SELECT * FROM people WHERE id = 1")

#     )
#     print(result.all())

"""
from sqlalchemy import create_engine, text,  MetaData, Table, Column, BigInteger, Text, Integer, ForeignKey, inspect
engine = create_engine(
     "postgresql+psycopg://postgres:160507@localhost:5432/people",
     echo = False
)
metadata_obj = MetaData()

people_table = Table(
    "people",
    metadata_obj,
    Column("id",BigInteger, primary_key= True),
    Column("name", Text),
    Column("age",Integer)
)


addresses_table = Table(
    "addresses",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column(
        "person_id",
        ForeignKey("people.id"),
        nullable=False
    ),
    Column("email", Text, nullable=False)
)


metadata_obj.create_all(engine)

inspector = inspect(engine)

print("\nCac bang:")
print(inspector.get_table_names(schema = "public"))

print("\nCot cua people:")
for column in inspector.get_columns("people", schema = "public"):
     print(
        "Tên:", column["name"],
        "| Kiểu:", column["type"],
        "| Cho phép NULL:", column["nullable"],
        "| Default:", column["default"]
    )

print("\nKhoa chinh cua people:")
print(inspector.get_pk_constraint("people", schema = "public"))

if inspector.has_table("addresses", schema = "public"):
     print("\nKhoa ngoai cua addresses:")
     for foreign_key in inspector.get_foreign_keys("addresses", schema = "public"):
          print(
            "Cột:", foreign_key["constrained_columns"],
            "| Tham chiếu bảng:", foreign_key["referred_table"],
            "| Tham chiếu cột:", foreign_key["referred_columns"]
        )

with engine.connect() as conn:
     result = conn.execute(text("SELECT * FROM public.people ORDER BY id"))
     print("\nDu lieu people")
     print(result.all())
"""

from sqlalchemy import create_engine, text,  MetaData, Table, Column, BigInteger, Text, Integer, ForeignKey, inspect, select, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
engine = create_engine(
     "postgresql+psycopg://postgres:160507@localhost:5432/people",
     echo = False
)
metadata_obj = MetaData()

class Base(DeclarativeBase):
    pass
class Person(Base):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(BigInteger, primary_key = True)
    name: Mapped[str | None] = mapped_column(Text)
    age: Mapped[int | None] = mapped_column(Integer)

    predictions: Mapped[list["Prediction"]] = relationship(
        back_populates= "person"
    )
class Prediction(Base):
    __tablename__ = "predictions"
    id:Mapped[int] = mapped_column(BigInteger, primary_key= True)
    person_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("people.id"),
        nullable = False
    )
    label: Mapped[str] = mapped_column(Text, nullable = False)
    person: Mapped["Person"] = relationship(
        back_populates = "predictions"
    )
    confidence: Mapped[float | None] = mapped_column(
    Float,
    nullable=True
    )
Base.metadata.create_all(engine)

"""

with Session(engine) as session:
    user = Person(
        name = "Dao Tuan Dat",
        age = 19
    )
    session.add(user)
    session.flush()
    user_id = user.id
    session.commit()
    print("Da them, ID", user_id)
with Session(engine) as session:
    user = session.get(Person,user_id)

    if user is not None:
        print("Doc:",user.id, user.name, user.age)
with Session(engine) as session:
    user = session.get(Person,user_id)

    if user is not None:
        user.name = "Dat Tuan Dao"
        session.commit()

with Session(engine) as session:
    user = session.get(Person, user_id)

    if user is not None:
        print("Sau sửa:", user.name)
with Session(engine) as session:
    session.add_all([
        Person(name="An", age=18),
        Person(name="Binh", age=22),
        Person(name="Bao", age=20),
        Person(name="Hoa", age=25),
        Person(name="Lan", age=21),
        Person(name="Minh", age=17)
    ])
    session.commit()

from sqlalchemy import select

# Câu 1: Tất cả người, ID tăng dần
with Session(engine) as session:
    stmt = select(Person).order_by(Person.id)
    users = session.scalars(stmt).all()

    print("\nCau 1:")
    for user in users:
        print(user.id, user.name, user.age)

# Câu 2: Tuổi >= 20, sắp xếp tuổi tăng dần
with Session(engine) as session:
    stmt = (
        select(Person)
        .where(Person.age >= 20)
        .order_by(Person.age, Person.id)
    )
    users = session.scalars(stmt).all()

    print("\nCau 2:")
    for user in users:
        print(user.id, user.name, user.age)

# Câu 3: Tuổi từ 18 đến 22, bao gồm hai đầu
with Session(engine) as session:
    stmt = (
        select(Person)
        .where(Person.age >= 18, Person.age <= 22)
        .order_by(Person.age, Person.id)
    )
    users = session.scalars(stmt).all()

    print("\nCau 3:")
    for user in users:
        print(user.id, user.name, user.age)

# Câu 4: Tên chứa "an", không phân biệt hoa/thường
with Session(engine) as session:
    stmt = (
        select(Person)
        .where(Person.name.ilike("%an%"))
        .order_by(Person.id)
    )
    users = session.scalars(stmt).all()

    print("\nCau 4:")
    for user in users:
        print(user.id, user.name, user.age)

# Câu 5: Ba người lớn tuổi nhất, bỏ qua tuổi NULL
with Session(engine) as session:
    stmt = (
        select(Person)
        .where(Person.age.is_not(None))
        .order_by(Person.age.desc(), Person.id)
        .limit(3)
    )
    users = session.scalars(stmt).all()

    print("\nCau 5:")
    for user in users:
        print(user.id, user.name, user.age)

# Câu 6: Trang 2, mỗi trang 2 người
page = 2
page_size = 2

with Session(engine) as session:
    stmt = (
        select(Person)
        .order_by(Person.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    users = session.scalars(stmt).all()

    print("\nCau 6:")
    for user in users:
        print(user.id, user.name, user.age)

# Câu 7: Lấy hai cột, nhận các Row bằng execute()
with Session(engine) as session:
    stmt = select(Person.name, Person.age).order_by(Person.id)
    rows = session.execute(stmt).all()

    print("\nCau 7:")
    for row in rows:
        print(row.name, row.age)

# Câu 8: Lấy một cột, nhận list chuỗi bằng scalars()
with Session(engine) as session:
    stmt = select(Person.name).order_by(Person.id)
    names = session.scalars(stmt).all()

    print("\nCau 8:")
    print(names)
"""

with Session(engine) as session:
    person = Person(name = "Dao Tuan Dat", age = 25)
    prediction1 = Prediction(label="plastic")
    prediction2 = Prediction(label="paper")

    person.predictions.append(prediction1)
    person.predictions.append(prediction2)
    session.add(person)

    print("Truoc flush:")
    print("Person ID:", person.id)
    print("Prediction 1 person_id:", prediction1.person_id)

    session.flush()

    person_id = person.id

    print("\nSau flush:")
    print("Person ID:", person.id)
    print("Prediction 1:", prediction1.id, prediction1.person_id)
    print("Prediction 2:", prediction2.id, prediction2.person_id)

    session.commit()
    print("\nDa commit!")


# 4. Đọc người vừa tạo và các lần dự đoán của người đó
with Session(engine) as session:
    person = session.get(Person, person_id)

    if person is not None:
        print("\nNguoi vua them:")
        print(person.id, person.name, person.age)

        print("\nCac lan du doan:")
        for prediction in sorted(
            person.predictions,
            key=lambda prediction: prediction.id
        ):
            print(
                "Prediction ID:", prediction.id,
                "| Label:", prediction.label,
                "| Person ID:", prediction.person_id
            )

            print("Nguoi so huu:", prediction.person.name)


# 5. Đọc tất cả các lần dự đoán trong database
with Session(engine) as session:
    stmt = select(Prediction).order_by(Prediction.id)
    predictions = session.scalars(stmt).all()

    print("\nTat ca predictions:")
    for prediction in predictions:
        print(
            prediction.id,
            prediction.label,
            prediction.person_id
        )


with Session(engine) as session:
    stmt = select(Prediction).order_by(Prediction.id).limit(1)
    prediction = session.scalars(stmt).first()

    if prediction is None:
        print("Chua co prediction")
    else:
        prediction.confidence = 0.95
        prediction_id = prediction.id
        session.commit()

with Session(engine) as session:
    if prediction is not None:
        saved = session.get(Prediction, prediction_id)
        print(saved.id, saved.label, saved.confidence)
with Session(engine) as session:
    stmt = select(Prediction).order_by(Prediction.id).limit(1)
    prediction = session.scalars(stmt).first()

    if prediction is None:
        print("Chưa có prediction")
    else:
        prediction.model_name = "garbage-classifier-v1"
        session.commit()

        print("Đã lưu:", prediction.id, prediction.model_name)