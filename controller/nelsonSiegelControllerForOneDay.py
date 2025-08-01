from csvReader import load_my_data
from view.oneDayView import OneDayView
from models.nelsonSiegelModel import NelsonSiegelModel

class NelsonSiegelControllerForOneDay:
    def __init__(self):
        # Load the data
        self.df = load_my_data()
        self.view = OneDayView()
        self.params = [4.69270036, 0.72601528, 1.25823072, 0.25633094]

    def extract_yields_for_one_day(self):
        ##just use the first row of the dataframe
        if self.df.empty:
            raise ValueError("DataFrame is empty. Please load data before extracting yields.")
        return self.df.iloc[1, 1:].values  # Extract yields from the first row, excluding the date column
    
    def extract_yields(self):
        # Assuming the first column is the date and the rest are yields
        # each column represents a different tenure 1 Mo, 2 Mo, ..., 30 Yr
        # We return the yields as a numpy array for further processing
        if self.df.empty:
            raise ValueError("DataFrame is empty. Please load data before extracting yields.")
        return self.df.iloc[:, 1:].values
    
    # Run the model and display the results for one day
    def run(self):
        #Get data
        yields = self.extract_yields_for_one_day()

        #create and run model on each day of the data set until the end

        self.model = NelsonSiegelModel(yields)
        # Initial parameters for the Nelder-Mead optimization

        # Fit the model using the Nelder-Mead method
        result = self.model.nelder_mead(self.params)

        self.params = result.x

        # Get the yield curve using the fitted parameters
        yield_curve = self.model.get_yield_curve(self.params)

        # Send to view
        self.view.plot_yield_curve_proper_scale(yield_curve)
