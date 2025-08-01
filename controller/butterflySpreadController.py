import numpy as np
import pandas as pd

from models.buttefly import Butterfly
from csvReader import get_five_year_yields_from_last_3_months, get_ten_year_yields_from_last_3_months, get_two_year_yields_from_last_3_months
from models.nelsonSiegelModel import NelsonSiegelModel
from controller.nelsonSiegelController import NelsonSiegelController
from view.butterflyView import ButterflyView
from csvReader import load_my_data


class ButterflyController:
    """
    Controller for managing the butterfly spread between yields.
    """

    def __init__(self):
        self.maturities = [1/12, 2/12, 3/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30]  # Maturities in years
        self.butterfly = Butterfly(self.maturities)
        # Load the last 3 months of yields for 2, 5, and 10 years
        self.df2 = get_two_year_yields_from_last_3_months()
        self.df5 = get_five_year_yields_from_last_3_months()
        self.df10 = get_ten_year_yields_from_last_3_months()
        
        # Get dates for indexing (load once)
        self.df = load_my_data()
        last_3_months = self.df[self.df['Date'] >= (self.df['Date'].max() - pd.DateOffset(months=3))]
        self.dates = last_3_months['Date'].values
        
        self.view = ButterflyView(self.df2, self.df5, self.df10)
        
        # Initialize Nelson-Siegel controller to get full curve data
        self.nss_controller = NelsonSiegelController()
        self.full_curve_data = self.nss_controller.extract_yields()  # Full yield curve data

    def run(self):
        print("=== EFFICIENT BUTTERFLY SPREAD ANALYSIS ===")
        print("Using vectorized operations and batch processing")
        print("Optimal R² thresholds:")
        print("- NSS Curve Fitting: R² > 0.90 (excellent), R² > 0.80 (good), R² < 0.80 (poor)")
        print("- Mean Reversion: R² < 0.10 (mean-reverting), R² > 0.50 (trending)")
        print()
        
        # Use the full curve data from NSS controller
        num_days = min(len(self.df2), len(self.full_curve_data))
        
        # Pre-allocate arrays for batch processing (MAJOR EFFICIENCY GAIN)
        butterfly_spreads_market = np.zeros(num_days)
        butterfly_spreads_nss = np.zeros(num_days)
        r_squared_values = np.zeros(num_days)
        twos_tens_spreads = np.zeros(num_days)
        five_year_levels = np.zeros(num_days)
        
        # Create single NSS model for parameter initialization (EFFICIENCY GAIN)
        print("Initializing NSS model...")
        template_nss_model = NelsonSiegelModel([self.full_curve_data[0]])
        template_nss_model.fit_nelson_siegel_svensson()
        initial_params = template_nss_model.fitted_params
        print(f"Template NSS parameters: {initial_params}")
        
        # Batch process all days with individual fitting
        for i in range(num_days):
            # Get market yields for butterfly calculation
            m_y2 = self.df2[i]
            m_y5 = self.df5[i]
            m_y10 = self.df10[i]

            # Calculate the butterfly spread using market yields
            butterfly_spreads_market[i] = self.butterfly.calculate_butterfly_spread(m_y2, m_y5, m_y10)

            # Get the full yield curve for this day from NSS controller
            daily_full_curve = self.full_curve_data[i]
            
            # Fit NSS model to THIS specific day (maintains accuracy)
            daily_nss_model = NelsonSiegelModel([daily_full_curve])
            daily_nss_model.fitted_params = initial_params  # Warm start for efficiency
            daily_nss_model.fit_nelson_siegel_svensson()
            
            # Get the fitted curve for this day
            nss_curve = daily_nss_model.get_nelson_siegel_svensson_curve(daily_nss_model.fitted_params)
            
            # Calculate R² for this day's curve fit (now should be excellent!)
            r_squared_values[i] = daily_nss_model.get_R_squared(daily_full_curve, nss_curve)
            
            # Extract yields for butterfly calculation from NSS fitted curve
            nss_y2_yield = nss_curve[6]   # 2Y yield at index 6
            nss_y5_yield = nss_curve[8]   # 5Y yield at index 8  
            nss_y10_yield = nss_curve[10] # 10Y yield at index 10
            
            # Calculate NSS butterfly spread
            butterfly_spreads_nss[i] = self.butterfly.calculate_butterfly_spread(nss_y2_yield, nss_y5_yield, nss_y10_yield)
            
            # Store regression features for batch processing
            twos_tens_spreads[i] = self.df2[i] - self.df10[i]
            five_year_levels[i] = self.df5[i]
            five_year_levels[i] = self.df5[i]

        # Batch regression hedging (SOLVES CIRCULAR DEPENDENCY + EFFICIENCY)
        print("Running batch multilinear regression hedging...")
        X = np.column_stack([twos_tens_spreads, five_year_levels])
        y = butterfly_spreads_nss
        self.butterfly.multilinear_regression_hedging(X, y)
        print(f"Regression coefficients: {self.butterfly.model.coef_}")
        print(f"Updated weights: {self.butterfly.weights}")

        #Mean reversion analysis for comparison
        print("Running mean reversion analysis...")
        mean_reversion_spread = np.mean(butterfly_spreads_market - butterfly_spreads_nss)
        std_reversion_spread = np.std(butterfly_spreads_market - butterfly_spreads_nss)
        print(f"Mean Reversion Spread: {mean_reversion_spread:.4f}%({mean_reversion_spread * 100:.1f} bps)")
        print(f"Standard Deviation of Reversion Spread: {std_reversion_spread:.4f}%({std_reversion_spread * 100:.1f} bps)")
    

        self.view.plot_butterfly_spreads(butterfly_spreads_market, butterfly_spreads_nss, r_squared_values, self.dates)
        self.view.plot_butterfly_z_scores(mean_reversion_spread, std_reversion_spread, butterfly_spreads_market - butterfly_spreads_nss)
