from logger_config import log

from typing import List

from ConfigLoader import ConfigLoader
from ScraperService import ScraperService
from JobOffer import JobOffer
from EmailFormatService import EmailFormatService
from EmailSenderService import EmailSenderService

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

    log.info("Saving the data")

    log.info("Send emails")
    sender = EmailSenderService()
    sender.send_email(formatted_offers)

if __name__ == "__main__":
    main()