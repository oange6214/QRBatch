import pandas as pd
import os
import logging
from qrbatch import __version__
from typing import Set, List, Optional

from qrbatch.exceptions import QRBatchProcessingError, QRGenerationError
from qrbatch.utils.config_handler import ConfigHandler
from qrbatch.utils.file_handler import FileHandler
from qrbatch.utils.data_processor import DataProcessor
from qrbatch.utils.qr_generator import QRCodeGenerator

class QRCodeBatchProcessor:
    def __init__(self, 
                 config_handler: ConfigHandler, 
                 file_handler: FileHandler,
                 data_processor: DataProcessor, 
                 qr_generator: QRCodeGenerator):
        self.config_handler = config_handler
        self.file_handler = file_handler
        self.data_processor = data_processor
        self.qr_generator = qr_generator
        
        self.config = self._load_config()
        self.version = __version__

    def _load_config(self):
        return {
            'sheets': self.config_handler.parse_config_list('Sheets', 'process'),
            'include_columns': self.config_handler.parse_config_list('Columns', 'include'),
            'exclude_columns': self.config_handler.parse_config_list('Columns', 'exclude'),
            'row_header': self.config_handler.get('Header', 'row')
        }

    def process_excel(self, excel_file: str, output_folder: str) -> None:
        logging.info(f"Running QR Code Generator version {self.version}")
        self.file_handler.ensure_directory(output_folder)
        
        try:
            with pd.ExcelFile(excel_file) as xls:
                sheets_to_process = self._get_sheets_to_process(xls.sheet_names)
                row_header = self._get_row_header()

                for sheet_name in sheets_to_process:
                    self._process_sheet(xls, sheet_name, row_header, output_folder)
        except Exception as e:
            logging.error(f"Error processing Excel file: {str(e)}")
            raise QRBatchProcessingError("Failed to process Excel file", original_exception=e)

    def _get_sheets_to_process(self, available_sheets: List[str]) -> Set[str]:
        available_sheets_set = set(available_sheets)
        return set(self.config['sheets']) & available_sheets_set if self.config['sheets'] else available_sheets_set

    def _get_row_header(self) -> Optional[int]:
        if not self.config['row_header']:
            return None
        try:
            return int(self.config['row_header'])
        except ValueError:
            logging.error(f"Invalid row header value: {self.config['row_header']}")
            raise QRBatchProcessingError(f"Invalid row header: {self.config['row_header']} is not an integer.")

    def _process_sheet(self, xls: pd.ExcelFile, sheet_name: str, row_header: Optional[int], output_folder: str) -> None:
        try:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=row_header)
            
            logging.info(f"Columns in sheet '{sheet_name}': {df.columns.tolist()}")
            df = self.data_processor.filter_columns(df, self.config['include_columns'], self.config['exclude_columns'])
            logging.info(f"Columns after filtering: {df.columns.tolist()}")

            sheet_folder = os.path.join(output_folder, sheet_name.strip())
            self.file_handler.ensure_directory(sheet_folder)

            df.apply(lambda row: self._process_row(row, sheet_name, sheet_folder), axis=1)
                
        except Exception as e:
            logging.error(f"Error processing sheet '{sheet_name}': {str(e)}")
            raise QRBatchProcessingError(f"Failed to process sheet '{sheet_name}'", original_exception=e)

    def _process_row(self, row: pd.Series, sheet_name: str, sheet_folder: str) -> None:
        try:
            item_index = self.file_handler.clean_filename(str(row.iloc[0]))
            item_identifier = self.file_handler.clean_filename(str(row.iloc[5]))
            
            if pd.isna(item_index) or item_index.lower() == 'nan':
                logging.warning(f"Skipped row with NaN identifier: {row.name}")
                return
            
            item_index = int(item_index.split('.')[0])
            
            formatted_data = self.data_processor.format_data(row)
            qr_filename = os.path.join(sheet_folder, f"f{item_index:04d}_{item_identifier}.png")
            self.qr_generator.generate_qr_code(formatted_data, qr_filename)
            logging.info(f"Generated QR code: {qr_filename}")
            
        except Exception as e:
            logging.error(f"Error processing row at index {row.name} in sheet '{sheet_name}': {str(e)}")
            raise QRGenerationError(f"Failed to process row at index {row.name} in sheet '{sheet_name}'", original_exception=e)