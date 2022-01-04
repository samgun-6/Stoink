
from django.test import TestCase
from h5py._hl import dataset
from tensorflow.python.keras.backend import tile
from stock.models import AiModel, DataSet
import stock.admin as admin
import pandas as pd
from os.path import exists

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

class AiModelTestCase(TestCase):
    def setUp(self):
        
        # create dataset
        testDataset = DataSet.objects.create(title='testData.csv')

        # Create AiModel
        AiModel.objects.create(title='UnitModel', deployed=True, dataset=testDataset)

    def test_train_model_saves_file(self):
        testModel = AiModel.objects.get(id=1)

        # Simulate data uploaded to admin page and train a model
        df = pd.read_csv(filepath_or_buffer='data/testData.csv')
        testModel.dataset.putframe(df)
        testModel.train_model()

        # Assert if the file was created
        file_exists = exists('UnitModel.h5')
        self.assertTrue(file_exists, msg='File does not exist')

