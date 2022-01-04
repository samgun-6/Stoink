
from django.test import TestCase
from h5py._hl import dataset
from tensorflow.python.keras.backend import tile
from stock.models import AiModel, DataSet
import stock.admin as admin
import pandas as pd
from os.path import exists


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
        file_exists = exists('UnitModel_v1.h5')
        self.assertTrue(file_exists, msg='File does not exist')

# Create your tests here.
class Column(TestCase):
    def test_columns_topfivefeats(self):
        df = pd.read_csv(r'../client/data/topFiveFeats.csv', sep=',')
        expected = ["timestamp", "symbol", "1m", "reportedEPS", "totalNonCurrentAssets", "depreciation",
                    "proceedsFromRepaymentsOfShortTermDebt", "currentAccountsPayable"]
        self.assertTrue(set(expected) <= set(df.columns))
