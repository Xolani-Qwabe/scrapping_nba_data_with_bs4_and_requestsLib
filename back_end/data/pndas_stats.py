import pandas as pd
from sqlalchemy import create_engine


database_url = 'sqlite:///C:/Users/thabi/Documents/BBallAI/back_end/data/nba_databases/nba.db'
# Establish a connection to your SQL database
engine = create_engine(database_url)  # Change this connection string according to your database type and credentials

# Query to select data from your SQL table
sql_query = "SELECT * FROM basic_game"

# Use Pandas to read data from SQL table into a DataFrame
df = pd.read_sql(sql_query, engine)

# Now you have your SQL table data in a Pandas DataFrame (df)
print(df)
