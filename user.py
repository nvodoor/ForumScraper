from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

Base = declarative_base();

class User(Base):
	__tablename__ = 'Users'

	id=Column(Integer, primary_key=True)
	username=Column(String, unique=True)
	password=Column(String, unique=True)

engine = create_engine('sqlite:///Forum.sqlite')
Base.metadata.create_all(engine)
session = Session(bind=engine)


conn = engine.connect();

TBD1 = User(username='***', password='****');
TBD2 = User(username='***', password='****');

# session.add_all([Neil,Joe]);
# session.commit();

tables = engine.execute("SELECT * FROM sqlite_master WHERE TYPE='table'")
for index, table in enumerate(tables):
    table_name = table[1]
    print(f"The #{index} table in the database is called '{table_name}'.")

search = conn.execute('SELECT * FROM Users').fetchall();

print(search);

