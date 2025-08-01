import matplotlib.pyplot as plt

class OneDayView():

    def plot_yield_curve_proper_scale(self, curve):
        """
        Plot the yield curve for a single day
        X axis represents the different tenures 1 Month, 2 Month, ..., 30 Year
        they should be spaced according to the difference in time between them. 
        Y axis represents the yield in percentage.

        :param curve: The yield curve to plot.
        :param tenures: The tenures corresponding to the yield curve.
        """
        maturities = [1/12, 2/12, 3/12, 4/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30]  # Tenures in years
        plt.figure(figsize=(12, 6))

        # Use actual time values as x-coordinates
        plt.plot(maturities, curve, 'bo-', linewidth=2, markersize=6)

        # Set up x-axis with proper labels generated from tenures
        labels = ['1M', '2M', '3M', '4M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y', '30Y']
        # Ensure labels and maturities have the same length
        plt.xticks(maturities, labels[:len(maturities)], rotation=45)

        plt.xlabel('Maturity')
        plt.ylabel('Yield (%)')
        plt.title('Treasury Yield Curve')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()



