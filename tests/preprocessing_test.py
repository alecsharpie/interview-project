from retail.processing import process_sheet

import pandas as pd

def test_process_sheet():
    """Test the process_sheet function."""
    # Create a mock DataFrame
    df = pd.read_csv('tests/test_data.csv')

    # Call the function
    processed_data_dict = process_sheet(df)

    # Check the output
    assert len(processed_data_dict) == 6
    assert processed_data_dict['fact_transactions'].shape == (12, 6)
    assert processed_data_dict['invoices'].shape == (12, 3)
    assert processed_data_dict['dates'].shape == (12, 7)
    assert processed_data_dict['products'].shape == (11, 3)
    assert processed_data_dict['customers'].shape == (12, 2)
    assert processed_data_dict['countries'].shape == (4, 6)
