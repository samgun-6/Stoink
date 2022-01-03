
from django.test import TestCase
import pandas as pd


# Create your tests here.
class Column(TestCase):
    def test_columns_topfivefeats(self):
        df = pd.read_csv(r'../client/data/topFiveFeats.csv', sep=',')
        expected = ["timestamp", "symbol", "1m", "reportedEPS", "totalNonCurrentAssets", "depreciation",
                    "proceedsFromRepaymentsOfShortTermDebt", "currentAccountsPayable"]
        self.assertTrue(set(expected) <= set(df.columns))
