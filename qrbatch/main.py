import os
import sys
import logging
import argparse
from qrbatch import __version__

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from qrbatch.utils.qr_generator import QRCodeGenerator
else:
    from qrbatch.utils.qr_generator import QRCodeGenerator


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description=f"QRBatch v{__version__} - Generate QR codes from Excel data")
    parser.add_argument("-d", "--data", default="resources/data.xlsx", help="Path to the input Excel file")
    parser.add_argument("-o", "--output", default="qr_codes", help="Output folder for QR codes")
    parser.add_argument("-c", "--config", default=os.path.join("config", "custom_config.ini"), help="Path to the configuration file")
    
    args = parser.parse_args()
    
    try:
        generator = QRCodeGenerator(args.data, args.output, args.config)
        generator.process_excel()
        logging.info(f"QR codes generated successfully. Output folder: {args.output}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()