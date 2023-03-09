import json
from tqdm import tqdm

from dotenv import load_dotenv

import pandas as pd
import numpy as np

from retail.processing import process_sheet
from retail.data import get_data
from retail.bigquery import BigQuery

from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
DATASET = "online_retail_uci_roller"

raw_data = get_data()
# df = raw_data['Year 2009-2010']

with open('table_schema.json', 'r') as f:
    table_schema = json.load(f)

bq = BigQuery(PROJECT_ID, DATASET)

for _key, sheet in raw_data.items():

    proc_tables = process_sheet(sheet)

    for name, schema in table_schema.items():
        table = proc_tables[name]
        print('\n', name, ' : ', table.shape)
        print(('-----'))
        print(table.dtypes)

        if name == 'fact_transactions':
            bq.create_table(name,
                            schema,
                            clustered_columns=['customer_id', 'product_id'])

        else:
            bq.create_table(name,
                            schema)

        chunk_size = 1000
        for i in tqdm(range(0, table.shape[0], chunk_size)):
            data_chunk = table.iloc[i:i + chunk_size].fillna(np.nan).replace([np.nan], [None])
            bq.insert_data(name, data_chunk.to_dict('records'))
