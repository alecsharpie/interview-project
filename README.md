# Interview Project

## Introduction

The goal of the project is to create a database that can be queried to provide business insights

- What are top selling products?
- What is revenue by product?
- What revenue per customer?
- What is sales trend? Can we make some inferences between sales trend and other factors?
- Make use of 1 or more APIs e.g. can we overlay data using weather API to show sales and
weather trend or currency API to provide access of revenue in AUD?
- What are other interesting insights that you would like to share?


## Data

[Data](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II) is from UCI Machine Learning Repository. It is a transnational data set which contains all the transactions occurring between 01/12/2009 and 09/12/2011 for a UK-based and registered non-store online retail.

## Dimensions

InvoiceNo: Invoice number. Nominal. A 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter 'c', it indicates a cancellation.
StockCode: Product (item) code. Nominal. A 5-digit integral number uniquely assigned to each distinct product.
Description: Product (item) name. Nominal.
Quantity: The quantities of each product (item) per transaction. Numeric.
InvoiceDate: Invice date and time. Numeric. The day and time when a transaction was generated.
UnitPrice: Unit price. Numeric. Product price per unit in sterling (Â£).
CustomerID: Customer number. Nominal. A 5-digit integral number uniquely assigned to each customer.
Country: Country name. Nominal. The name of the country where a customer resides.
