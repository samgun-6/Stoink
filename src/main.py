import database
import datahandler

name = 'topTenFeats211201'
db = '../client.db.sqlite3'
djangoDb = '../client.db.sqlite3'
csv = f'../client/data/{name}.csv'

# database.load_database(db, csv, name)
# database.show_table(db, name)
# database.show_all(db, name)

database.query_stocks(db=djangoDb, table='EARNINGS', symbol='AAPL') # Example call

# datahandler.load_dataset()

# database.show_table(db)

# database.drop_table(db)