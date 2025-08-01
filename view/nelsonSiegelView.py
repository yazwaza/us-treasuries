import matplotlib.pyplot as plt

class NSSView:

    def plot_yield_curve_proper_scale(self, market_curve, svensson_curve, date, nss_R_squared):
        maturities = [1/12, 2/12, 3/12, 4/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30]
        maturity_labels = ['1M', '2M', '3M', '4M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y', '30Y']
        
        # Create figure with subplots - compact layout
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), 
                                       gridspec_kw={'height_ratios': [2.5, 1]})
        
        # Plot the curves
        ax1.plot(maturities, svensson_curve, 'green', linewidth=2, markersize=6, label='NSS Model')
        ax1.plot(maturities, market_curve, 'ro', markersize=6, label='Market Data')
        
        ax1.set_title(f'Treasury Yield Curve - {date}')
        ax1.set_xlabel('Maturity')
        ax1.set_ylabel('Yield (%)')
        ax1.set_xticks(maturities)
        ax1.set_xticklabels(maturity_labels, rotation=45)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))
        
        # Create table data with color coding
        table_data = []
        for i, maturity in enumerate(maturity_labels):
            nss_error = abs(market_curve[i] - svensson_curve[i])
            
            table_data.append([
                maturity,
                f'{market_curve[i]:.2f}%',
                f'{svensson_curve[i]:.2f}%',
                f'{nss_error:.2f}%',
                f'{nss_R_squared:.2f}'
            ])
        
        # Create table
        ax2.axis('tight')
        ax2.axis('off')
        table_obj = ax2.table(cellText=table_data,
                             colLabels=['Maturity', 'Market', 'NSS Model', 'Error', 'R²'],
                             cellLoc='center',
                             loc='center',
                             bbox=[0, 0, 1, 1])  # Fill entire subplot area
        table_obj.auto_set_font_size(False)
        table_obj.set_fontsize(7)
        table_obj.scale(1, 0.9)  # Compress table vertically
        
        # Color code the table headers
        for i in range(len(table_data[0])):
            table_obj[(0, i)].set_facecolor('#E6E6FA')
        
        # Color code error values in the table
        for i, maturity in enumerate(maturity_labels):
            nss_error = abs(market_curve[i] - svensson_curve[i])
            
            # Color Error column (column 3 - 0-indexed)
            if nss_error < 0.05:
                table_obj[(i+1, 3)].set_facecolor('#90EE90')  # Light green
            elif nss_error > 0.15:
                table_obj[(i+1, 3)].set_facecolor('#FFB6C1')  # Light red

        # Color code R² values
        for i in range(len(table_data)):  # Start from 0 to include first data row
            r_squared = float(table_data[i][4])
            if r_squared > 0.9:
                table_obj[(i+1, 4)].set_facecolor('#90EE90')  # Light green
            elif r_squared < 0.5:
                table_obj[(i+1, 4)].set_facecolor('#FFB6C1')  # Light red

        plt.subplots_adjust(hspace=0.1)  # Minimize space between subplots
        plt.tight_layout()
        plt.show()