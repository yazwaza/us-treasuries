import numpy as np
from sklearn.linear_model import LinearRegression
class Butterfly:
    def __init__(self, maturities):
        self.maturities = maturities
        self.model = LinearRegression()
        self.weights = np.array([-1, 2.0, -1])  # Weights for the butterfly spread

    def calculate_butterfly_spread(self, y1, y2, y3):
        # set weights for the butterfly spread
        # The weights are -1 for the first and last maturities, and
        # 2.0 for the middle maturity, which is a common configuration for butterfly spreads
        

        # Calculate the butterfly spread with dot product using the weights
        return np.dot(np.array([-1, 2.0, -1]), [y1, y2, y3])
    
    def compare_butterfly_spread(self, butterfly_spread_1, butterfly_spread_2):
        """
        Compare two butterfly spreads and return the difference.
        
        :param butterfly_spread_1: The first butterfly spread value.
        :param butterfly_spread_2: The second butterfly spread value.
        :return: The difference between the two spreads.
        """
        return butterfly_spread_1 - butterfly_spread_2

    def multilinear_regression_hedging(self, X, y):
        """
        Perform multilinear regression to hedge the butterfly spread.
        
        :param X: The independent variables (features) matrix of shape (n_samples, n_features).
        :param y: The butterfly spread values (target) of shape (n_samples,).
        :return: The fitted model.
        """
        # Ensure X is 2D array for sklearn
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        # Ensure y is 1D array for sklearn
        if hasattr(y, 'ndim') and y.ndim > 1:
            y = y.ravel()
        
        self.model.fit(X, y)

        # Return the coefficients of the fitted model
        beta1, beta2 = self.model.coef_

        # Update weights based on regression coefficients
        # Keep middle weight as 1.0 for duration neutrality
        self.weights = np.array([beta1, 1.0, beta2])
        
        return self.model
