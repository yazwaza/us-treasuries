from csvReader import load_my_data

from view.nelsonSiegelView import NSSView
from models.nelsonSiegelModel import NelsonSiegelModel

class NelsonSiegelController:
    def __init__(self):
        # Load the data
        self.df = load_my_data()
        self.view = NSSView()

    def extract_yields(self):
        # Assuming the first column is the date and the rest are yields
        # each column represents a different tenure 1 Mo, 2 Mo, ..., 30 Yr
        # We return the yields as a numpy array for further processing
        if self.df.empty:
            raise ValueError("DataFrame is empty. Please load data before extracting yields.")
        return self.df.iloc[:, 1:].values

    # Run the model and display the results one day at a time with efficient error checking
    def run_with_warm_start(self):
        initial_params = [4.5, -1.5, -4.0, 3.0, 0.8, 0.15]  # Initial parameters for the Svensson model

        # Define reasonable bounds for NSS parameters
        bounds = [
            (1.0, 8.0),    # β0 (level): reasonable yield levels
            (-6.0, 6.0),    # β1 (slope): reasonable slope range  
            (-8.0, 8.0),  # β2 (curvature): reasonable curvature
            (-6.0, 6.0),  # β3 (second hump): reasonable hump size
            (0.6, 2.0),     # λ0 (first decay): reasonable decay rate
            (0.08, 0.25)     # λ1 (second decay): reasonable decay rate
        ]

        # Set the bounds for the Nelder-Mead optimization
        self.model = NelsonSiegelModel(self.extract_yields())
        # Error thresholds for efficiency
        GOOD_ERROR_THRESHOLD = 0.05  # Skip intensive optimization if error is below this
        ACCEPTABLE_ERROR_THRESHOLD = 0.15  # Use moderate optimization
        
        # Counters for efficiency tracking
        quick_optimizations = 0
        moderate_optimizations = 0 
        intensive_optimizations = 0

        # Process each day's data
        for day_index in range(len(self.df)):
            # Extract yields for this specific day (excluding the date column)
            daily_yields = self.df.iloc[day_index, 1:].values
            current_date = self.df.iloc[day_index, 0]
        
            print(f"Processing day {day_index + 1}/{len(self.df)}: {current_date}")
            
            # Create model with this day's yields
            self.model = NelsonSiegelModel(daily_yields)
            
            # STEP 1: Quick optimization with current parameters (limited iterations)
            result = self.model.nelder_mead_with_bounds(initial_params, self.model.nelson_siegel_svensson_error_function, bounds, max_iter=50)
            
            # Cal
            nss_curve = self.model.get_nelson_siegel_svensson_curve(result.x)
            
            # NSS Model: Check SHORT-TERM error (1M-3Y, indices 0-7)
            nss_short_term_residuals = daily_yields[:8] - nss_curve[:8]  # 1M through 3Y
            nss_short_term_error = sum(nss_short_term_residuals ** 2)
            
            # NSS Model: Check MID-TERM error (5Y-10Y, indices 8-10)
            nss_mid_term_residuals = daily_yields[8:11] - nss_curve[8:11]  # 5Y, 7Y, 10Y
            nss_mid_term_error = sum(nss_mid_term_residuals ** 2)
            
            # NSS Model: Check LONG-TERM error (20Y-30Y, indices 11-12)
            nss_long_term_residuals = daily_yields[11:] - nss_curve[11:]  # 20Y, 30Y
            nss_long_term_error = sum(nss_long_term_residuals ** 2)
            
            print(f"NSS Short-term: {nss_short_term_error:.4f}, NSS Mid-term: {nss_mid_term_error:.4f}, NSS Long-term: {nss_long_term_error:.4f}")
            
            # STEP 2: Decide optimization level based on maturity-specific errors
            # For NSS: Check all three regions (short, mid, long), for NS: check short-term
            if (nss_short_term_error < GOOD_ERROR_THRESHOLD and 
                nss_mid_term_error < GOOD_ERROR_THRESHOLD and 
                nss_long_term_error < GOOD_ERROR_THRESHOLD):
                print("Excellent fit - All error regions below threshold")
                quick_optimizations += 1
                
            elif (nss_short_term_error < ACCEPTABLE_ERROR_THRESHOLD and 
                  nss_mid_term_error < ACCEPTABLE_ERROR_THRESHOLD and 
                  nss_long_term_error < ACCEPTABLE_ERROR_THRESHOLD):
                print("Moderate optimization needed - Some regions need improvement")
                # Medium optimization (200 iterations)
                result = self.model.nelder_mead_with_bounds(initial_params, self.model.nelson_siegel_svensson_error_function, bounds, max_iter=200)
                moderate_optimizations += 1
                
            else:
                print("Intensive optimization required - Poor fit in one or more regions")
                # Full optimization (1000 iterations)
                result = self.model.nelder_mead_with_bounds(initial_params, self.model.nelson_siegel_svensson_error_function, bounds, max_iter=1000)
                intensive_optimizations += 1
            
            # Update parameters for next iteration (warm start)
            initial_params = result.x

        
            print(f"NSS Parameters: {result.x}")

            print(f"Final errors - NSS Short-term: {nss_short_term_error:.4f}, NSS Mid-term: {nss_mid_term_error:.4f}, NSS Long-term: {nss_long_term_error:.4f}")
            print(f"Full curve errors - NSS Total: {result.fun:.4f}")
            
            # Get the yield curve using the fitted parameters
            svensson_curve = self.model.get_nelson_siegel_svensson_curve(initial_params)

            current_date = self.df.iloc[day_index, 0]
            
            # Get the market curve for the current date
            market_curve = self.df.iloc[day_index, 1:].values

            # Plot the yield curve
            self.view.plot_yield_curve_proper_scale(market_curve, svensson_curve, current_date, self.model.get_R_squared(market_curve, svensson_curve))

        # Print efficiency summary
        total_days = len(self.df)
        print(f"\\EFFICIENCY SUMMARY:")
        print(f"Quick optimizations: {quick_optimizations}/{total_days} ({quick_optimizations/total_days*100:.1f}%)")
        print(f"Moderate optimizations: {moderate_optimizations}/{total_days} ({moderate_optimizations/total_days*100:.1f}%)")
        print(f"Intensive optimizations: {intensive_optimizations}/{total_days} ({intensive_optimizations/total_days*100:.1f}%)")
