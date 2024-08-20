import os
import logging
import argparse
from qrbatch import __version__
from qrbatch.exceptions import ConfigurationError, QRBatchProcessingError
from qrbatch.qr_batch_processor import QRCodeBatchProcessor
from qrbatch.utils.config_handler import ConfigHandler
from qrbatch.utils.data_processor import DataProcessor
from qrbatch.utils.file_handler import FileHandler
from qrbatch.utils.qr_generator import QRCodeGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description=f"QRBatch v{__version__} - Generate QR codes from Excel data")
    parser.add_argument("-d", "--data", default="resources/data.xlsx", help="Path to the input Excel file")
    parser.add_argument("-o", "--output", default="qr_codes", help="Output folder for QR codes")
    parser.add_argument("-c", "--config", default=os.path.join("config", "custom_config.json"), help="Path to the configuration file")
    
    args = parser.parse_args()
    
    try:
        config_handler = ConfigHandler(args.config)
        file_handler = FileHandler()
        data_processor = DataProcessor()
        qr_generator = QRCodeGenerator()
        
        generator = QRCodeBatchProcessor(
            args.data, 
            args.output, 
            config_handler,
            file_handler,
            data_processor,
            qr_generator
        )
        generator.process_excel()
        logging.info(f"QR codes generated successfully. Output folder: {args.output}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except ConfigurationError as e:
        logging.error(f"Configuration error: {e}")
    except QRBatchProcessingError as e:
        logging.error(f"QR batch processing error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()