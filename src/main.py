import os
import logging
import argparse
from utils.qr_generator import QRCodeGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate QR codes from Excel data")
    parser.add_argument("excel_file", nargs='?', default="resources/data.xlsx", 
                        help="Path to the input Excel file")
    parser.add_argument("-o", "--output", default="qr_codes", 
                        help="Output folder for QR codes (default: qr_codes)")
    parser.add_argument("-c", "--config", default="config/custom_config.ini", 
                        help="Path to the configuration INI file (default: custom_config.ini)")
    args = parser.parse_args()

    if not os.path.exists(args.excel_file):
        parser.error(f"Excel file '{args.excel_file}' not found. Please provide a valid Excel file path.")

    return args

def main():
    args = parse_arguments()
    generator = QRCodeGenerator(args.excel_file, args.output, args.config)
    generator.process_excel()

if __name__ == "__main__":
    main()