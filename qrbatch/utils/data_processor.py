import pandas as pd
from typing import List

class DataProcessor:
    @staticmethod
    def filter_columns(df: pd.DataFrame, include_columns: List[str], exclude_columns: List[str]) -> pd.DataFrame:
        if include_columns:
            columns_to_include = [col for col in df.columns if any(DataProcessor._column_matches(include, col) for include in include_columns)]
            return df[columns_to_include]
        elif exclude_columns:
            columns_to_exclude = [col for col in df.columns if any(DataProcessor._column_matches(exclude, col) for exclude in exclude_columns)]
            return df.drop(columns=columns_to_exclude, errors='ignore')
        return df

    @staticmethod
    def _column_matches(pattern: str, column: str) -> bool:
        return pattern.replace('\n', '').lower() in column.replace('\n', '').lower()

    @staticmethod
    def format_data(row: pd.Series) -> str:
        formatted_lines = []
        for column, value in row.items():
            value_str = str(value).replace('\n', ' / ')
            column_name = column.replace('\n', ' ')
            formatted_lines.append(f"{column_name.strip()}: {value_str}")
        return "\n".join(formatted_lines).strip()