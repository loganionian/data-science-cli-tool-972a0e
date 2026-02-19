import pandas as pd
import json
import os
from typing import Any, Dict, List, Optional

class DataCleaner:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.df = self.load_data()

    def load_data(self) -> pd.DataFrame:
        if self.input_path.endswith('.json'):
            with open(self.input_path, 'r') as f:
                data = json.load(f)
            return pd.json_normalize(data)
        elif self.input_path.endswith('.csv'):
            return pd.read_csv(self.input_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")

    def save_data(self):
        if self.output_path.endswith('.json'):
            self.df.to_json(self.output_path, orient='records', lines=True)
        elif self.output_path.endswith('.csv'):
            self.df.to_csv(self.output_path, index=False)
        else:
            raise ValueError("Unsupported output format. Use CSV or JSON.")

    def remove_nulls(self, columns: Optional[List[str]] = None):
        if columns:
            self.df.dropna(subset=columns, inplace=True)
        else:
            self.df.dropna(inplace=True)

    def normalize_features(self, columns: List[str]):
        for column in columns:
            self.df[column] = (self.df[column] - self.df[column].mean()) / self.df[column].std()

    def remove_outliers(self, columns: List[str], threshold: float = 1.5):
        for column in columns:
            lower_bound = self.df[column].quantile(0.25) - (threshold * self.df[column].std())
            upper_bound = self.df[column].quantile(0.75) + (threshold * self.df[column].std())
            self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]

    def clean_data(self, remove_null: bool = False, normalize: bool = False, outlier_removal: bool = False):
        if remove_null:
            self.remove_nulls()
        if normalize:
            self.normalize_features(self.df.columns.tolist())
        if outlier_removal:
            self.remove_outliers(self.df.columns.tolist())

    def execute(self):
        self.clean_data()
        self.save_data()