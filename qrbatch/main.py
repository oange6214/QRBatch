import os
import logging
import argparse
from utils.qr_generator import QRCodeGenerator

VERSION = "1.0.0"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description=f"QRBatch v{VERSION} - Generate QR codes from Excel data")
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