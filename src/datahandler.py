import json
import csv
import requests
import config
import pandas as pd
import time

# Get the balance_sheet data with an API key
def get_balance_sheet(symbol):
    # Add the API key to the config.py file before running the code below
    url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={config.API_KEY}'
    print(url)
    r = requests.get(url)
    data = r.json()

    with open('../data/temp.json', 'w') as f:
        json.dump(data, f)   

# Use Pandas library json_normalize to write json data to a csv file
def write_to_csv():
    with open('../data/temp.json') as data_file:  
        data = json.load(data_file)

    df = pd.json_normalize(data, record_path=['quarterlyReports'], meta=['symbol'])
    df.to_csv("../data/balance-sheet.csv", mode='a', index=False, header=False, sep=',', encoding="utf-8") # write to csv file

def sort_values():
    df = pd.read_csv('../data/nasdaq_screener_1637250291945.csv')
    df.sort_values(by=['Market Cap'], axis=0, ascending=[False], inplace=True)
    df.to_csv('../data/sorted-values.csv')

# Warning! This will deplete a lot of your API requests
# Loading data into csv file
def load_dataset():
    df = pd.read_csv('../data/sorted-values.csv')
    df_lim = df.head(200)
    for symbol in df_lim['Symbol']:
        # Request balance sheet
        get_balance_sheet(symbol)
        write_to_csv()
        # Add a timout to prevent exceeding the API call limit (5 requests/min)
        time.sleep(15)


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





