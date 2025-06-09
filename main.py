from logger_config import log

from typing import List

from ConfigLoader import ConfigLoader
from ScraperService import ScraperService
from JobOffer import JobOffer
from EmailFormatService import EmailFormatService
from EmailSenderService import EmailSenderService
from DatabaseConfig import DatabaseConfig

def main():
    log.info("Starting the scraping process")
    
    log.info("Loading the configuration")
    config = ConfigLoader()
    websites = config.get_sites_config()
    
    log.info("Scraping the data")
    scraper = ScraperService(websites)
    offers: List[JobOffer] = scraper.scrape_all_sites()

    log.info("Formatting the scraped data")
    formatter = EmailFormatService()
    formatted_offers = formatter.format_job_offers_email(offers)
    log.info(f"Found {len(offers)} offers")

    log.info("Saving the data")

    database = DatabaseConfig()
    database.create_database()
    database.create_table()
    database.insert_data(offers)

    #for element in database.read_data():
    #    print(element)

    log.info("Process completed successfully!")

    log.info("Send emails")
    sender = EmailSenderService()
    sender.send_email(formatted_offers)

if __name__ == "__main__":
    main()