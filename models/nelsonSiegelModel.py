import numpy as np
from scipy.optimize import minimize

class NelsonSiegelModel:
    tenures = 13 
    def __init__(self, observed_yields):
        self.observed_yields = observed_yields
        self.maturities = np.array([
            1/12, 2/12, 3/12, 4/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30
        ])
        self.fitted_params = None

    #nelson siegel: calculates the yield curve using the nelson siegel formula
    def nelson_siegel(self, β0: float, β1: float, β2: float, λ, t):
        x = np.exp(-t/λ)
        term_1: float = (1 - x) / (t/λ)
        term_2: float = term_1 - x
        return  β0 + β1 * term_1 + β2 * term_2
    
    #nelson siegel svansson: calculates the yield curve using the nelson siegel svansson formula with additional parameters
    def nelson_siegel_svansson(self, β0, β1, β2, β3, λ0, λ1, t):
        term_3 = β3 * (1 - np.exp(-t/λ1)) / (t/λ1) - np.exp(-t/λ1)
        return self.nelson_siegel(β0, β1, β2, λ0, t) + term_3
    
    #error function: calculates the error between the predicted value and the actual yields for all tenures in 1 day
    def nelson_siegel_error_function(self, params):
        # Unpack parameters
        β0, β1, β2, λ = params

        predicted_yields = np.array([self.nelson_siegel(β0, β1, β2, λ, t) for t in self.maturities]) 

        #Calculate the residuals
        ## residuals: difference between the actual yields and the predicted yields

        residual = self.observed_yields - predicted_yields

        # Calculate and return the margin of error (sum of squared residuals)
        return np.sum(residual ** 2)
    
    def nelson_siegel_svensson_error_function(self, params):
        # Unpack parameters
        β0, β1, β2, β3, λ0, λ1 = params

        predicted_yields = np.array([self.nelson_siegel_svansson(β0, β1, β2, β3, λ0, λ1, t) for t in self.maturities])

        residual = self.observed_yields - predicted_yields
        
        # Add weight vector to emphasize 10Y fitting (index 10)
        weights = np.ones(len(residual))
        weights[10] = 2.0  # Double weight for 10Y to reduce bias
        
        # Weighted sum of squared residuals
        return np.sum(weights * residual ** 2)

    #nelder mead: creates a simplex shape using the predicted value from the nelson siegel 
    #and calibrates it until it fits the curve
    def nelder_mead(self, params, function):
        # Use the Nelder-Mead method to minimize the error function
        result = minimize(function, x0=params, method='Nelder-Mead')
        return result
    
    def nelder_mead_with_limits(self, params, error_function, max_iter=100):
        """
        Nelder-Mead optimization with iteration limits for efficiency
        """
        result = minimize(error_function, x0=params, method='Nelder-Mead',
                         options={'maxiter': max_iter, 'xatol': 1e-6})
        return result
    
    def nelder_mead_with_bounds(self, params, error_function, bounds, max_iter=100):
        """
        Bounded optimization using L-BFGS-B method with parameter bounds
        This prevents parameters from exploding to unreasonable values
        """
        result = minimize(error_function, x0=params, method='L-BFGS-B',
                         bounds=bounds, options={'maxiter': max_iter})
        return result
    

    def get_nelson_siegel_curve(self, fitted_params):
        # Get the yield curve using the fitted parameters
        β0, β1, β2, λ = fitted_params
        maturities = np.array([
            1/12, 2/12, 3/12, 4/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30
        ])  # Tenures in years
        
        # Vectorized calculation for all maturities
        return np.array([self.nelson_siegel(β0, β1, β2, λ, t) for t in maturities])

    def get_nelson_siegel_svensson_curve(self, fitted_params):
        # Get the yield curve using the fitted parameters
        β0, β1, β2, β3, λ0, λ1 = fitted_params
        maturities = np.array([
            1/12, 2/12, 3/12, 4/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30
        ])
        # Vectorized calculation for all maturities
        return np.array([self.nelson_siegel_svansson(β0, β1, β2, β3, λ0, λ1, t) for t in maturities])

    def set_bounds(self, bounds_1, bounds_2):
        """
        Set the bounds for the parameters of the Nelson-Siegel and Svensson models.
        :param bounds_1: Bounds for the Nelson-Siegel model parameters.
        :param bounds_2: Bounds for the Svensson model parameters.
        """
        self.bounds_1 = bounds_1
        self.bounds_2 = bounds_2
    
    def validate_parameters(self, params, param_type="NSS"):
        """
        Validate that parameters are within reasonable ranges
        """
        if param_type == "NSS":
            β0, β1, β2, β3, λ0, λ1 = params
            issues = []
            
            if not (0 <= β0 <= 10):
                issues.append(f"β0 (level) = {β0:.3f} is outside [0, 10]")
            if not (-5 <= β1 <= 5):
                issues.append(f"β1 (slope) = {β1:.3f} is outside [-5, 5]")
            if not (-10 <= β2 <= 10):
                issues.append(f"β2 (curvature) = {β2:.3f} is outside [-10, 10]")
            if not (-15 <= β3 <= 15):
                issues.append(f"β3 (hump) = {β3:.3f} is outside [-15, 15]")
            if not (0.1 <= λ0 <= 5):
                issues.append(f"λ0 (decay1) = {λ0:.3f} is outside [0.1, 5]")
            if not (0.1 <= λ1 <= 10):
                issues.append(f"λ1 (decay2) = {λ1:.3f} is outside [0.1, 10]")
                
            return len(issues) == 0, issues
        
        return True, []
    
    def get_R_squared(self, observed_yields, predicted_yields):
        """
        Calculate the R-squared value for the model fit.
        :param observed_yields: Actual yields from the market.
        :param predicted_yields: Yields predicted by the model.
        :return: R-squared value.
        """
        #error function output: SSR = sum((observed - predicted)^2)
        SSR = np.sum((observed_yields - predicted_yields) ** 2)
        # Total sum of squares: TSS = sum((observed - mean(observed))^2)
        TSS = np.sum((observed_yields - np.mean(observed_yields)) ** 2)
        
        return 1 - (SSR / TSS) if TSS != 0 else 0
    
    def fit_nelson_siegel_svensson(self, use_warm_start=True):
        """
        Fit the Nelson-Siegel-Svensson model to the observed yields.
        
        Args:
            use_warm_start (bool): If True and fitted_params exist, use them as starting point
        
        Returns:
            scipy.optimize.OptimizeResult: The optimization result containing the fitted parameters
        """
            
        # Define reasonable bounds for NSS parameters
        # Adjusted bounds to fix 10Y overestimation issue
        bounds = [
            (1.0, 8.0),    # β0 (level): reasonable yield levels
            (-6.0, 6.0),    # β1 (slope): reasonable slope range  
            (-8.0, 8.0),  # β2 (curvature): reasonable curvature
            (-6.0, 6.0),  # β3 (second hump): reasonable hump size
            (0.8, 3.5),    # λ0 (first decay): expanded range to fix 10Y bias
            (0.05, 0.4)    # λ1 (second decay): expanded range for better fitting
        ]
        
        # Determine starting parameters based on warm start preference
        if use_warm_start and self.fitted_params is not None and len(self.fitted_params) == 6:
            # Use previous day's fitted parameters as starting point (warm start)
            initial_params = self.fitted_params.copy()
            
            # Ensure starting parameters are within bounds
            for i, (param, (lower, upper)) in enumerate(zip(initial_params, bounds)):
                if param < lower:
                    initial_params[i] = lower + 0.01
                elif param > upper:
                    initial_params[i] = upper - 0.01
        else:
            # Cold start with optimized initial guesses for better 10Y fitting
            # Use more conservative curvature and hump parameters
            initial_params = [4.5, -1.2, -2.5, 1.5, 1.2, 0.12]
        
        # Perform optimization
        result = self.nelder_mead_with_bounds(initial_params,
                                              self.nelson_siegel_svensson_error_function,
                                              bounds, max_iter=1000)

        # Store the fitted parameters for next warm start
        self.fitted_params = result.x
        
        return result