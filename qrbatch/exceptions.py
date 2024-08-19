from typing import Optional

class QRBatchProcessingError(Exception):
    """Base exception for QR batch processing errors."""
    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)

    def __str__(self):
        if self.original_exception:
            return f"{self.message} Original error: {str(self.original_exception)}"
        return self.message

class ExcelReadError(QRBatchProcessingError):
    """Raised when there's an error reading the Excel file."""
    def __init__(self, file_path: str, original_exception: Optional[Exception] = None):
        super().__init__(f"Error reading Excel file: {file_path}", original_exception)
        self.file_path = file_path

class SheetProcessingError(QRBatchProcessingError):
    """Raised when there's an error processing a specific sheet."""
    def __init__(self, sheet_name: str, original_exception: Optional[Exception] = None):
        super().__init__(f"Error processing sheet: {sheet_name}", original_exception)
        self.sheet_name = sheet_name

class QRGenerationError(QRBatchProcessingError):
    """Raised when there's an error generating a QR code."""
    def __init__(self, item_identifier: str, original_exception: Optional[Exception] = None):
        super().__init__(f"Error generating QR code for item: {item_identifier}", original_exception)
        self.item_identifier = item_identifier

class ConfigurationError(QRBatchProcessingError):
    """Raised when there's an error in the configuration."""
    def __init__(self, config_key: str, original_exception: Optional[Exception] = None):
        super().__init__(f"Configuration error for key: {config_key}", original_exception)
        self.config_key = config_key

class FileOperationError(QRBatchProcessingError):
    """Raised when there's an error in file operations."""
    def __init__(self, file_path: str, operation: str, original_exception: Optional[Exception] = None):
        super().__init__(f"File operation '{operation}' failed for: {file_path}", original_exception)
        self.file_path = file_path
        self.operation = operation