import pandas as pd

def get_data():
    """Get the data from the source."""
    # Get Data
    DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx"
    raw_data = pd.read_excel(DATA_URL, sheet_name=None)
    return raw_data
