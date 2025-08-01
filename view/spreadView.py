import matplotlib.pyplot as plt

class SpreadView:
    def __init__(self):
        pass

    def plot_two_year_five_year_yields(self, two_year_yields, five_year_yields, dates):
        """
        Plot the 2-year and 5-year yields on a single graph.

        :param two_year_yields: A numpy array of 2-year yields.
        :param five_year_yields: A numpy array of 5-year yields.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(dates, two_year_yields, label='2-Year Yield', color='blue', marker='o')
        plt.plot(dates, five_year_yields, label='5-Year Yield', color='orange', marker='o')

        plt.xlabel('Date')
        plt.ylabel('Yield (%)')
        plt.title('2-Year and 5-Year Treasury Yields Over Time')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        #create a table with the yields and the spreads (5yr - 2yr yields)
        spreads = five_year_yields - two_year_yields
        
        # Prepare table data
        table_data = []
        for date, two_year, five_year, spread in zip(dates, two_year_yields, five_year_yields, spreads):
            # Convert numpy.datetime64 to pandas datetime, then to string
            date_str = str(date)[:10] if hasattr(date, 'astype') else date.strftime('%Y-%m-%d')
            table_data.append([date_str, f'{two_year:.2f}%', f'{five_year:.2f}%', f'{spread:.2f}%'])

        # Pagination settings
        rows_per_page = 15
        total_rows = len(table_data)
        total_pages = (total_rows + rows_per_page - 1) // rows_per_page  # Ceiling division
        
        # Create paginated tables
        for page in range(total_pages):
            start_idx = page * rows_per_page
            end_idx = min(start_idx + rows_per_page, total_rows)
            page_data = table_data[start_idx:end_idx]
            
            # Create figure for this page
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.axis('tight')
            ax.axis('off')
            
            table = ax.table(cellText=page_data,
                            colLabels=['Date', '2-Year Yield', '5-Year Yield', 'Spread (5Y - 2Y)'],
                            cellLoc='center',
                            loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 1.2)
            
            # Add page information to title
            plt.title(f'2-Year and 5-Year Yields with Spreads - Page {page + 1} of {total_pages}')
            plt.tight_layout()
            plt.show()

    def plot_spread(self, spreads, dates):
        """
        Plot the mean spread between 2-year and 5-year yields.

        :param mean_spread: A numpy array of the mean spread.
        :param two_year_yields: A numpy array of 2-year yields.
        :param five_year_yields: A numpy array of 5-year yields.
        :param dates: Dates corresponding to the yields.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(dates, spreads, label='Spread', color='green', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Spread (bps)')
        plt.title('Spreads Between 2-Year and 5-Year Yields Over Time')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_spread_histogram(self, spreads, mean_spread, std_spread):
        """
        Plot a histogram of spread values showing distribution, z score, and standard deviation.
        
        :param spreads: Array of daily spread values
        :param mean_spread: Mean of the spreads
        :param std_spread: Standard deviation of the spreads
        """
        plt.figure(figsize=(10, 6))
        
        # Create histogram
        n, bins, patches = plt.hist(spreads, bins=20, alpha=0.7, color='lightblue', 
                                   edgecolor='black', density=True)
        
        # Add vertical lines for mean and std deviation bands
        plt.axvline(mean_spread, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {mean_spread:.3f}%')
        plt.axvline(mean_spread + std_spread, color='orange', linestyle=':', linewidth=2,
                    label=f'Mean + 1σ: {mean_spread + std_spread:.3f}%')
        plt.axvline(mean_spread - std_spread, color='orange', linestyle=':', linewidth=2,
                    label=f'Mean - 1σ: {mean_spread - std_spread:.3f}%')
        
        plt.xlabel('Spread (2Yx5Y) %')
        plt.ylabel('Density')
        plt.title('Distribution of 2Yx5Y Spreads')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Add text box with statistics
        stats_text = f'Mean: {mean_spread:.3f}%\nStd Dev: {std_spread:.3f}%\nCount: {len(spreads)} days'
        plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        plt.show()

    def plot_z_scores(self, z_scores, dates):
        """
        Plot a histogram of Z-scores of the spreads.

        :param z_scores: Array of Z-scores.
        :param dates: Dates corresponding to the Z-scores.
        """
        plt.figure(figsize=(12, 6))
        # Create histogram of Z-scores
        plt.hist(z_scores, bins=20, alpha=0.7, color='lightblue', edgecolor='black', density=True)
        plt.xlabel('Z-Score')
        plt.ylabel('Density')
        plt.title('Z-Scores of Spreads Over Time')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        #plot the Z-scores over time
        plt.figure(figsize=(12, 6))
        plt.plot(dates, z_scores, label='Z-Score', color='purple', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Z-Score')
        plt.title('Z-Scores of Spreads Over Time')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
    
        plt.show()