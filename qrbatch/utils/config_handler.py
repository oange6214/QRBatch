import configparser
import json
from typing import List, Any, Dict, Type
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
            raise ConfigurationError(f"Error parsing list in section '{section}', option '{option}'", original_exception=e)

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        try:
            return self.config.get(section, option, fallback=fallback)
        except configparser.Error as e:
            raise ConfigurationError(f"Error getting value from section '{section}', option '{option}'", original_exception=e)

class JsonConfigHandler(BaseConfigHandler):
    def __init__(self):
        self.config: Dict[str, Any] = {}

    def read_config(self, config_file: str) -> None:
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Error decoding JSON file: {config_file}", original_exception=e)

    def parse_config_list(self, section: str, option: str) -> List[str]:
        try:
            value = self.config.get(section, {}).get(option, [])
            if isinstance(value, list):
                return [item.strip().replace('\\n', '\n') for item in value if item.strip()]
            return []
        except Exception as e:
            raise ConfigurationError(f"Error parsing list in section '{section}', option '{option}'", original_exception=e)

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        try:
            return self.config.get(section, {}).get(option, fallback)
        except Exception as e:
            raise ConfigurationError(f"Error getting value from section '{section}', option '{option}'", original_exception=e)

class ConfigHandlerFactory:
    @staticmethod
    def create_handler(config_file: str) -> BaseConfigHandler:
        if config_file.endswith('.ini'):
            return IniConfigHandler()
        elif config_file.endswith('.json'):
            return JsonConfigHandler()
        else:
            raise ValueError(f"Unsupported file format: {config_file}")

class ConfigHandler:
    def __init__(self, config_file: str):
        self.handler = ConfigHandlerFactory.create_handler(config_file)
        self.handler.read_config(config_file)

    def parse_config_list(self, section: str, option: str) -> List[str]:
        return self.handler.parse_config_list(section, option)

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        return self.handler.get(section, option, fallback)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        ini_config = ConfigHandler("config.ini")
        ini_sheets = ini_config.parse_config_list("Sheets", "process")
        ini_header_row = ini_config.get("Header", "row", fallback=0)

        json_config = ConfigHandler("config.json")
        json_sheets = json_config.parse_config_list("Sheets", "process")
        json_header_row = json_config.get("Header", "row", fallback=0)

        logger.info(f"INI Sheets: {ini_sheets}, Header Row: {ini_header_row}")
        logger.info(f"JSON Sheets: {json_sheets}, Header Row: {json_header_row}")
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
    except ValueError as e:
        logger.error(f"Value error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)