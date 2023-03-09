import pandas as pd
import numpy as np

from tqdm import tqdm

import uuid

from retail.utils import join_uuid, get_latlon, great_circle_distance, get_weather

def process_sheet(df):
    """Process the raw data into a dictionary of dataframes."""

    df.columns = [
        'invoice_id',
        'product_id',
        'description',
        'quantity',
        'datetime',
        'price',
        'customer_id',
        'country'
    ]

    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime', ascending=True)

    df['transaction_id'] = [uuid.uuid4() for _ in range(len(df))]
    df = join_uuid(df, 'datetime', 'date_id')
    df = join_uuid(df, 'country', 'country_id')

    str_cols = [
        'invoice_id',
        'product_id',
        'description',
        'customer_id',
        'country',
        'transaction_id',
        'date_id',
        'country_id'
    ]

    df['price'] = df['price'].astype(float)
    df['quantity'] = df['quantity'].astype(int)
    df[str_cols] = df[str_cols].astype(str)

    # Invoices Table

    invoices = df[['invoice_id']].drop_duplicates()

    invoices['cancelled'] = invoices['invoice_id'].str.startswith('C', na=False)

    # Dates Table

    dates = df.groupby('date_id').agg({
        'datetime': 'first'
        }).reset_index()

    dates['year'] = dates['datetime'].dt.year
    dates['quarter'] = dates['datetime'].dt.quarter
    dates['month'] = dates['datetime'].dt.month
    dates['day'] = dates['datetime'].dt.day_name()
    dates['hour'] = dates['datetime'].dt.hour

    dates['datetime'] = dates['datetime'].astype(str)

    # Products Table

    products = df.groupby('product_id').agg({
        'description': 'first',
        'price': 'first'
        }).reset_index()

    # Countries Table

    countries = df.groupby('country_id').agg({
        'country': 'first'
        }).reset_index()

    uk_coords = (54.7023545, -3.2765753)

    country_stats = []
    print("Getting country data, geocode & weather API...")
    for country in tqdm(countries['country'].unique()):
        lat, lon = get_latlon(country)
        avg_max_temp = get_weather(lat, lon)
        dist_from_uk = great_circle_distance(lat, uk_coords[0], lon, uk_coords[1])
        country_stats.append((country, lat, lon, avg_max_temp, dist_from_uk))

    countries = countries.merge(pd.DataFrame(
        country_stats,
        columns=['country', 'lat', 'lon', 'avg_max_temp', 'dist_from_uk']),
                                on='country')

    # Customer Table

    customers = df.groupby('customer_id').agg({
        'country_id': 'first'
    }).reset_index()

    # Fact Table - Transactions

    fact_transactions = df[[
        'transaction_id', 'invoice_id', 'product_id', 'customer_id', 'date_id',
        'quantity'
    ]]

    return {
        'invoices': invoices,
        'dates': dates,
        'products': products,
        'countries': countries,
        'customers': customers,
        'fact_transactions': fact_transactions,
    }
