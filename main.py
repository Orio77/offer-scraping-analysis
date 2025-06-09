from logger_config import log

from typing import List

from ConfigLoader import ConfigLoader
from ScraperService import ScraperService
from JobOffer import JobOffer
from EmailFormatService import EmailFormatService
from EmailSenderService import EmailSenderService
from SupabaseService import DatabaseConfig

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