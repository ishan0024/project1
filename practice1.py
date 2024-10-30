from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import json

# Create a connection to the MySQL database
engine = create_engine('mysql://root:@localhost/uniportal')

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the table you want to query
metadata = MetaData(bind=engine)
my_table = Table('Item', metadata, autoload_with=engine)

# Query the table
result = session.query(my_table).all()

# Convert the result into a list of dictionaries
def row_to_dict(row):
    return {column.name: getattr(row, column.name) for column in row._table_.columns}

# Convert each row to a dictionary
data = [row_to_dict(row) for row in result]

# Convert the list of dictionaries to JSON
json_data = json.dumps(data, indent=4)

# Output or use the JSON data
print(json_data)