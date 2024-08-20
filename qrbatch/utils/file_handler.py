import re
import os

class FileHandler:
    @staticmethod
    def clean_filename(filename: str) -> str:
        return re.sub(r'[\\/*?:"<>|\s]', '_', filename)

    @staticmethod
    def ensure_directory(directory: str) -> None:
        os.makedirs(directory, exist_ok=True)