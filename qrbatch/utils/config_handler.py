import configparser
from typing import List
from qrbatch import __version__
from qrbatch.exceptions import ConfigurationError

class ConfigHandler:
    def __init__(self, config_file: str):
        self.config = self._read_config(config_file)

    def _read_config(self, config_file: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        return config

    def parse_config_list(self, section: str, option: str) -> List[str]:
        try:
            if self.config.has_option(section, option):
                value = self.config.get(section, option)
                return [item.strip().replace('\\n', '\n') for item in value.split('\n') if item.strip()]
            return []
        except Exception as e:
            raise ConfigurationError(section, original_exception=e)