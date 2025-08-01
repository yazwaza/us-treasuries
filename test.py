import unittest
from numpy.testing import assert_almost_equal
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from models.buttefly import Butterfly

from models.nelsonSiegelModel import NelsonSiegelModel

# Test the csv files
class TestCsvReader(unittest.TestCase):
    def setUp(self):
        self.df2023 = pd.read_csv('data/2023.csv')
        self.df2024 = pd.read_csv('data/2024.csv')
        self.df2025 = pd.read_csv('data/2025.csv')
        self.df2025.drop('1.5 Month', axis = 1, inplace = True)

        self.df = pd.concat([self.df2023, self.df2024, self.df2025], ignore_index=True)

        self.df['Date'] = pd.to_datetime(self.df['Date'])

        self.df = self.df.sort_values('Date').reset_index(drop=True)
        

    def test_df2023(self):
        self.assertEqual(self.df2023.shape, (250, 14))

    def test_df2024(self):
        self.assertEqual(self.df2024.shape, (250, 14)) 
    
    def test_df2025(self):
        self.assertEqual(self.df2025.shape, (136, 14))

    def test_df(self):
        self.assertEqual(self.df.shape, (636, 14))
    
    #Test number of columns
    def test_df(self):
        self.assertEqual(list(self.df.columns), ['Date', '1 Mo', '2 Mo', '3 Mo', '4 Mo', '6 Mo', '1 Yr', '2 Yr', '3 Yr', '5 Yr', '7 Yr', '10 Yr', '20 Yr', '30 Yr'])
    
    #Test order
    def test_df_order(self):
        first_col = self.df.iloc[:, 0]
        first_value = first_col.iloc[0]
        last_value = first_col.iloc[-1]
        self.assertEqual(first_value, pd.Timestamp('2023-01-03 00:00:00'))
        self.assertEqual(last_value, pd.Timestamp('2025-07-18 00:00:00'))

class TestCurveBuilding(unittest.TestCase):
    t = np.array([
        1/12, 2/12, 3/12, 4/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30
    ]) # Tenures in years
    β0 = 10 #long term rate
    β1 = 1/12 #short term rate
    β2 = 3 #medium term rate
    λ = 2.134999999999998 # decay factor
    params : list[float] = [β0, β1, β2, λ]
    ##US treasury yields for 1.5 Month, 2 Month, ..., 30 Year
    observed_yields = np.array([
        0.0445, 0.0436, 0.0436, 0.0431, 0.0425, 0.0417, 0.0425, 0.0429, 0.0438, 0.0447,
        0.0457, 0.0486, 0.0479
    ])

    def setUp(self):
        self.model = NelsonSiegelModel(self.observed_yields)
        self.mock_nelson_siegel = self.β0 + self.β1 * ((1 - np.exp(-self.t/self.λ)) / (self.t/self.λ)) + self.β2 * (((1 - np.exp(-self.t/self.λ)) / (self.t/self.λ)) - np.exp(-self.t/self.λ))

    def test_nelson_siegel(self):
        predicted_yield = self.model.nelson_siegel(self.β0, self.β1, self.β2, self.λ, self.t)
        assert_almost_equal(predicted_yield, self.mock_nelson_siegel)

    # Test the error function
    def test_error_function(self):
        result = self.model.nelder_mead(self.params, self.model.nelson_siegel_error_function)
    
        # Test that we get reasonable fitted parameters
        self.assertEqual(len(result.x), 4)
        self.assertTrue(result.success)
        
        # Test that final error is reasonable
        self.assertLess(result.fun, 100)  # Should be much less than initial error

    def test_nelson_siegel_svansson(self):
        # Test the Nelson-Siegel Svensson function
        β3 = 0.25633094
        λ1 = 2.134999999999998
        expected_yield = self.model.nelson_siegel_svansson(self.β0, self.β1, self.β2, β3, self.λ, λ1, self.t)
        # Calculate the expected yield using the mock function
        mock_yield = self.mock_nelson_siegel + β3 * (1 - np.exp(-self.t/λ1)) / (self.t/λ1) - np.exp(-self.t/λ1)
        assert_almost_equal(expected_yield, mock_yield)

    def test_nelson_siegel_svensson_error_function(self):
        # Test the error function for the Nelson-Siegel Svensson model
        β3 = 0.25633094
        λ1 = 2.134999999999998
        params = [self.β0, self.β1, self.β2, β3, self.λ, λ1]
        
        result = self.model.nelder_mead(params, self.model.nelson_siegel_svensson_error_function)
        
        # Test that we get reasonable fitted parameters
        self.assertEqual(len(result.x), 6)
        self.assertTrue(result.success)
        
        # Test that final error is reasonable
        self.assertLess(result.fun, 100)
    
    # def test_nelder_mead(self):
    #     result = self.model.nelder_mead(self.params)
    #     # Check if the optimization was successful
    #     self.assertTrue(result.success, "Nelder-Mead optimization failed")
    #     # Check if the optimized parameters are close to the expected values
    #     optimized_params = result.x
    #     assert_almost_equal(optimized_params, self.params, decimal=2)

    # def test_get_yield_curve(self):
    #     fitted_params = [0.0445, 0.0436, 0.0436, 2.134999999999998]
    #     yield_curve = self.model.get_yield_curve(fitted_params)
    #     assert_almost_equal(yield_curve, self.mock_nelson_siegel)

class TestButterflyHedging(unittest.TestCase):

    def setUp(self):
        self.model = ButterflyHedgingModel()

    def test_butterfly_hedging(self):
        result = self.model.butterfly_hedging()
        self.assertTrue(result.success)
        assert_almost_equal(result.x, self.model.expected_params, decimal=2)

if __name__ == '__main__':
    unittest.main()