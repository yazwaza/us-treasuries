import numpy as np
from sklearn.linear_model import LinearRegression

class MeanReversionCalculator:

    def find_mean_spread(self, two_year_yields, five_year_yields):

        """
        Calculate the mean spread between 2-year and 5-year yields.
        
        :param two_year_yields: A numpy array of 2-year yields.
        :param five_year_yields: A numpy array of 5-year yields.
        :return: The mean spread as a float.
        """
        if len(two_year_yields) != len(five_year_yields):
            raise ValueError("Yield arrays must have the same length.")
        
        spreads = five_year_yields - two_year_yields
        return np.mean(spreads)
    
    def calculate_spread(self, two_year_yields, five_year_yields):
        """
        Calculate the spread between 2-year and 5-year yields.
        
        :param two_year_yields: A numpy array of 2-year yields.
        :param five_year_yields: A numpy array of 5-year yields.
        :return: A numpy array of spreads.
        """
        if len(two_year_yields) != len(five_year_yields):
            raise ValueError("Yield arrays must have the same length.")
        
        return five_year_yields - two_year_yields
    
    def calculate_spread_max(self, two_year_yields, five_year_yields):
        """
        Calculate the maximum spread between 2-year and 5-year yields.
        
        :param two_year_yields: A numpy array of 2-year yields.
        :param five_year_yields: A numpy array of 5-year yields.
        :return: The maximum spread as a float.
        """
        spreads = self.calculate_spread(two_year_yields, five_year_yields)
        return np.max(spreads)

    def calculate_spread_min(self, two_year_yields, five_year_yields):
        """
        Calculate the minimum spread between 2-year and 5-year yields.

        :param two_year_yields: A numpy array of 2-year yields.
        :param five_year_yields: A numpy array of 5-year yields.
        :return: The minimum spread as a float.
        """
        spreads = self.calculate_spread(two_year_yields, five_year_yields)
        return np.min(spreads) 
    
    def calculate_spread_std(self, two_year_yields, five_year_yields):
        """
        Calculate the standard deviation of the spread between 2-year and 5-year yields.
        
        :param two_year_yields: A numpy array of 2-year yields.
        :param five_year_yields: A numpy array of 5-year yields.
        :return: The standard deviation of the spreads as a float.
        """
        spreads = self.calculate_spread(two_year_yields, five_year_yields)
        return np.std(spreads)

    def calculate_z_scores(self, current_spread, mean_spread, std_spread, slope, r_squared):
        """
        Only calculate if slope is minimal and R-squared is less than 0.1.
        If the conditions are not met, return None.
        Calculate the Z-score of the current spread.

        :param current_spread  : The current spread value.
        :param mean_spread: The mean spread value.
        :param std_spread: The standard deviation of the spreads.
        :return: The Z-score as a float.
        """
        if std_spread == 0:
            raise ValueError("Standard deviation cannot be zero for Z-score calculation.")

        if slope < 0.1 and r_squared < 0.1:
            return (current_spread - mean_spread) / std_spread
        return None

class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()

    def linear_regression(self, x, y):
        """
        Perform linear regression to find the slope and intercept
        """
        if len(x) != len(y):
            raise ValueError("Input arrays must have the same length.")
        
        x = x.reshape(-1, 1)
        # Fit the linear regression model
        self.model.fit(x, y)
        # Return the slope, intercept, and R-squared value
        return self.model.coef_[0], self.model.intercept_, self.model.score(x, y)
    
    def fit(self, yield_1, yield_2):
        """
        Fit a linear regression model to the yields.
        
        :param yield_1: A numpy array of 2-year yields.
        :param yield_2: A numpy array of 5-year yields.
        :return: The fitted model.
        """
        if len(yield_1) != len(yield_2):
            raise ValueError("Yield arrays must have the same length.")

        slope, intercept, r_2 = self.linear_regression(yield_1, yield_2)
        return slope, intercept, r_2