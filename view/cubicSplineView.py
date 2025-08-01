import matplotlib.pyplot as plt

class CubicSplineView:
    def __init__(self):
        pass

    def plot_yield_curve(self, maturities, yields, smooth_maturities, smooth_yields, date):
        """
        Plot the yield curve using cubic spline interpolation.

        :param maturities: Original maturity points.
        :param yields: Original yield values corresponding to maturities.
        :param smooth_maturities: Smooth maturity points for interpolated curve.
        :param smooth_yields: Smooth yield values from cubic spline.
        :param date: Date for which the yield curve is plotted.
        """
        plt.figure(figsize=(12, 6))
        
        # Plot original data points
        plt.plot(maturities, yields, 'ro', markersize=8, label='Market Data', zorder=3)
        
        # Plot smooth cubic spline curve
        plt.plot(smooth_maturities, smooth_yields, 'b-', linewidth=2, label='Cubic Spline', zorder=2)

        plt.xlabel('Maturity (Years)')
        plt.ylabel('Yield (%)')
        plt.title(f'Treasury Yield Curve - {date}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()