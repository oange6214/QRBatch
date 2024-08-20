import os
import logging
import argparse
from typing import Dict, Any
from qrbatch import __version__
from qrbatch.exceptions import ConfigurationError, QRBatchProcessingError
from qrbatch.qr_batch_processor import QRCodeBatchProcessor
from qrbatch.utils.config_handler import ConfigHandler
from qrbatch.utils.data_processor import DataProcessor
from qrbatch.utils.file_handler import FileHandler
from qrbatch.utils.qr_generator import QRCodeGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"QRBatch v{__version__} - Generate QR codes from Excel data")
    parser.add_argument("-d", "--data", default="resources/data.xlsx", help="Path to the input Excel file")
    parser.add_argument("-o", "--output", default="qr_codes", help="Output folder for QR codes")
    parser.add_argument("-c", "--config", default=os.path.join("config", "custom_config.json"), help="Path to the configuration file")
    return parser.parse_args()

def setup_dependencies(config_path: str) -> Dict[str, Any]:
    return {
        'config_handler': ConfigHandler(config_path),
        'file_handler': FileHandler(),
        'data_processor': DataProcessor(),
        'qr_generator': QRCodeGenerator()
    }

def process_qr_codes(processor: QRCodeBatchProcessor, input_file: str, output_folder: str) -> None:
    processor.process_excel(input_file, output_folder)
    logger.info(f"QR codes generated successfully. Output folder: {output_folder}")

def main() -> None:
    args = parse_arguments()
    
    try:
        dependencies = setup_dependencies(args.config)
        processor = QRCodeBatchProcessor(**dependencies)
        process_qr_codes(processor, args.data, args.output)
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
    except QRBatchProcessingError as e:
        logger.error(f"QR batch processing error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()