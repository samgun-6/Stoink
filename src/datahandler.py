import json
from pandas.io.json import json_normalize
import csv
import requests
import config
import pandas as pd

# Get the balance_sheet data with an API key
def get_balance_sheet(symbol):
    # Add the API key to the config.py file
    url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={config.API_KEY}'
    print(url)
    r = requests.get(url)
    data = r.json()

    with open(f'../data/{symbol}.json', 'w+') as f:
        json.dump(data, f)

# Use Pandas library json_normalize to write json data to a csv file
def write_to_csv(symbol):
    with open(f'../data\{symbol}.json') as data_file:    
        data = json.load(data_file) 

    df = json_normalize(data, 'quarterlyReports')
    df.to_csv(f"../data/{symbol}.csv", index=False, sep=',', encoding="utf-8") #write to csv file

    print (df)


# Write json data to a csv file
def write_to_csv_func(symbol):
    # Opening JSON file and loading the data
    # into the variable data
    with open(f'../data/{symbol}.json') as json_file:
        data = json.load(json_file)
    
    # Retreive dictionary from json data
    qreps = data['quarterlyReports']
    
    # Open file for writing
    data_file = open(f'../data/{symbol}.csv', 'w', newline='')
    
    # create csv writer object
    csv_writer = csv.writer(data_file)
    
    # Counter variable used for writing
    count = 0

    header = {...}
    for rep in qreps:
        if count == 0:
            header = rep.keys()

            print('Headers of the file columns created:')
            print(header)
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(rep.values())

    # Close file
    data_file.close()





