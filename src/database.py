import pandas as pd
import sqlite3
from sqlite3 import Error


def db_connection(db):
    # Connect to database
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)

    return conn

def create_table(db):

    # Connect to database
    conn = db_connection(db)
    # Create a cursor
    cursor = conn.cursor()

    # Create a table
    cursor.execute("""CREATE TABLE stocksdata (
        time text,
        open real,
        high real,
        low real,
        close real,
        volume integer
    );""")

    # Commit changes & close connection
    conn.commit()
    conn.close()

def show_table(db):

    conn = db_connection(db)
    cursor = conn.cursor()

    # Display columns
    print('\nColumns in Stocksdata table:')
    data=cursor.execute('''SELECT * FROM stocksdata''')
    for column in data.description:
        print(column[0])

    # Commit changes & close connection
    conn.commit()
    conn.close()

def drop_table(db):

    # # Connect to database
    conn = db_connection(db)
    # Create a cursor
    cursor = conn.cursor()

    # Drop table
    cursor.execute("DROP TABLE IF EXISTS stocksdata")

    print('Table Dropped!')

    # Commit changes & close connection
    conn.commit()
    conn.close()

def load_database(db, csv):
    df = pd.read_csv(csv)

    print(df.dtypes)
    conn = db_connection(db)
    df.to_sql(name='stocksdata', con=conn, if_exists='append')

def show_all(db):
    # Connect to database
    conn = db_connection(db)
    # Create a cursor
    cursor = conn.cursor()

    # Query the database
    cursor.execute("SELECT * from stocksdata")
    items = cursor.fetchall()

    for item in items:
        print(item)
    
    # Commit changes & close connection
    conn.commit()
    conn.close()
