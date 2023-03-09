from retail.data import get_data

def test_get_data():
    """Test the get_data function."""
    raw_data = get_data()
    columns = ['Invoice', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'Price', 'Customer ID', 'Country']
    assert raw_data
    for key, sheet in raw_data.items():
        assert len(sheet) > 0
        assert list(sheet.columns) == columns
