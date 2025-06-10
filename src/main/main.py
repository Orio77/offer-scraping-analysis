import sys
import os

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.main.config.logger_config import log

from typing import List

from main.config.SitesConfigLoader import ConfigLoader
from src.main.service.ScraperService import ScraperService
from src.main.model.JobOffer import JobOffer
from src.main.service.EmailFormatService import EmailFormatService
from src.main.service.EmailSenderService import EmailSenderService
from src.main.persistance.Supabase import DatabaseConfig

def main():
    log.info("Starting the scraping process")
    
    log.info("Loading the configuration")
    config = ConfigLoader()
    websites = config.get_sites_config()
    log.info(f"Loaded {len(websites)} websites from the configuration")
    
    log.info("Scraping the data")
    scraper = ScraperService(websites)
    offers: List[JobOffer] = scraper.scrape_all_sites()
    log.info(f"Scraped {len(offers)} job offers from {len(websites)} websites")

    log.info("Saving the data")
    database = DatabaseConfig()
    database.create_table()
    inserted_offers = database.insert_data(offers)
    log.info("Data has been saved to the database")

    log.info("Formatting the scraped data")
    formatter = EmailFormatService()

    formatted_offers = formatter.format_job_offers_email(inserted_offers)
    log.info(f"Found {len(formatted_offers)} offers")

    log.info("Send emails")
    sender = EmailSenderService()
    sender.send_email(formatted_offers)
    log.info("Emails have been sent")

if __name__ == "__main__":
    main()