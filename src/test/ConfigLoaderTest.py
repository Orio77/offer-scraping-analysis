import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import unittest
from unittest.mock import patch, mock_open
import yaml
from src.main.config.ConfigLoader import ConfigLoader 

class TestConfigLoader(unittest.TestCase):

    @patch('ConfigLoader.log') # Mock the logger
    def test_load_config_success(self, mock_log):
        with patch('builtins.open', mock_open(read_data="scraper:\n  sites:\n    - name: 'TestSite'\n      url: 'http://test.com'")) as mock_file, \
             patch('yaml.safe_load', return_value={'scraper': {'sites': [{'name': 'TestSite', 'url': 'http://test.com'}]}}) as mock_safe_load:
            config_loader = ConfigLoader(config_path='dummy_path.yml')
            self.assertIsNotNone(config_loader.config)
            self.assertEqual(config_loader.config['scraper']['sites'][0]['name'], 'TestSite')
            mock_log.info.assert_called_with("Configuration loaded successfully from 'dummy_path.yml'.")

    @patch('ConfigLoader.log') # Mock the logger
    def test_load_config_file_not_found(self, mock_log):
        with patch('builtins.open', side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                ConfigLoader(config_path='non_existent_path.yml')
            mock_log.error.assert_called_with("Configuration file 'non_existent_path.yml' not found.")

    @patch('ConfigLoader.log') # Mock the logger
    def test_load_config_yaml_error(self, mock_log):
        with patch('builtins.open', mock_open(read_data="invalid_yaml: [")) as mock_file, \
             patch('yaml.safe_load', side_effect=yaml.YAMLError("YAML parsing error")) as mock_safe_load:
            with self.assertRaises(ValueError) as context:
                ConfigLoader(config_path='invalid_yaml.yml')
            self.assertTrue("Error parsing YAML configuration" in str(context.exception))
            mock_log.error.assert_called_with("Error parsing YAML configuration file 'invalid_yaml.yml': YAML parsing error", exc_info=True)

    @patch('ConfigLoader.log') # Mock the logger
    def test_load_config_missing_scraper_section(self, mock_log):
        with patch('builtins.open', mock_open(read_data="some_other_key: value")) as mock_file, \
             patch('yaml.safe_load', return_value={'some_other_key': 'value'}) as mock_safe_load:
            with self.assertRaises(ValueError) as context:
                ConfigLoader(config_path='missing_scraper.yml')
            self.assertEqual(str(context.exception), "Invalid configuration file format.")
            # Assert the log message from the generic exception handler
            mock_log.error.assert_any_call("Invalid configuration file format. 'scraper' or 'sites' section missing.")
            mock_log.error.assert_any_call("Failed to load configuration from 'missing_scraper.yml': Invalid configuration file format.", exc_info=True)


    @patch('ConfigLoader.log') # Mock the logger
    def test_load_config_missing_sites_section(self, mock_log):
        with patch('builtins.open', mock_open(read_data="scraper:\n  other_key: value")) as mock_file, \
             patch('yaml.safe_load', return_value={'scraper': {'other_key': 'value'}}) as mock_safe_load:
            with self.assertRaises(ValueError) as context:
                ConfigLoader(config_path='missing_sites.yml')
            self.assertEqual(str(context.exception), "Invalid configuration file format.")
            # Assert the log message from the generic exception handler
            mock_log.error.assert_any_call("Invalid configuration file format. 'scraper' or 'sites' section missing.")
            mock_log.error.assert_any_call("Failed to load configuration from 'missing_sites.yml': Invalid configuration file format.", exc_info=True)

    @patch('ConfigLoader.log') # Mock the logger
    def test_get_sites_config_success(self, mock_log):
        expected_sites = [{'name': 'Site1'}, {'name': 'Site2'}]
        with patch('builtins.open', mock_open(read_data="scraper:\n  sites:\n    - name: 'Site1'\n    - name: 'Site2'")) as mock_file, \
             patch('yaml.safe_load', return_value={'scraper': {'sites': expected_sites}}) as mock_safe_load:
            config_loader = ConfigLoader(config_path='dummy_sites.yml')
            sites_config = config_loader.get_sites_config()
            self.assertEqual(sites_config, expected_sites)

    @patch('ConfigLoader.log') # Mock the logger
    def test_get_sites_config_empty(self, mock_log):
        with patch('builtins.open', mock_open(read_data="scraper:\n  sites: []")) as mock_file, \
             patch('yaml.safe_load', return_value={'scraper': {'sites': []}}) as mock_safe_load:
            config_loader = ConfigLoader(config_path='dummy_empty_sites.yml')
            sites_config = config_loader.get_sites_config()
            self.assertEqual(sites_config, [])

if __name__ == '__main__':
    unittest.main()