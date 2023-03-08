import json

from dotenv import load_dotenv

import pandas as pd

from retail.processing import process_sheet

load_dotenv()

# Get Data
DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx"

raw_data = pd.read_excel(DATA_URL, sheet_name=None)

df = raw_data['Year 2009-2010']

# Process Data
processed_data_dict = process_sheet(df)

for k, v in processed_data_dict.items():
    print('\n\n', k, ' : ', v.shape)
    print(v.dtypes)

# Open the JSON file and read its contents
with open('table_schema.json', 'r') as f:
    table_schema = json.load(f)
