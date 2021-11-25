from agent.transform import add_missing_cols_to_dataframe
import pandas as pd


def test_joining_of_tables():
    df = pd.DataFrame(data={'estate_id': [1], 'street': ['skolevej']})
    df_to_join = pd.DataFrame(data={'estate_id': [1], 'url': ['www.google.com']})
    df_result = add_missing_cols_to_dataframe(df, df_to_join, 'estate_id')
    df_expected = pd.DataFrame(data={'estate_id': [1], 'street': ['skolevej'], 'url': ['www.google.com']})
    assert df_result.equals(df_expected)
