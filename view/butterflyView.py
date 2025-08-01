import matplotlib.pyplot as plt

class ButterflyView:
    def __init__(self, df2, df5, df10):
        self.df2 = df2
        self.df5 = df5
        self.df10 = df10

    def plot_butterfly_spreads(self, butterfly_spreads_market, butterfly_spreads_nss, r_squared_values, dates):
        """
        Plot the butterfly spreads and R² values.

        :param butterfly_spreads_market: List of market butterfly spreads.
        :param butterfly_spreads_nss: List of NSS butterfly spreads.
        :param r_squared_values: List of R² values for NSS curve fit.
        :param dates: List of dates corresponding to the spreads.
        """
        plt.figure(figsize=(14, 8))
        
        # Plot market and NSS butterfly spreads
        plt.plot(dates, butterfly_spreads_market, 'ro-', label='Market Butterfly Spread', markersize=6)
        plt.plot(dates, butterfly_spreads_nss, 'go-', label='NSS Butterfly Spread', markersize=6)
        
        
        plt.title('Butterfly Spreads Comparison')
        plt.xlabel('Date')
        plt.ylabel('Butterfly Spread (%)')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()

        # Create a table with the spreads and R² values and compared spread values
        table_data = []
        for date, market_spread, nss_spread, r_squared in zip(dates, butterfly_spreads_market, butterfly_spreads_nss, r_squared_values):
            table_data.append([
                f'{date}',
                f'{market_spread:.2f}%',
                f'{nss_spread:.2f}%',
                f'{r_squared:.2f}',
                f'{market_spread - nss_spread:.2f}%'
            ])
        # Pagination settings
        rows_per_page = 15
        total_rows = len(table_data)
        total_pages = (total_rows + rows_per_page - 1) // rows_per_page 
        # Create paginated tables
        for page in range(total_pages):     
            start_idx = page * rows_per_page
            end_idx = min(start_idx + rows_per_page, total_rows)
            page_data = table_data[start_idx:end_idx]
            
            # Create figure for this page
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.axis('tight')
            ax.axis('off')
            
            table = ax.table(cellText=page_data,
                            colLabels=['Date', 'Market Spread', 'NSS Spread', 'R²', 'Spread Difference'],
                            cellLoc='center',
                            loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 1.2)
            
            plt.title(f'Butterfly Spreads Table - Page {page + 1} of {total_pages}')
            plt.tight_layout()
            plt.show()

    def plot_butterfly_z_scores(self, mean_reversion_spread, std_reversion_spread, difference):
        """
        Using a historgram to plot the z-scores of the difference in butterfly spreads.
        """

        plt.figure(figsize=(12, 6))
        z_scores = (difference - mean_reversion_spread) / std_reversion_spread
        
        plt.hist(z_scores, bins=30, color='blue', alpha=0.7, edgecolor='black')
        plt.axvline(0, color='red', linestyle='dashed', linewidth=1)
        
        plt.title('Z-Scores of Butterfly Spread Differences')
        plt.xlabel('Z-Score')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()