import pandas as pd
from typing import List, Callable, Optional

class DataProcessor:
    @staticmethod
    def filter_columns(df: pd.DataFrame, 
                       include_columns: Optional[List[str]] = None, 
                       exclude_columns: Optional[List[str]] = None) -> pd.DataFrame:
        if include_columns:
            return DataProcessor._include_columns(df, include_columns)
        elif exclude_columns:
            return DataProcessor._exclude_columns(df, exclude_columns)
        return df

    @staticmethod
    def _include_columns(df: pd.DataFrame, include_columns: List[str]) -> pd.DataFrame:
        columns_to_include = DataProcessor._get_matching_columns(df, include_columns)
        return df[columns_to_include]

    @staticmethod
    def _exclude_columns(df: pd.DataFrame, exclude_columns: List[str]) -> pd.DataFrame:
        columns_to_exclude = DataProcessor._get_matching_columns(df, exclude_columns)
        return df.drop(columns=columns_to_exclude, errors='ignore')

    @staticmethod
    def _get_matching_columns(df: pd.DataFrame, patterns: List[str]) -> List[str]:
        return [col for col in df.columns if any(DataProcessor._column_matches(pattern, col) for pattern in patterns)]

    @staticmethod
    def _column_matches(pattern: str, column: str) -> bool:
        return pattern.replace('\n', '').lower() in column.replace('\n', '').lower()

    @staticmethod
    def format_data(row: pd.Series, 
                    separator: str = ': ', 
                    line_separator: str = '\n',
                    value_processor: Callable[[str], str] = lambda x: x.replace('\n', ' / '),
                    column_processor: Callable[[str], str] = lambda x: x.replace('\n', ' ').strip()) -> str:
        formatted_lines = [
            f"{column_processor(str(column))}{separator}{value_processor(str(value))}"
            for column, value in row.items()
        ]
        return line_separator.join(formatted_lines).strip()

    @staticmethod
    def safe_process(func: Callable, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {str(e)}")
            return None

if __name__ == "__main__":
    df = pd.DataFrame({
        'Name': ['John Doe', 'Jane Smith'],
        'Age': [30, 25],
        'Address\nCity': ['New York\nNY', 'Los Angeles\nCA']
    })

    include_result = DataProcessor.safe_process(
        DataProcessor.filter_columns, df, include_columns=['Name', 'Age']
    )
    print("Include columns result:")
    print(include_result)

    exclude_result = DataProcessor.safe_process(
        DataProcessor.filter_columns, df, exclude_columns=['Age']
    )
    print("\nExclude columns result:")
    print(exclude_result)

    for _, row in df.iterrows():
        formatted = DataProcessor.safe_process(DataProcessor.format_data, row)
        print("\nFormatted data:")
        print(formatted)

    custom_formatted = DataProcessor.safe_process(
        DataProcessor.format_data, 
        df.iloc[0], 
        separator=' - ', 
        line_separator=' | ',
        value_processor=lambda x: x.upper(),
        column_processor=lambda x: x.lower()
    )
    print("\nCustom formatted data:")
    print(custom_formatted)