import database
import datahandler

# Symbol for company. Change string to handle another company
symbol = "IBM"

db = f'../data/{symbol}.db'
csv = f'../data/{symbol}.csv'


datahandler.get_balance_sheet(symbol)
datahandler.write_to_csv(symbol)
database.load_database(db, csv)
database.show_all(db)

# database.show_table(db)

# database.drop_table(db)