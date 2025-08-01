import pandas as pd

def load_my_data():
    df2023 = pd.read_csv('data/2023.csv')
    df2024 = pd.read_csv('data/2024.csv')
    df2025 = pd.read_csv('data/2025.csv')
    df2025 = df2025.drop('1.5 Month', axis=1)

    #combine into 1 dataframe
    df = pd.concat([df2023, df2024, df2025], ignore_index=True)

    #convert date column to date time
    df['Date'] = pd.to_datetime(df['Date'])

    #sort based on date time 
    df = df.sort_values('Date').reset_index(drop=True)

    return df

def get_two_year_yields_from_last_3_months():
    """
    Extracts the 2-years yields from the loaded data.
    :return: A numpy array of 2-year yields.
    """
    df = load_my_data()
    if '2 Yr' not in df.columns:
        raise ValueError("2 Year yields not found in the data.")

    # Get the last 3 months of data
    last_3_months = df[df['Date'] >= (df['Date'].max() - pd.DateOffset(months=3))]
    if '2 Yr' not in last_3_months.columns:
        raise ValueError("2 Year yields not found in the data.")
    return last_3_months['2 Yr'].values

def get_five_year_yields_from_last_3_months():
    """
    Extracts the 5-year yields from the loaded data.
    :return: A numpy array of 5-year yields.
    """
    df = load_my_data()
    if '5 Yr' not in df.columns:
        raise ValueError("5 Year yields not found in the data.")

    # Get the last 3 months of data
    last_3_months = df[df['Date'] >= (df['Date'].max() - pd.DateOffset(months=3))]
    if '5 Yr' not in last_3_months.columns:
        raise ValueError("5 Year yields not found in the data.")

    return last_3_months['5 Yr'].values

def get_ten_year_yields_from_last_3_months():
    """
    Extracts the 10-year yields from the loaded data.
    :return: A numpy array of 10-year yields.
    """
    df = load_my_data()
    if '10 Yr' not in df.columns:
        raise ValueError("10 Year yields not found in the data.")

    # Get the last 3 months of data
    last_3_months = df[df['Date'] >= (df['Date'].max() - pd.DateOffset(months=3))]
    if '10 Yr' not in last_3_months.columns:
        raise ValueError("10 Year yields not found in the data.")

    return last_3_months['10 Yr'].values