import pytest
import pandas as pd
from src.data_science_cli_tool.core import DataCleaner

def test_load_json():
    cleaner = DataCleaner('data/raw.json', 'data/cleaned.json')
    assert not cleaner.df.empty

def test_remove_nulls():
    df = pd.DataFrame({'a': [1, 2, None], 'b': [4, None, 6]})
    cleaner = DataCleaner('data/raw.json', 'data/cleaned.json')
    cleaner.df = df
    cleaner.remove_nulls(columns=['b'])
    assert not cleaner.df['b'].isnull().any()

def test_normalize_features():
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    cleaner = DataCleaner('data/raw.json', 'data/cleaned.json')
    cleaner.df = df
    cleaner.normalize_features(columns=['a'])
    assert abs(cleaner.df['a'].mean()) < 1e-5

def test_remove_outliers():
    df = pd.DataFrame({'a': [1, 2, 3, 1000], 'b': [4, 5, 6, 7]})
    cleaner = DataCleaner('data/raw.json', 'data/cleaned.json')
    cleaner.df = df
    cleaner.remove_outliers(columns=['a'])
    assert len(cleaner.df) == 3  # 1000 should be removed

def test_save_data():
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    cleaner = DataCleaner('data/raw.json', 'data/cleaned.json')
    cleaner.df = df
    cleaner.save_data()
    loaded_df = pd.read_csv('data/cleaned.json')
    pd.testing.assert_frame_equal(df, loaded_df)