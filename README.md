# Interview Project

The goal of the project is to create a database that can be queried to provide business insights

# Data

[Data](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II) is from UCI Machine Learning Repository. It is a transnational data set which contains all the transactions occurring between 01/12/2009 and 09/12/2011 for a UK-based and registered non-store online retail.

## Dimensions

InvoiceNo: Invoice number. Nominal. A 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter 'c', it indicates a cancellation.
StockCode: Product (item) code. Nominal. A 5-digit integral number uniquely assigned to each distinct product.
Description: Product (item) name. Nominal.
Quantity: The quantities of each product (item) per transaction. Numeric.
InvoiceDate: Invoice date and time. Numeric. The day and time when a transaction was generated.
UnitPrice: Unit price. Numeric. Product price per unit in sterling (Â£).
CustomerID: Customer number. Nominal. A 5-digit integral number uniquely assigned to each customer.
Country: Country name. Nominal. The name of the country where a customer resides.

# Additional data

Geolocation data is obtained from [Nominatim API](https://nominatim.org/)
Weather data is obtained from [Open-Meteo API](https://open-meteo.com/)

# Usage

You will need to set up a GCP service key with the bigquery permissions.
This key should be saved as a JSON file and the path to the file should be set as an environment variable called GOOGLE_APPLICATION_CREDENTIALS.
A tutorial can be found [here](https://cloud.google.com/iam/docs/keys-create-delete#iam-service-account-keys-create-console)

### Clone the repository
```bash
git clone
```

### Install the requirements
```bash
pip install -r requirements.txt
```

### Run the script to load the data into bigquery
```bash
python load_data.py
```

### Run the script to create views in bigquery
```bash
python create_views.py
```

### Run the tests
```bash
pytest tests
```
