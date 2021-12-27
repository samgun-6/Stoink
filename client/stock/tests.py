
from django.test import TestCase
import pandas as pd

# Create your tests here.
def test_cleaned_data_columns(csvfile):
    df = pd.read_csv (r'../client/data/balance-sheet.csv', sep=',')

    actual = []
    expected = ["timestamp", "symbol", "1m","reportedEPS","totalNonCurrentAssets","depreciation",
               "proceedsFromRepaymentsOfShortTermDebt","currentAccountsPayable"]
    for col in df.columns:
        actual.append(col)

    if set(actual) == set(expected):
        return True
    else:
        return False

test_cleaned_data_columns('topFiveFeats.csv')

