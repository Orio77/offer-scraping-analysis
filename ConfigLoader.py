import yaml
from typing import List, Dict, Any
from logger_config import log 

class ConfigLoader:
    def __init__(self, config_path='resources/config.yml'):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            if not config_data or 'scraper' not in config_data or 'sites' not in config_data['scraper']:
                log.error("Invalid configuration file format. 'scraper' or 'sites' section missing.")
                raise ValueError("Invalid configuration file format.")
            log.info(f"Configuration loaded successfully from '{self.config_path}'.")
            return config_data
        except FileNotFoundError:
            log.error(f"Configuration file '{self.config_path}' not found.")
            raise
        except yaml.YAMLError as e:
            log.error(f"Error parsing YAML configuration file '{self.config_path}': {e}", exc_info=True)
            raise ValueError(f"Error parsing YAML configuration: {e}")
        except Exception as e:
            log.error(f"Failed to load configuration from '{self.config_path}': {e}", exc_info=True)
            raise

    def get_sites_config(self) -> List[Dict[str, Any]]:
        return self.config.get('scraper', {}).get('sites', [])
    
if __name__ == "__main__":
    config_loader = ConfigLoader()
    sites_config = config_loader.get_sites_config()
    print(sites_config)