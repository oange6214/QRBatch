import pandas as pd
import qrcode
import os
import logging
import configparser
from typing import List, Optional
import re

VERSION = "1.0.0"

class QRCodeGenerator:
    def __init__(self, excel_file: str, output_folder: str, config_file: str):
        self.version = __version__
        self.excel_file = excel_file
        self.output_folder = output_folder
        self.config = self.read_config(config_file)
        self.sheets = self.parse_config_list('Sheets', 'process')
        self.include_columns = self.parse_config_list('Columns', 'include')
        self.exclude_columns = self.parse_config_list('Columns', 'exclude')

    def read_config(self, config_file: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        return config

    def parse_config_list(self, section: str, option: str) -> List[str]:
        if self.config.has_option(section, option):
            value = self.config.get(section, option)
            # 使用 \\n 來表示實際的換行符
            return [item.strip().replace('\\n', '\n') for item in value.split('\n') if item.strip()]
        return []

    def filter_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.include_columns:
            columns_to_include = [col for col in df.columns if any(self.column_matches(include, col) for include in self.include_columns)]
            return df[columns_to_include]
        elif self.exclude_columns:
            columns_to_exclude = [col for col in df.columns if any(self.column_matches(exclude, col) for exclude in self.exclude_columns)]
            return df.drop(columns=columns_to_exclude, errors='ignore')
        return df

    def column_matches(self, pattern: str, column: str) -> bool:
        # 使用更靈活的匹配方法，允許部分匹配和忽略換行符
        return pattern.replace('\n', '').lower() in column.replace('\n', '').lower()

    def format_data(self, row: pd.Series) -> str:
        """Format a single row of data into readable text, handling newlines in cell values and column names"""
        formatted_lines = []
        for column in row.index:
            value = str(row[column])
            # 替換單元格內的換行為 ' / '
            value = value.replace('\n', ' / ')
            # 替換列名中的換行為空格
            column_name = column.replace('\n', ' ')
            formatted_lines.append(f"{column_name.strip()}: {value}")
        return "\n".join(formatted_lines).strip()

    def generate_qr_code(self, data: str, filename: str) -> None:
        """Generate QR code and save as an image file"""
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        
    def clean_filename(self, filename: str) -> str:
        """Remove or replace characters that are invalid in filenames"""
        return re.sub(r'[\\/*?:"<>|]', '_', filename)

    def process_excel(self) -> None:
        """Process Excel file and generate QR code for each row in each sheet"""
        
        logging.info(f"Running QR Code Generator version {self.version}")
       
        try:
            xls = pd.ExcelFile(self.excel_file)
            sheets_to_process = set(self.sheets) & set(xls.sheet_names)

            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)

            for sheet_name in sheets_to_process:
                try:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    logging.info(f"Columns in sheet '{sheet_name}': {df.columns.tolist()}")
                    df = self.filter_columns(df)
                    logging.info(f"Columns after filtering: {df.columns.tolist()}")

                    sheet_folder = os.path.join(self.output_folder, sheet_name)
                    if not os.path.exists(sheet_folder):
                        os.makedirs(sheet_folder)

                    for index, row in df.iterrows():
                        formatted_data = self.format_data(row)
                        item_identifier = self.clean_filename(str(row.iloc[0]))
                        qr_filename = os.path.join(sheet_folder, f"qr_{sheet_name}_item_{item_identifier}.png")
                        self.generate_qr_code(formatted_data, qr_filename)
                        logging.info(f"Generated QR code: {qr_filename}")

                except Exception as e:
                    logging.error(f"Error processing sheet '{sheet_name}': {str(e)}")

        except Exception as e:
            logging.error(f"Error processing Excel file: {str(e)}")
