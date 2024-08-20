import re
import os
from typing import Optional, Any, Callable
from pathlib import Path

class FileHandler:
    @staticmethod
    def clean_filename(filename: str, replacement: str = '_', 
                       invalid_chars: str = r'[\\/*?:"<>|\s]') -> str:
        """
        清理檔名，替換無效字元。

        :param filename: 原始檔名
        :param replacement: 用於替換無效字元的字元
        :param invalid_chars: 定義無效字元的正規表示式
        :return: 清理後的檔名
        """
        return re.sub(invalid_chars, replacement, filename)

    @staticmethod
    def ensure_directory(directory: str, mode: int = 0o777) -> None:
        """
        確保目錄存在，如果不存在則建立。

        :param directory: 目錄路徑
        :param mode: 目錄權限模式
        """
        try:
            os.makedirs(directory, mode=mode, exist_ok=True)
        except OSError as e:
            raise IOError(f"無法建立目錄 '{directory}': {e}")

    @staticmethod
    def safe_file_operation(operation: Callable, *args, **kwargs) -> Optional[Any]:
        """
        安全地執行檔案操作，處理可能的例外情況。

        :param operation: 要執行的檔案操作函式
        :param args: 傳遞給操作的位置參數
        :param kwargs: 傳遞給操作的關鍵字參數
        :return: 操作的結果，如果出錯則回傳 None
        """
        try:
            return operation(*args, **kwargs)
        except (IOError, OSError) as e:
            print(f"檔案操作錯誤: {e}")
            return None

    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """
        取得檔案的基本資訊。

        :param file_path: 檔案路徑
        :return: 包含檔案資訊的字典
        """
        path = Path(file_path)
        return {
            "name": path.name,
            "extension": path.suffix,
            "size": path.stat().st_size if path.exists() else None,
            "created_time": path.stat().st_ctime if path.exists() else None,
            "modified_time": path.stat().st_mtime if path.exists() else None,
        }

# 使用範例
if __name__ == "__main__":
    # 清理檔名
    print(FileHandler.clean_filename("file: with * invalid ? chars.txt"))
    
    # 確保目錄存在
    FileHandler.safe_file_operation(FileHandler.ensure_directory, "test_directory")
    
    # 取得檔案資訊
    file_info = FileHandler.safe_file_operation(FileHandler.get_file_info, "example.txt")
    if file_info:
        print(f"檔案資訊: {file_info}")
    
    # 自訂清理檔名
    custom_clean = FileHandler.clean_filename("file with spaces.txt", replacement="-", invalid_chars=r'\s')
    print(f"自訂清理後的檔名: {custom_clean}")