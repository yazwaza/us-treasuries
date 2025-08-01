from csvReader import get_two_year_yields_from_last_3_months, get_five_year_yields_from_last_3_months, load_my_data
from view.spreadView import SpreadView
from models.spreadMeanCalculator import MeanReversionCalculator
from models.spreadMeanCalculator import LinearRegressionModel

class SpreadController:
    """
    Controller for managing the spread between two-year and five-year yields.
    """

    def __init__(self):
        self.view = SpreadView()
        self.model = MeanReversionCalculator()
        self.linear_model = LinearRegressionModel()
        self.df_2 = get_two_year_yields_from_last_3_months()
        self.df_5 = get_five_year_yields_from_last_3_months()
        self.df = load_my_data()
        self.mean_spread = self.model.find_mean_spread(self.df_2, self.df_5)
        self.spreads = self.model.calculate_spread(self.df_2, self.df_5)
        self.std_spread = self.model.calculate_spread_std(self.df_2, self.df_5)

    def run_averages(self):
        """
        Run the averaging process for the yield curves.
        """
        two_year_yields = self.df_2
        five_year_yields = self.df_5

        # Calculate the maximum, minimum, and standard deviation of the spreads
        max_spread = self.model.calculate_spread_max(two_year_yields, five_year_yields)
        min_spread = self.model.calculate_spread_min(two_year_yields, five_year_yields)

        # Calculate the linear regression model for the spreads
        linear_model = self.linear_model.fit(two_year_yields, five_year_yields)
        slope = linear_model[0]
        r_squared = linear_model[2]
        # Calculate the z-scores for the spreads
        z_scores = self.model.calculate_z_scores(self.spreads, self.mean_spread, self.std_spread, 
                                                 slope, r_squared)
        # Store the z-scores for plotting
        self.view.z_scores = z_scores

        # Plot the histogram showing spread distribution
        # self.view.plot_spread_histogram(self.spreads, self.mean_spread, self.std_spread)   
        # Print summary statistics
        print(f"\\n5Y-2Y Spread Statistics:")
        print(f"Mean Spread: {self.mean_spread:.4f}% ({self.mean_spread*100:.1f} bps)")
        print(f"Standard Deviation: {self.std_spread:.4f}% ({self.std_spread*100:.1f} bps)")
        print(f"Min Spread: {min_spread:.4f}% ({min_spread*100:.1f} bps)")
        print(f"Max Spread: {max_spread:.4f}% ({max_spread*100:.1f} bps)")
        print(f"Data covers {len(self.spreads)} days")
        print(f"Slope: {slope:.4f}, R-squared: {r_squared:.4f}")
        
