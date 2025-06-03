from logger_config import log

from typing import List

from ConfigLoader import ConfigLoader
from ScraperService import ScraperService
from JobOffer import JobOffer

def main():
    log.info("Starting the scraping process")
    
    log.info("Loading the configuration")
    config = ConfigLoader()
    websites = config.get_sites_config()
    
    log.info("Scraping the data")
    scraper = ScraperService(websites)
    offers: List[JobOffer] = scraper.scrape_all_sites()

    log.info("Saving the data")
    
    log.info("Process completed successfully!")

    log.info("Send emails")

if __name__ == "__main__":
    main()