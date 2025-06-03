import unittest
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ScraperService import ScraperService
from ConfigLoader import ConfigLoader
from JobOffer import JobOffer
from logger_config import log

class TestScraperService(unittest.TestCase):

    CONFIG_PATH = 'resources/config.yml'
    MAX_OFFERS_TO_CHECK_PER_SITE = 3

    @classmethod
    def setUpClass(cls):
        log.info(f"Setting up tests for ScraperService. Config path: {cls.CONFIG_PATH}")
        if not os.path.exists(cls.CONFIG_PATH):
            raise FileNotFoundError(
                f"Test configuration file not found: {cls.CONFIG_PATH}. "
                "Please ensure it exists and is correctly formatted for ScraperService.py."
            )
        try:
            config_loader = ConfigLoader(config_path=cls.CONFIG_PATH)
            cls.sites_config_for_test = config_loader.get_sites_config() 
            if not cls.sites_config_for_test:
                log.warning(f"No sites found in configuration file: {cls.CONFIG_PATH}. Tests might be limited.")

            cls.scraper_service = ScraperService(sites_config=cls.sites_config_for_test)
        except Exception as e:
            log.error(f"Failed to initialize ScraperService in setUpClass: {e}", exc_info=True)
            raise

    def test_scrape_first_few_offers_all_sites(self):
        log.info("Starting test: test_scrape_first_few_offers_all_sites")
        self.assertIsNotNone(self.scraper_service.sites_config, "Sites configuration is missing.")
        self.assertTrue(len(self.scraper_service.sites_config) > 0, "No sites configured to test.")

        for site_config in self.scraper_service.sites_config:
            site_id = site_config.get('id', 'Unknown Site ID')
            log.info(f"Testing scraping for site: {site_id}")
            
            with self.subTest(site=site_id):
                try:
                    offers = self.scraper_service.scrape_site(site_config)
                except Exception as e:
                    self.fail(f"scrape_site failed for {site_id} with exception: {e}")

                self.assertIsInstance(offers, list, f"scrape_site for {site_id} should return a list.")
                
                if not offers:
                    log.warning(f"No offers found for site {site_id}. Test for this site will be limited.")
                    continue

                log.info(f"Found {len(offers)} offers for site {site_id}. Checking up to {self.MAX_OFFERS_TO_CHECK_PER_SITE}.")

                for i, offer in enumerate(offers[:self.MAX_OFFERS_TO_CHECK_PER_SITE]):
                    log.debug(f"Checking offer {i+1}/{len(offers)} (max {self.MAX_OFFERS_TO_CHECK_PER_SITE}) for {site_id}: {offer.title}")
                    self.assertIsInstance(offer, JobOffer, f"Item {i} from {site_id} is not a JobOffer instance.")
                    self.assertIsNotNone(offer.title, f"Offer {i} from {site_id} has no title.")
                    self.assertTrue(len(offer.title.strip()) > 0, f"Offer {i} from {site_id} has an empty title.")
                    self.assertIsNotNone(offer.url, f"Offer {i} from {site_id} has no URL.")
                    self.assertTrue(len(offer.url.strip()) > 0, f"Offer {i} from {site_id} has an empty URL.")
                    self.assertTrue(offer.url.startswith('http'), f"Offer {i} URL '{offer.url}' from {site_id} does not look valid.")
                    self.assertEqual(offer.site_id, site_id, f"Offer {i} from {site_id} has incorrect site_id '{offer.site_id}'.")
        log.info("Finished test: test_scrape_first_few_offers_all_sites")

if __name__ == '__main__':
    log.info("Running ScraperService tests...")
    unittest.main()