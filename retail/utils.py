import uuid
import pandas as pd
import numpy as np
import requests
import math



def join_uuid(df, column_name, new_column_name='id'):

    unique_items = df[column_name].unique()

    invoice_id_key = pd.DataFrame({
        new_column_name: [uuid.uuid4().int for i in range(len(unique_items))],
        column_name:
        unique_items
    })

    return df.merge(invoice_id_key, on=column_name)



def get_latlon(country_name):

    url = "https://nominatim.openstreetmap.org/search"

    params = {"country": country_name, "format": "json"}

    response = requests.get(url, params=params).json()

    if response:
        return float(response[0].get('lat', np.nan)), float(response[0].get('lon', np.nan))
    else:
        return (np.nan, np.nan)



def great_circle_distance(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # calculate great-circle distance
    d = math.acos(
        math.sin(lat1) * math.sin(lat2) +
        math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)) * 6371

    return abs(d)


def get_weather(lat, lon, variable='temperature_2m_max'):

    url = "https://archive-api.open-meteo.com/v1/era5"

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2009-12-01",  # YYYY-MM-DD from dataset info
        "end_date": "2011-12-09",
        "timezone": "UTC",
        "daily": variable
    }

    response = requests.get(url,
                            params=params).json().get('daily',
                                                      {}).get(variable, [])

    if response:
        return sum(response) / len(response)
    else:
        return np.nan
