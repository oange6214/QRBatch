import configparser
import json
from typing import List, Any, Dict
from abc import ABC, abstractmethod
from qrbatch.exceptions import ConfigurationError

class BaseConfigHandler(ABC):
    @abstractmethod
    def read_config(self, config_file: str) -> None:
        pass

    @abstractmethod
    def parse_config_list(self, section: str, option: str) -> List[str]:
        pass

    @abstractmethod
    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        pass

class IniConfigHandler(BaseConfigHandler):
    def __init__(self):
        self.config = configparser.ConfigParser()

    def read_config(self, config_file: str) -> None:
        self.config.read(config_file, encoding='utf-8')

    def parse_config_list(self, section: str, option: str) -> List[str]:
        try:
            if self.config.has_option(section, option):
                value = self.config.get(section, option)
                return [item.strip().replace('\\n', '\n') for item in value.split('\n') if item.strip()]
            return []
        except Exception as e:
            raise ConfigurationError(section, original_exception=e)

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        return self.config.get(section, option, fallback=fallback)

class JsonConfigHandler(BaseConfigHandler):
    def __init__(self):
        self.config: Dict[str, Any] = {}

    def read_config(self, config_file: str) -> None:
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    def parse_config_list(self, section: str, option: str) -> List[str]:
        try:
            value = self.config.get(section, {}).get(option, [])
            if isinstance(value, list):
                return [item.replace('\\n', '\n') for item in value if item.strip()]
            return []
        except Exception as e:
            raise ConfigurationError(section, original_exception=e)

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        return self.config.get(section, {}).get(option, fallback)

class ConfigHandler:
    def __init__(self, config_file: str):
        self.handler = self._get_handler(config_file)
        self.handler.read_config(config_file)

    def _get_handler(self, config_file: str) -> BaseConfigHandler:
        if config_file.endswith('.ini'):
            return IniConfigHandler()
        elif config_file.endswith('.json'):
            return JsonConfigHandler()
        else:
            raise ValueError(f"Unsupported file format: {config_file}")

    def parse_config_list(self, section: str, option: str) -> List[str]:
        return self.handler.parse_config_list(section, option)

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        return self.handler.get(section, option, fallback)

if __name__ == "__main__":
    ini_config = ConfigHandler("config.ini")
    ini_sheets = ini_config.parse_config_list("Sheets", "process")
    ini_header_row = ini_config.get("Header", "row", fallback=0)

    json_config = ConfigHandler("config.json")
    json_sheets = json_config.parse_config_list("Sheets", "process")
    json_header_row = json_config.get("Header", "row", fallback=0)

    print(f"INI Sheets: {ini_sheets}, Header Row: {ini_header_row}")
    print(f"JSON Sheets: {json_sheets}, Header Row: {json_header_row}")