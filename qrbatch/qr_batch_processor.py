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
                 excel_file: str, 
                 output_folder: str, 
                 config_handler: ConfigHandler,
                 file_handler: FileHandler,
                 data_processor: DataProcessor,
                 qr_generator: QRCodeGenerator):
        self.excel_file = excel_file
        self.output_folder = output_folder
        
        self.config_handler = config_handler
        self.file_handler = file_handler
        self.data_processor = data_processor
        self.qr_generator = qr_generator
        
        self.sheets = self.config_handler.parse_config_list('Sheets', 'process')
        self.include_columns = self.config_handler.parse_config_list('Columns', 'include')
        self.exclude_columns = self.config_handler.parse_config_list('Columns', 'exclude')
        self.row_header = self.config_handler.parse_config_list('Header', 'row')
        
        self.version = __version__

    def process_excel(self) -> None:
        logging.info("Running QR Code Generator version %s", self.version)
        self.file_handler.ensure_directory(self.output_folder)
        
        try:
            with pd.ExcelFile(self.excel_file) as xls:
                sheets_to_process = self._get_sheets_to_process(xls.sheet_names)
                row_header = self._get_row_header()

                for sheet_name in sheets_to_process:
                    self._process_sheet(xls, sheet_name, row_header)
        except Exception as e:
            logging.error("Error processing Excel file: %s", str(e))
            raise QRBatchProcessingError("Failed to process Excel file", original_exception=e)

    def _get_sheets_to_process(self, available_sheets: List[str]) -> Set[str]:
        available_sheets_set = set(available_sheets)
        return set(self.sheets) & available_sheets_set if self.sheets else available_sheets_set

    def _get_row_header(self) -> Optional[int]:
        if not self.row_header:
            return None
        try:
            return int(self.row_header[0])
        except ValueError:
            logging.error("Invalid row header value: %s", self.row_header)
            raise QRBatchProcessingError(f"Invalid row header: {self.row_header} is not an integer.")

    def _process_sheet(self, xls: pd.ExcelFile, sheet_name: str, row_header: Optional[int]) -> None:
        try:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=row_header)
            
            logging.info("Columns in sheet '%s': %s", sheet_name, df.columns.tolist())
            df = self.data_processor.filter_columns(df, self.include_columns, self.exclude_columns)
            logging.info("Columns after filtering: %s", df.columns.tolist())

            sheet_folder = os.path.join(self.output_folder, sheet_name)
            self.file_handler.ensure_directory(sheet_folder)

            for index, row in df.iterrows():
                self._process_row(row, index, sheet_name, sheet_folder)
                
        except Exception as e:
            logging.error("Error processing sheet '%s': %s", sheet_name, str(e))
            raise QRBatchProcessingError(f"Failed to process sheet '{sheet_name}'", original_exception=e)

    def _process_row(self, row: pd.Series, index: int, sheet_name: str, sheet_folder: str) -> None:
        try:
            item_index = self.file_handler.clean_filename(str(row.iloc[0]))
            item_name = self.file_handler.clean_filename(str(row.iloc[2]))
            item_identifier = self.file_handler.clean_filename(str(row.iloc[5]))
            
            if pd.isna(item_index) or item_index.lower() == 'nan':
                logging.warning("Skipped row at index %d due to NaN identifier.", index)
                return
            
            item_index = int(item_index.split('.')[0])
            
            formatted_data = self.data_processor.format_data(row)
            qr_filename = os.path.join(sheet_folder, f"f{item_index:04d}_{item_identifier}.png")
            self.qr_generator.generate_qr_code(formatted_data, qr_filename)
            logging.info("Generated QR code: %s", qr_filename)
            
        except Exception as e:
            logging.error("Error processing row at index %d in sheet '%s': %s", item_index, sheet_name, str(e))
            raise QRGenerationError(f"Failed to process row at index {item_index} in sheet '{sheet_name}'", original_exception=e)