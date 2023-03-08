import pandas as pd
import numpy as np

from tqdm import tqdm

import uuid

from retail.utils import join_uuid, get_latlon, great_circle_distance, get_weather

def process_sheet(df):

    df.columns = [
        'invoice_id', 'product_id', 'description', 'quantity', 'datetime',
        'price', 'customer_id', 'country'
    ]

    df['transaction_id'] = [uuid.uuid4().int for i in range(len(df))]

    df = df.sort_values('datetime', ascending=True)


    df['datetime'] = pd.to_datetime(df['datetime'])

    df = join_uuid(df, 'datetime', 'date_id')

    fact_transaction = df[[
        'transaction_id', 'invoice_id', 'product_id', 'customer_id',
        'quantity', 'price'
    ]]

    # Invoice table

    invoices = df.groupby('invoice_id').agg({'date_id': 'first'}).reset_index()

    invoices['cancelled'] = invoices['invoice_id'].str.startswith('C', na=False)

    ## Date Table

    dates = df.groupby('date_id').agg({'datetime': 'first'})

    # Create other date features

    dates['year'] = dates['datetime'].dt.year
    dates['quarter'] = dates['datetime'].dt.quarter
    dates['month'] = dates['datetime'].dt.month
    dates['day'] = dates['datetime'].dt.day_name()
    dates['hour'] = dates['datetime'].dt.hour

    ## Product Table

    # most recent price and description
    products = df.groupby('product_id').agg({'description': 'first', 'price': 'first'})

    ## Customer Table

    df = join_uuid(df, 'country', 'country_id')

    customers = df.groupby('customer_id').agg({
        'country_id': 'first'  # most recent country
    }).reset_index()

    ## Country Table


    countries = df.groupby('country_id').agg({'country': 'first'}).reset_index()

    uk_coords = (54.7023545, -3.2765753)


    country_stats = []

    for country in tqdm(countries['country'].unique()):
        lat, lon = get_latlon(country)
        avg_max_temp = get_weather(lat, lon)
        dist_from_uk = great_circle_distance(lat, uk_coords[0], lon, uk_coords[1])
        country_stats.append((country, lat, lon, avg_max_temp, dist_from_uk))

    countries = countries.merge(pd.DataFrame(
        country_stats,
        columns=['country', 'lat', 'lon', 'avg_max_temp', 'dist_from_uk']),
                                on='country')

    data = {
        'fact_transaction': fact_transaction,
        'invoices': invoices,
        'dates': dates,
        'products': products,
        'customers': customers,
        'countries': countries
    }

    return data
