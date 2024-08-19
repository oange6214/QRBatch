import pandas as pd
import qrcode
import os
import logging
import configparser
from typing import List, Optional
import re
from qrbatch import __version__

class QRCodeGenerator:
    def __init__(self, excel_file: str, output_folder: str, config_file: str):
        self.excel_file = excel_file
        self.output_folder = output_folder
        self.config = self.read_config(config_file)
        self.sheets = self.parse_config_list('Sheets', 'process')
        self.include_columns = self.parse_config_list('Columns', 'include')
        self.exclude_columns = self.parse_config_list('Columns', 'exclude')
        self.row_header = self.parse_config_list('Header', 'row')
        self.version = __version__

    def read_config(self, config_file: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        return config

    def parse_config_list(self, section: str, option: str) -> List[str]:
        if self.config.has_option(section, option):
            value = self.config.get(section, option)
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
        return pattern.replace('\n', '').lower() in column.replace('\n', '').lower()

    def format_data(self, row: pd.Series) -> str:
        """Format a single row of data into readable text, handling newlines in cell values and column names"""
        formatted_lines = []
        for column in row.index:
            value = str(row[column])
            value = value.replace('\n', ' / ')
            column_name = column.replace('\n', ' ')
            formatted_lines.append(f"{column_name.strip()}: {value}")
        return "\n".join(formatted_lines).strip()

    def generate_qr_code(self, data: str, filename: str) -> None:
        """Generate QR code and save as an image file"""
        qr = qrcode.QRCode(
            version=None, 
            error_correction=qrcode.constants.ERROR_CORRECT_L, 
            box_size=10, 
            border=4
        )
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
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        
        try:
            xls = pd.ExcelFile(self.excel_file)
            
            if self.sheets:
                sheets_to_process = set(self.sheets) & set(xls.sheet_names)
            else:
                sheets_to_process = xls.sheet_names
            
            row_header = None
            if self.row_header:
                try:
                    row_header = int(self.row_header[0])
                except ValueError:
                    logging.error(f"Invalid row header value: {self.row_header}")
                    raise ValueError(f"Invalid row header: {self.row_header} is not an integer.")

            for sheet_name in sheets_to_process:
                self.process_sheet(xls, sheet_name, row_header)

        except Exception as e:
            logging.error(f"Error processing Excel file: {str(e)}")
            raise

    def process_sheet(self, xls, sheet_name, row_header):
        try:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=row_header)
            logging.info(f"Columns in sheet '{sheet_name}': {df.columns.tolist()}")
            df = self.filter_columns(df)
            logging.info(f"Columns after filtering: {df.columns.tolist()}")

            sheet_folder = os.path.join(self.output_folder, sheet_name)
            if not os.path.exists(sheet_folder):
                os.makedirs(sheet_folder)

            for index, row in df.iterrows():
                self.process_row(row, index, sheet_name, sheet_folder)

        except Exception as e:
            logging.error(f"Error processing sheet '{sheet_name}': {str(e)}")
            raise

    def process_row(self, row, index, sheet_name, sheet_folder):
        item_identifier = self.clean_filename(str(row.iloc[0]))
        
        if pd.isna(item_identifier) or item_identifier.lower() == 'nan':
            logging.warning(f"Skipped row at index {index} due to NaN identifier.")
            return
        
        formatted_data = self.format_data(row)
        qr_filename = os.path.join(sheet_folder, f"qr_{sheet_name}_item_{index}.png")
        self.generate_qr_code(formatted_data, qr_filename)
        logging.info(f"Generated QR code: {qr_filename}")