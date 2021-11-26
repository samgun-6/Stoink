import database
import datahandler

# Symbol for company. Change string to handle another company
symbol = "IBM"

db = f'../data/{symbol}.db'
csv = f'../data/{symbol}.csv'


datahandler.load_dataset()

# database.show_table(db)

# database.drop_table(db)