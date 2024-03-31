from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import configparser

from sqlalchemy.sql.ddl import DropTable

# Read the configuration file
config = configparser.ConfigParser()
config.read("config.ini")

# # Get the PostgreSQL connection details
# host = config.get("postgresql", "host")
# port = config.get("postgresql", "port")
# dbname = config.get("postgresql", "dbname")
# user = config.get("postgresql", "user")
# password = config.get("postgresql", "password")

# Define the database connection
engine = create_engine(f'postgresql+psycopg2://your_username:your_password@localhost:5432/your_database')

# Define the ORM model
Base = declarative_base()

class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Create the table
print(DropTable(Test).compile(engine))
# Create a session
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create
new_entry1 = Test(name="John Doe")
new_entry2 = Test(name="Bob")
session.add(new_entry1)
session.add(new_entry2)
session.commit()

# Read
rows = session.query(Test).all()
print("Read:")
for row in rows:
    print(row.id, row.name)

# Update
update_entry = session.query(Test).filter_by(name="John Doe").first()
if update_entry:
    update_entry.name = "Jane Smith"
    session.commit()
    print("Update: Entry updated successfully.")

# Read after update
rows = session.query(Test).all()
print("Read after update:")
for row in rows:
    print(row.id, row.name)

# Delete
delete_entry = session.query(Test).filter_by(name="Jane Smith").first()
if delete_entry:
    session.delete(delete_entry)
    session.commit()
    print("Delete: Entry deleted successfully.")

# Read after delete
rows = session.query(Test).all()
print("Read after delete:")
for row in rows:
    print(row.id, row.name)

# Close the session
session.close()