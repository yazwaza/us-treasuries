from csvReader import load_my_data
from view.cubicSplineView import CubicSplineView
from models.cubicSpline import CubicSplineAnalyzer
import numpy as np



class CubicSplineController:
    def __init__(self):
        # Load the data
        self.df = load_my_data()
        self.view = CubicSplineView()
        self.model = CubicSplineAnalyzer(self.df)

    def run(self):
        """
        Run the cubic spline analysis and display the results.
        """
        # Extract maturities and yields from the DataFrame
        maturities = self.model.maturities
        yields = self.df.iloc[:, 1:].values  # Assuming the first column is the date

        # Calculate the cubic spline for each day (limit to first few days for demonstration)
        for i in range(min(3, len(yields))):  # Show first 3 days only
            spline = self.model.calculate_spline(yields[i])
            
            # Create smooth curve with more points for plotting
            smooth_maturities = np.linspace(maturities.min(), maturities.max(), 100)
            smooth_yields = spline(smooth_maturities)
            
            # Plot the results
            self.view.plot_yield_curve(maturities, yields[i], smooth_maturities, smooth_yields, self.df.columns[i + 1])
