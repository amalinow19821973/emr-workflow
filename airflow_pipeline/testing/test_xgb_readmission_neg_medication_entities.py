import sys
sys.path.insert(0,'..')

import unittest
#import the script from the main directory
import xgb_readmission_neg_medication_entities

class SomeCallableTest(unittest.TestCase):

    # create test cases for make_one_hot, train_xgb_model, add_predictions_column, make_top_n_features
    def test_1(self):
        #assert(somecallable.some_function() == 'some expected value')
        assert(2 == 2)

if __name__ == '__main__':
    unittest.main()
